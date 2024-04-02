## Overview
In this project, I show the data engineering pipeline, from data ingestion using . This project is a capstone for the fulfilment of the [data engineering zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp.git). The dataset for this project can be found [here](https://www.kaggle.com/datasets/ealaxi/paysim1/data). This is my first data engineering project and I am happy to pick up these tools.
 
### Pre-Requisites
1. Terraform client installation: https://www.terraform.io/downloads
2. Cloud Provider account: https://console.cloud.google.com/
3. Download the dataset [here](https://www.kaggle.com/datasets/ealaxi/paysim1/data). This can be downloaded locally or by API. For this project, the former was explored for this project.
   
## Table of Contents
- [Infrastructure Provisioning](#infrastructure-provisioning)
- [ETL Ingestion](#etl-ingestion)
- [Batch Processing](#batch-processing)
- [Visualization](#visualization)


First step is to clone the directory
 ```bash
  git clone https://github.com/peter716/data_engineering_credit_fraud_project.git
```
Go to the folder
 ```bash
  cd /path/from/your/computer/data_engineering_credit_fraud_project
```

#### Infrasctuture Provisioning
Terraform is used for infrastructure provisioning in this project.
To get this started, first, we go to the terraform directory
Go to the folder
 ```bash
  cd terraform_gcs
```
There are two files of interest `main.tf` and `variables.tf`. The `main.tf` is for provisiong the cloud infrastructure while the `variables.tf` is used to abstract the variables from the `main.tf`. We also need to create a service account in GCP, which has admin access to Cloud Storage. The key is then saved in the `terraform_gcs` directory and the path updated in the `variables.tf` file.

Thereafter, the following commands are run:
1. `terraform init`: 
    * Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control
2. `terraform fmt`: 
    * To format the *.tf files
3. `terraform plan`:
    * Matches/previews local changes against a remote state, and proposes an Execution Plan.
4. `terraform apply`: 
    * Asks for approval to the proposed plan, and applies changes to cloud
5. `terraform destroy`
    * Removes your stack from the Cloud. This should only be done when after the project is completed and there is no need 
    for the resources anymore. 

#### ETL Ingestion
To setup mage, you can clone the mage-ai directory 
```bash
git clone  https://github.com/mage-ai/mage-zoomcamp
```
Then go to the mage-zoomcamp folder `cd mage-zoomcamp`. 
Then run `cp dev.env .env`. 
Thereafter, run `docker compose build` to build the docker image that sets up docker container. 
Run `docker pull mageai/mageai:latest` to pull the latest mage image. 
Thereafter, run `docker compose up` to start the container. 
Mage is deployed on `localhost:6789`

You can then create a project on Mage and the code in `mage_etl/load_credit_fraud_gcs.py` can be copied to a data exporter python script. The ETL process is setup to be done in just a single block of this data expoter. Since mage is configured to `/home/src`, we will download our dataset to this directory (locally or by Kaggle API call). In addition, the credential that allows us to write to GCS, will also be under the directory `/home/src/keys/`. The credentials can also be configured in the `io_config.yaml` file.
It should be noted that the read is in CSV format. To make the data more lightweight for storage, the dataset is converted to parquets before transferring to cloud storage.

Some processing done during the ETL ingestion on Mage are:
- Data is read in batches of 100,000 records.
- A new `date` column is created in a date range format to substitute the existing `step` column. The frequency was measured per minute. The resulting `date` column is formatted as a string timestamp for subsequent transformations in Spark.
- Convert column names from camelCase to snake_case.

#### Batch Processing
The data for this project is loaded by batch processing. Spark is used for transformations and to create table in BigQuery.
The following transformations are done in Spark:
- Rename the `date` column to `tranc_date`
- Extract the month from the string time type, and create a new column `month`
- Convert the string time type to timestamp and name this as `tranc_timestamp`
- Drop the `date` column
- Partition the data to improve efficiency, query performance, and manageability 
- Sort the data in each partition by the `tranc_timestamp`, again to improve query performance.
- Generate a table which is written to bigquery

A Dataproc cluster is created in the same region as the GCS data and the bigquery table. A temporary bucket is created when the cluster is launched. This bucket should be updated in the `spark_bigquery.py` code. The service account should also have access to storage administration and dataprocs. 

For steps on how to move the driver code to GCS, and submiting the Dataproc Spark job, see [here](cloud.md)

Note that Partitioning was done in Spark. The data was partitioned into 50 and sorted within partitions. To add an extra layer of partioning, the table written to BigQuery can also be partioned to improve performance in using the query. This query creates or replaces a table with data that is partitioned based on the month extracted from the timestamp column.  
```sql
CREATE OR REPLACE TABLE data-engr-zoomcamp-dara.project_dataset.credit_fraud_bigquery_table_partitioned
PARTITION BY
  TIMESTAMP_TRUNC(tranc_timestamp, MONTH) AS
SELECT * FROM data-engr-zoomcamp-dara.project_dataset.credit_fraud_bigquery_table;
```

To query the table for the first 10 records which is ordered by timestamps, this query can be run
```sql
SELECT * FROM  data-engr-zoomcamp- 
   dara.project_dataset.credit_fraud_bigquery_table_partitioned
ORDER BY tranc_timestamp 
LIMIT 10;
```
#### Visualization
Looker Studio facilitates visualization for this project. A new report is created, utilizing the data from the BigQuery table for visualization purposes. To enhance clarity and relevance, certain style modifications and filters are applied to the visualization. You can access the finalized visualization [here](https://lookerstudio.google.com/reporting/5da912e1-8240-4d4c-a25c-d5f0b7454233)


