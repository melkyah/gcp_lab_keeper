# Copyright 2018 GCP Lab Keeper authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

provider "google" {
  credentials = "${local.credentials_file_path}"
  project     = "${local.project_id}"
}

terraform {
  required_version = ">= 0.10.0"

  backend "gcs" {
    bucket      = "tf-remote-state-test"
    prefix      = "Terraform/state/GCP_lab_keeper"
    credentials = "../../../credentials.json"
  }
}


locals {
  project_id            = "prod-host-4f86"
  credentials_file_path = "../../../credentials.json"
  timezone              = "America/Buenos_Aires"
}

# Implement function modules

module "gcp_lab_keeper" {
  source = "../terraform_modules/functions"

  project_id               = "${local.project_id}"
  enable_stop_gce_instance = true
  wanted_zone_prefixes     = ["us"]
  cron_schedule_string     = "*/2 * * * *"
  scheduler_timezone       = "${local.timezone}"
  scheduler_region         = "us-west2"
  region                   = "us-central1"
}
