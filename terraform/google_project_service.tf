
resource "google_project_service" "project_service" {
  for_each = { for v in local.services :
    v => v
  }
  project                    = local.project_id
  service                    = each.value
  disable_dependent_services = true
}

locals {
  services = [
    "appengine.googleapis.com",
    "calendar-json.googleapis.com",
    "cloudscheduler.googleapis.com",
    "iam.googleapis.com",
    "sheets.googleapis.com",
  ]
}
