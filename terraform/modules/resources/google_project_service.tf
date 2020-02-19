
resource "google_project_service" "project_service" {
  for_each = { for v in local.services :
    v => v
  }
  project                    = var.project
  service                    = each.value
  disable_dependent_services = true
}

locals {
  services = [
    "iam.googleapis.com",
    "cloudscheduler.googleapis.com",
  ]
}

