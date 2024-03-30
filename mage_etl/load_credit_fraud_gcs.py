# if 'data_loader' not in globals():
#     from mage_ai.data_preparation.decorators import data_loader
# if 'test' not in globals():
#     from mage_ai.data_preparation.decorators import test

import pandas as pd
import os
from datetime import datetime, timedelta
import inflection
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import pyarrow as pa
import pyarrow.parquet as pq
import os
from google.cloud import storage

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

#Function to upload data to gcs
def upload_to_gcs(data,root_path):
    
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()
    
    pq.write_to_dataset(
        table,
        root_path,
        coerce_timestamps="us",
        filesystem=gcs)
    
#Function to get new start date and end date after each chunk of data
def update_date_range(start_date, end_date, chunk_size_minutes):
    current_date = start_date
    while current_date < end_date:
        next_date = min(current_date + timedelta(minutes=chunk_size_minutes), end_date)
        yield current_date, next_date
        current_date = next_date

def parquets_to_gcs():
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    # config_path = path.join(get_repo_path(), 'io_config.yaml')
    # config_profile = 'default'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/keys/my-creds.json"
    bucket_name = 'dara-project-bucket'
    #Datatypes for the data
    dtypes = {"type":str, 
            "amount": float,
            "nameOrig":str, 
            "oldbalanceOrg":float,
            "newbalanceOrig":float,
            "nameDest": str, 
            "oldbalanceDest": float,
            "newbalanceDest": float,
            "isFraud": pd.Int64Dtype(),  
            "isFlaggedFraud": pd.Int64Dtype()
            }
    #Because the data is large, we are read it in chunks
    chunksize = 100000
    # parse_dates = ["date"] 

    df_iter = pd.read_csv("/home/src/magic-zoomcamp/archive.zip" \
                         ,dtype=dtypes,iterator= True \
                         ,chunksize = chunksize  \
                         ,low_memory=False)
    # Define the start and end datetime
    start_date = datetime(2010, 1, 1)
    end_date = datetime(2034, 12, 12) #an arbitrary long date where loop terminates.
    chunk_size_minutes = chunksize  # Chunk size in minutes
    # Get first chunk
    df = next(df_iter)
    # Create a datetime range with minute frequency
    df['step'] = pd.date_range(start=start_date, periods=chunk_size_minutes, freq='T')

    df.rename(columns={'step': 'date'}, inplace=True)
    #Convert from date range to string time. This will later be converted back to timestamp using Spark
    df.date = df.date.dt.strftime("%Y-%m-%d %H:%M:%S")
    #Get all columns that are Camel case
    camel_case = [col for col in df.columns if inflection.underscore(col) != col]
    print(f"Number of camelCase columns: {len(camel_case)}")
    #Change from camel case to snake case
    df.columns = [inflection.underscore(col) for col in df.columns]
   
    object_key = f'credit_fraud_parquet'
    #The parquet files are saved into folders by year of the start date of the chunk
    root_path = f"{bucket_name}/{object_key}/{start_date.year}"
    upload_to_gcs(df,root_path)
    print("Uploaded to GCS successfully")
     #Get the new start and end chunk date
    start_chunk_date, end_chunk_date = next(update_date_range(start_date, end_date, chunk_size_minutes))

    
    while True:
        try:
            # get the next item
            df = next(df_iter)
            print(df.shape)
            #For the last chunk, the number of records is less than the chunk size of 100000. Update this
            if df.shape[0] < chunk_size_minutes:
                chunk_size_minutes = df.shape[0]

            start_date =   end_chunk_date
            df['step'] = pd.date_range(start=start_date, periods=chunk_size_minutes, freq='T')

            df.rename(columns={'step': 'date'}, inplace=True)
            df.date = df.date.dt.strftime("%Y-%m-%d %H:%M:%S")
            # Change columns to snake_case
            camel_case = [col for col in df.columns if inflection.underscore(col) != col]
            df.columns = [inflection.underscore(col) for col in df.columns]

            object_key = f'credit_fraud_parquet'
            #The parquet files are saved into folders by year of the start date of the chunk
            root_path = f"{bucket_name}/{object_key}/{start_date.year}"
            upload_to_gcs(df,root_path)
            print("Uploaded to GCS successfully")
            #update date range
            start_chunk_date, end_chunk_date = next(update_date_range(start_date, end_date, chunk_size_minutes))

            print(f"inserted another chunk")
        except StopIteration:
            # if StopIteration is raised, break from loop
            break
    
@data_exporter
def output():
    parquets_to_gcs()