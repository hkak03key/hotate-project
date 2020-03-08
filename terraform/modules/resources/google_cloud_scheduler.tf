
resource "google_cloud_scheduler_job" "call_gcf_today_attendance" {
  # 本番環境のみschedulerを作成
  for_each = { for v in(var.project == "hotate-project" ? ["call_gcf_today_attendance"] : []) :
    v => v
  }
  name             = each.key
  description      = "call gcf today_attendance"
  schedule         = "0 17 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "120s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.today_attendance.https_trigger_url

    oidc_token {
      service_account_email = "${var.project}@appspot.gserviceaccount.com"
    }
  }

  depends_on = [
    google_project_service.project_service["cloudscheduler.googleapis.com"],
  ]
}

resource "google_cloud_scheduler_job" "call_gcf_schedule_update_info" {
  # 本番環境のみschedulerを作成
  for_each = { for v in(var.project == "hotate-project" ? ["call_gcf_schedule_update_info"] : []) :
    v => v
  }
  name             = each.key
  description      = "call gcf schedule_update_info"
  schedule         = "30 08-23/7 * * *"
  time_zone        = "Asia/Tokyo"
  attempt_deadline = "180s"

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.schedule_update_info.https_trigger_url

    oidc_token {
      service_account_email = "${var.project}@appspot.gserviceaccount.com"
    }
  }

  depends_on = [
    google_project_service.project_service["cloudscheduler.googleapis.com"],
  ]
}

