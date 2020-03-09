terraform {
  backend "gcs" {
    prefix      = "tfstate"
    credentials = "gcp_service_key.json"
  }
}


