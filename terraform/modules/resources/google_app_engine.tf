
resource "google_app_engine_application" "app" {
  project     = var.project
  location_id = var.region

  depends_on = [
    google_project_service.project_service["appengine.googleapis.com"],
  ]
}
