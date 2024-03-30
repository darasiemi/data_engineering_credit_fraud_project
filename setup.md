## Overview
In this project, we show the data engineering pipeline, from data ingestion using . This project is a capstone for the fulfilment of the data engineering zoomcamp[link]. The dataset for this project can be found [here](https://www.kaggle.com/datasets/ealaxi/paysim1/data)
 
### Pre-Requisites
1. Terraform client installation: https://www.terraform.io/downloads
2. Cloud Provider account: https://console.cloud.google.com/
3. Download the dataset [here](https://www.kaggle.com/datasets/ealaxi/paysim1/data). This can be downloaded locally or by API. For this project, the former was explored for this project.
   
## Table of Contents
- [Infrasctuture Provisioning](#terraform)
- [Streamlined Data Ingestion](#ingestion)
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
