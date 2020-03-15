

resource "google_secret_manager_secret_iam_binding" "LINE" {
  provider  = google-beta
  project   = local.project_id
  secret_id = "LINE"
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${local.project_id}@appspot.gserviceaccount.com",
  ]

  depends_on = [
    google_project_service.project_services,
  ]
}

resource "google_secret_manager_secret_iam_binding" "twitter" {
  provider  = google-beta
  project   = local.project_id
  secret_id = "twitter"
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${local.project_id}@appspot.gserviceaccount.com",
  ]

  depends_on = [
    google_project_service.project_services,
  ]
}
