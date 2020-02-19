
resource "google_app_engine_application" "app" {
  project     = var.project
  location_id = var.region
}
