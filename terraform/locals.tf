locals {
  project_id = jsondecode(file("gcp_service_key.json")).project_id
  region     = "asia-northeast1"
  tf_bucket  = "${local.project_id}-terraform"
}

