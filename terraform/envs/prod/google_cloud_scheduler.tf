
resource "google_cloud_scheduler_job" "job" {
  name             = "today_attendance"
  description      = "today_attendance"
  schedule         = "0 17 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "120s"

  http_target {
    http_method = "POST"
    uri         = "https://${local.region}-${data.google_project.project.name}.cloudfunctions.net/today_attendance"

    oidc_token {
      service_account_email = "${data.google_project.project.name}@appspot.gserviceaccount.com"
    }
  }

  depends_on = [
    module.resources,
  ]
}

