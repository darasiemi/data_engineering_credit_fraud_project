variable "credentials" {
  description = "My Credentials"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project"
  default     = "data-engr-zoomcamp-dara"
}

variable "region" {
  description = "Region"
  default     = "eu"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "project_dataset"

}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "dara-project-bucket"

}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"

}