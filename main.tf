provider "aws" {
	region= "us-east-1"

}
terraform {
  backend "s3"{
	bucket = "thereson-pdk"
	key = "states/terraform.tf"
	region = "eu-north-1"
}
}


