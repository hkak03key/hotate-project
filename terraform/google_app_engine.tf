
resource "google_app_engine_application" "app" {
  project     = local.project_id
  location_id = local.region

  depends_on = [
    google_project_service.project_services,
  ]
}
