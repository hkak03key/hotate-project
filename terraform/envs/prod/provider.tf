provider "google" {
  credentials = "${file("gcp-service-key.json")}"
  project     = "hotate-project"
  region      = "asia-northeast1"
}
