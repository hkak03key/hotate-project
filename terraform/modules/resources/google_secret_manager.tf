

resource "google_secret_manager_secret_iam_binding" "LINE" {
  provider  = google-beta
  project   = var.project
  secret_id = "LINE"
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${var.project}@appspot.gserviceaccount.com",
  ]
}

resource "google_secret_manager_secret_iam_binding" "twitter" {
  provider  = google-beta
  project   = var.project
  secret_id = "twitter"
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${var.project}@appspot.gserviceaccount.com",
  ]
}
