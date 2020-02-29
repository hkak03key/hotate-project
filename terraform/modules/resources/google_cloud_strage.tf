
resource "google_storage_bucket" "gcf_code" {
  name     = "${var.project}-gcf-code"
  location = "us-west1"
}
