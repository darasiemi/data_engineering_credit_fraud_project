## Overview
In this project, we show the data engineering pipeline, from data ingestion using . This project is a capstone for the fulfilment of the data engineering zoomcamp[link].
 
### Pre-Requisites
1. Terraform client installation: https://www.terraform.io/downloads
2. Cloud Provider account: https://console.cloud.google.com/
   
## Table of Contents
- [Infrasctuture Provisioning](#terraform)
- [Streamlined Data Ingestion](#ingestion)
- [Automated Data Orchestration](#orchestration)
- [Data Warehousing and Visualization](#orchestration)

First step is to clone the directory
 ```bash
  git clone 
```

#### Infrasctuture Provisioning
Terraform is used for infrastructure provisioning in this project.
First, you go to the 
1. `terraform init`: 
    * Initializes & configures the backend, installs plugins/providers, & checks out an existing configuration from a version control 
2. `terraform plan`:
    * Matches/previews local changes against a remote state, and proposes an Execution Plan.
3. `terraform apply`: 
    * Asks for approval to the proposed plan, and applies changes to cloud
4. `terraform destroy`
    * Removes your stack from the Cloud
