To copy files from local file to gcs
```bash
$ gsutil cp sparl_gcs_to_bigquery/spark_bigquery.py gs://dara-project-bucket/code/
```
To submit dataproc jobs to run spark on cloud
```bash
$ gcloud dataproc jobs submit pyspark \
     --cluster=project-cluster \
     --region=europe-west4 \
     gs://dara-project-bucket/code/spark_bigquery.py \
     -- \
     --input_credit 'gs://dara-project-bucket/credit_fraud_parquet/2010/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2011/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2012/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2013/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2014/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2015/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2016/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2017/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2018/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2019/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2020/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2021/*' \
     --output=project_dataset.credit_fraud_bigquery_table
```
To enable private ip google access
```bash 
$ gcloud compute networks subnets update default --region=europe-west4 --enable-private-ip-google-access
```
