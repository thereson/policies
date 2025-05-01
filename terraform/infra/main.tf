provider "aws" {
  region = "eu-north-1"
}

terraform {
  backend "s3" {
    bucket = "thereson-pdk"
    key    = "eks/terraform.tfstate"
    region = "eu-north-1"
  }
}