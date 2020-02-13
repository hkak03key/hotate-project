terraform {
  backend "gcs" {
    bucket      = "hotate-terraform-backend"
    credentials = "gcp_service_key.json"
  }
}


