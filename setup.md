## Overview
In this project, we show the data engineering pipeline, from data ingestion using . This project is a capstone for the fulfilment of the data engineering zoomcamp[link]. The dataset for this project can be found [here](https://www.kaggle.com/datasets/ealaxi/paysim1/data)
 
### Pre-Requisites
1. Terraform client installation: https://www.terraform.io/downloads
2. Cloud Provider account: https://console.cloud.google.com/
3. Download the dataset [here](https://www.kaggle.com/datasets/ealaxi/paysim1/data). This can be downloaded locally or by API. For this project, the former was explored for this project.
   
## Table of Contents
- [Infrasctuture Provisioning](#infrastructure)
- [Ingestion](#ingestion)
- [Automated Data Orchestration](#orchestration)
- [Data Warehousing and Visualization](#orchestration)

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
    * Removes your stack from the Cloud

#### Ingestion
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

You can then create a project on Mage and the code in `mage_etl/load_credit_fraud_gcs.py` can be copied to a data exporter. The ETL process is setup to be done in just a single block of this data expoter. Since mage is configured to `/home/src`, we will download our dataset to this directory. In addition, the credential that allows us to write to GCS, will also be under the directory `/home/src/keys/`. The credentials can also be configured in the `io_.yaml` file.
