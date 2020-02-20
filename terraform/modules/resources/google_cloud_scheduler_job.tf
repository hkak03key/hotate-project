
resource "google_cloud_scheduler_job" "job" {
  name             = "hello-world"
  description      = "hello-world"
  schedule         = "0 */12 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "60s"

  http_target {
    http_method = "GET"
    uri         = "https://${var.region}-${var.project}.cloudfunctions.net/hello_world"

    oidc_token {
      service_account_email = google_service_account.gcf_hello_world_invoker.email
    }
  }

  depends_on = [
    google_project_service.project_service["cloudscheduler.googleapis.com"],
    google_app_engine_application.app,
  ]
}

resource "google_service_account" "gcf_hello_world_invoker" {
  account_id   = "gcf-hello-world-invoker"
  display_name = "gcf-hello-world-invoker"

  depends_on = [
    google_project_service.project_service["iam.googleapis.com"],
  ]
}

resource "google_project_iam_member" "gcf_hello_world_invoker" {
  project = var.project
  role    = "roles/cloudfunctions.invoker" #"roles/editor"
  member  = "serviceAccount:${google_service_account.gcf_hello_world_invoker.email}"
}
