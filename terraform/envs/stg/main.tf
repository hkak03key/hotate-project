data "google_project" "project" {
}

locals {
  region = "asia-northeast1"
}

module "resources" {
  source  = "../../modules/resources"
  project = data.google_project.project.name
  region  = local.region
}
