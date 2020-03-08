locals {
  project_id = jsondecode(file("gcp_service_key.json")).project_id
  region     = "asia-northeast1"
}

provider "google" {
  project     = local.project_id
  region      = local.region
  credentials = "gcp_service_key.json"
}

provider "google-beta" {
  project     = local.project_id
  region      = local.region
  credentials = "gcp_service_key.json"
}

provider "archive" {}
