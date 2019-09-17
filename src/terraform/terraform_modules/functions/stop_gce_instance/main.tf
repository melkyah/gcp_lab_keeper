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

locals {
  service_list = [
    "pubsub.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudscheduler.googleapis.com",
    "appengine.googleapis.com"
  ]
}


# Enable services

resource "google_project_service" "resource_manager" {
  project = "${var.project_id}"
  service = "cloudresourcemanager.googleapis.com"

  disable_dependent_services = true
}

resource "google_project_service" "services" {
  count      = "${length(local.service_list)}"
  depends_on = ["google_project_service.resource_manager"]

  project = "${var.project_id}"
  service = "${element(local.service_list, count.index)}"

  disable_dependent_services = true
}

# Function templates.
data "template_file" "stop_gce_instance" {
  template = "${file("${path.module}/template/main.py.tpl")}"
  vars = {
    project_id           = "${var.project_id}"
    wanted_zone_prefixes = "${join(", ", var.wanted_zone_prefixes)}"
  }
}

# Creates a Zip file from the function files and uploads it to the bucket.
data "archive_file" "function" {
  count = "${var.enable_stop_gce_instance ? 1 : 0}"

  type        = "zip"
  output_path = "${path.module}/files/function.zip"

  source {
    content  = "${data.template_file.stop_gce_instance.rendered}"
    filename = "main.py"
  }

  source {
    content  = "${file("${path.module}/template/requirements.txt")}"
    filename = "requirements.txt"
  }
}

resource "google_storage_bucket_object" "function" {
  count = "${var.enable_stop_gce_instance ? 1 : 0}"

  name   = "stop_gce_instance/function.zip"
  source = "${data.archive_file.function.0.output_path}"
  bucket = "${var.storage_bucket}"
}

# Create a pub/sub topic to trigger the function

resource "google_pubsub_topic" "trigger_topic" {
  count      = "${var.enable_stop_gce_instance ? 1 : 0}"
  depends_on = ["google_project_service.services"]

  name    = "${var.trigger_topic_name}"
  project = "${var.project_id}"
}

# Deploy the cloud function using the uploaded files

resource "google_cloudfunctions_function" "main_function" {
  count      = "${var.enable_stop_gce_instance ? 1 : 0}"
  depends_on = ["google_project_service.services"]

  name        = "stop_gce_instance"
  description = "A function that stops GCE instances for given zones in the project"
  runtime     = "python37"
  region      = "${var.region}"

  available_memory_mb   = 128
  source_archive_bucket = "${var.storage_bucket}"
  source_archive_object = "${google_storage_bucket_object.function.0.name}"
  timeout               = 60
  entry_point           = "stop_gce_instances"

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "${google_pubsub_topic.trigger_topic.0.name}"
  }
}

# Schedule function run

resource "google_app_engine_application" "app" {
  count      = "${var.create_appengine_app ? 1 : 0}"
  depends_on = ["google_project_service.services"]

  project     = "${var.project_id}"
  location_id = "${var.scheduler_location_id}"
}

resource "google_cloud_scheduler_job" "function_run" {
  count      = "${var.enable_stop_gce_instance ? 1 : 0}"
  depends_on = ["google_project_service.services", "google_app_engine_application.app"]

  name        = "stop_gce_instance_schedule"
  description = "This schedule triggers the execution of stop_gce_instance function."
  region      = "${var.scheduler_region}"
  schedule    = "${var.cron_schedule_string}"
  time_zone   = "${var.scheduler_timezone}"

  pubsub_target {
    topic_name = "${google_pubsub_topic.trigger_topic.0.id}"
    data       = "${base64encode("Run")}"
  }
}
