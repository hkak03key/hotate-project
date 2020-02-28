
resource "google_cloud_scheduler_job" "call_gcf_today_attendance" {
  name             = "call_gcf_today_attendance"
  description      = "call_gcf today_attendance"
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

resource "google_cloud_scheduler_job" "call_gcf_schedule_update_info" {
  name             = "call_gcf_schedule_update_info"
  description      = "gall gcf schedule_update_info"
  schedule         = "30 08-23/7 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "180s"

  http_target {
    http_method = "POST"
    uri         = "https://${local.region}-${data.google_project.project.name}.cloudfunctions.net/schedule_update_info"

    oidc_token {
      service_account_email = "${data.google_project.project.name}@appspot.gserviceaccount.com"
    }
  }

  depends_on = [
    module.resources,
  ]
}

