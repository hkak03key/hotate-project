provider "google" {
  project     = "hotate-project-stg"
  region      = "asia-northeast1"
  credentials = "gcp_service_key.json"
}

provider "google-beta" {
  project     = "hotate-project-stg"
  region      = "asia-northeast1"
  credentials = "gcp_service_key.json"
}

provider "archive" {}
