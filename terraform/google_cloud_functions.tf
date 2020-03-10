
###################################################
# script upload to gcs
locals {
  cloud_functions = [
    "post_sns",
    "schedule_update_info",
    "today_attendance",
  ]
}

data "archive_file" "gcf_code" {
  for_each = { for v in local.cloud_functions :
    v => v
  }
  type        = "zip"
  source_dir  = "../google_cloud_functions/${each.value}"
  output_path = ".workspace/${each.value}.zip"
}

resource "google_storage_bucket_object" "gcf_code" {
  for_each = { for v in data.archive_file.gcf_code :
    basename(v.output_path) => v
  }
  name   = "gcf/${each.key}/${each.value.output_md5}.zip"
  bucket = local.tf_bucket
  source = each.value.output_path
}

###################################################
# each function
#
#-----------------------------------------
# post_sns
resource "google_cloudfunctions_function" "post_sns" {
  name        = "post_sns"
  description = "post_sns"
  runtime     = "python37"

  available_memory_mb   = 128
  service_account_email = "${local.project_id}@appspot.gserviceaccount.com"
  source_archive_bucket = google_storage_bucket_object.gcf_code["post_sns.zip"].bucket
  source_archive_object = google_storage_bucket_object.gcf_code["post_sns.zip"].name
  trigger_http          = true
  entry_point           = "main"
}

resource "google_cloudfunctions_function_iam_binding" "post_sns" {
  project        = google_cloudfunctions_function.post_sns.project
  region         = google_cloudfunctions_function.post_sns.region
  cloud_function = google_cloudfunctions_function.post_sns.name

  role = "roles/cloudfunctions.invoker"
  members = [
    "serviceAccount:${local.project_id}@appspot.gserviceaccount.com",
  ]
}

#-------------------------------------------------------------
# schedule_update_info
resource "google_cloudfunctions_function" "schedule_update_info" {
  name        = "schedule_update_info"
  description = "schedule_update_info"
  runtime     = "python37"

  available_memory_mb   = 128
  service_account_email = "${local.project_id}@appspot.gserviceaccount.com"
  source_archive_bucket = google_storage_bucket_object.gcf_code["schedule_update_info.zip"].bucket
  source_archive_object = google_storage_bucket_object.gcf_code["schedule_update_info.zip"].name
  trigger_http          = true
  entry_point           = "main"
}

resource "google_cloudfunctions_function_iam_binding" "schedule_update_info" {
  project        = google_cloudfunctions_function.schedule_update_info.project
  region         = google_cloudfunctions_function.schedule_update_info.region
  cloud_function = google_cloudfunctions_function.schedule_update_info.name

  role = "roles/cloudfunctions.invoker"
  members = [
    "serviceAccount:${local.project_id}@appspot.gserviceaccount.com",
  ]
}

#-------------------------------------------------------------
# today_attendance
resource "google_cloudfunctions_function" "today_attendance" {
  name        = "today_attendance"
  description = "today_attendance"
  runtime     = "python37"

  available_memory_mb   = 256
  service_account_email = "${local.project_id}@appspot.gserviceaccount.com"
  source_archive_bucket = google_storage_bucket_object.gcf_code["today_attendance.zip"].bucket
  source_archive_object = google_storage_bucket_object.gcf_code["today_attendance.zip"].name
  trigger_http          = true
  entry_point           = "main"
}

resource "google_cloudfunctions_function_iam_binding" "today_attendance" {
  project        = google_cloudfunctions_function.today_attendance.project
  region         = google_cloudfunctions_function.today_attendance.region
  cloud_function = google_cloudfunctions_function.today_attendance.name

  role = "roles/cloudfunctions.invoker"
  members = [
    "serviceAccount:${local.project_id}@appspot.gserviceaccount.com",
  ]
}

