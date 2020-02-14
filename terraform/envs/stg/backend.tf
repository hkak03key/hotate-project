terraform {
  backend "gcs" {
    bucket      = "hotate-stg-terraform-backend"
    credentials = "gcp_service_key.json"
  }
}


