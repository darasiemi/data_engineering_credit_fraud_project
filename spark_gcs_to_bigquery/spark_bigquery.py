import argparse

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import date_format
from pyspark.sql.functions import to_timestamp
# from pyspark.sql.functions import month


import os
import sys 

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

parser = argparse.ArgumentParser()

parser.add_argument('--input_credit', nargs='+', required=True)
# parser.add_argument('--input_credit', required=True)
parser.add_argument('--output', required=True)

args = parser.parse_args()

input_credit = args.input_credit
output = args.output

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

bucket = 'dara-project-bucket'
spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west4-690544574168-akp05xcw')

df = spark.read.parquet(*input_credit, inferSchema=True)

df = df \
    .withColumnRenamed('date', 'tranc_date') \
    
schema = df.schema
print("schema is", schema)

colums = df.columns

df = df \
    .select(colums) \
    .withColumn('month', F.date_format(df['tranc_date'], 'MMMM')) \
    .withColumn('tranc_timestamp', F.to_timestamp(df['tranc_date'], 'yyyy-MM-dd HH:mm:ss')) \
    .drop(df['tranc_date']) 
    
 # Partition by timestamp
df = df.repartition(50)
print("dataframe repartitioned")

# Sort data within partiions by timestamp
df = df.sortWithinPartitions('tranc_timestamp')
print("dataframe ordered by timestamp")


df_data = df.show()
row_count = df.count()
print("Number of rows in DataFrame:", row_count)

df.createOrReplaceTempView('credit_fraud_table')

df_result = spark.sql("""
SELECT
  tranc_timestamp,
  month, 
  type, 
  amount, 
  name_orig, 
  oldbalance_org, 
  newbalance_orig, 
  name_dest, 
  oldbalance_dest, 
  newbalance_dest, 
  is_fraud, 
  is_flagged_fraud   
FROM
    credit_fraud_table                     
""")

df_result.write.format('bigquery') \
    .option('table', output) \
    .save()