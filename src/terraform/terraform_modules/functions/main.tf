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

# This module deploys a cloud function that stops VM instances 
#    on a schedules basis.

# This module deploys desired GCP Lab Keeper functions to a given project.

provider "archive" {}

resource "google_storage_bucket" "code_store" {
  name    = "${var.storage_bucket_name}"
  project = "${var.project_id}"

  storage_class = "${var.storage_bucket_class}"
  location      = "${var.storage_bucket_location}"
}

# If enable_stop_gce_instance = True, deploy stop_gce_instance
module "stop_gce_instance" {
  source = "./stop_gce_instance"

  enable_stop_gce_instance = "${var.enable_stop_gce_instance}"
  project_id               = "${var.project_id}"
  wanted_zone_prefixes     = "${var.wanted_zone_prefixes}"
  storage_bucket           = "${google_storage_bucket.code_store.name}"
  trigger_topic_name       = "${var.trigger_topic_name}"
  region                   = "${var.region}"
  scheduler_timezone       = "${var.scheduler_timezone}"
  scheduler_region         = "${var.scheduler_region}"
  scheduler_location_id    = "${var.scheduler_location_id}"
  cron_schedule_string     = "${var.cron_schedule_string}"
  create_appengine_app     = "${var.create_appengine_app}"
}
