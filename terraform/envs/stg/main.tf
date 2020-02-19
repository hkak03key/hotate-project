data "google_project" "project" {
}

module "resources" {
  source  = "../../modules/resources"
  project = data.google_project.project.name
  region  = "asia-northeast1"
}
