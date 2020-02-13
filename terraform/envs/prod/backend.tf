terraform {
  backend "gcs" {
    bucket  = "hotate-terraform-backend"
    prefix  = "state"
  }
}


