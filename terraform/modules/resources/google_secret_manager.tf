

resource "google_secret_manager_secret_iam_binding" "editor" {
  provider  = google-beta
  project   = var.project
  secret_id = "LINE"
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${var.project}@appspot.gserviceaccount.com",
  ]
}
