```bash
To copy files from local file to gcs
$ gsutil cp sparl_gcs_to_bigquery/spark_bigquery.py gs://dara-project-bucket/code/

$ gcloud dataproc jobs submit pyspark \
     --cluster=project-cluster \
     --region=europe-west4 \
     gs://dara-project-bucket/code/spark_bigquery.py \
     -- \
     --input_credit 'gs://dara-project-bucket/credit_fraud_parquet/2020/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2021/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2022/*' \
     'gs://dara-project-bucket/credit_fraud_parquet/2023/*' \
     --output=project_dataset.credit_fraud_bigquery_table


$ gcloud compute networks subnets update default --region=europe-west4 --enable-private-ip-google-access
