
resource "google_cloud_scheduler_job" "job" {
  name             = "hello-world"
  description      = "hello-world"
  schedule         = "0 */12 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "60s"

  http_target {
    http_method = "GET"
    uri         = "https://cloudscheduler.googleapis.com/v1/projects/${var.project}/locations/${var.region}/jobs"

    oauth_token {
      service_account_email = google_service_account.gcf_hello_world_invoker.email
    }
  }
}

resource "google_service_account" "gcf_hello_world_invoker" {
  account_id = "gcf-hello-world-invoker"
}

