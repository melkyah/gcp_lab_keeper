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

# Function templates
data "template_file" "stop_gce_instance" {
  template = "${file("${path.module}/template/main.py.tpl")}"
  vars = {
    project_id = "${var.project_id}"
    wanted_zone_prefixes = "${var.wanted_zone_prefixes}"
  }
}

resource "google_storage_bucket_object" "stop_gce_instance" {
  name   = "stop_gce_instance/main.py"
  source = "${data.template_file.stop_gce_instance.rendered}"
  bucket = "${var.storage_bucket}"
}

resource "google_storage_bucket_object" "requirements" {
  name   = "stop_gce_instance/requirements.txt"
  source = "${file("${path.module}/template/requirements.txt")}"
  bucket = "${var.storage_bucket}"
}

resource "google_pubsub_topic" "trigger_topic" {
  name = "${var.trigger_topic_name}"
  project = "${var.project_id}"
  labels = {
    app = "GCP_lab_keeper"
  }
}

resource "google_cloudfunctions_function" "main_function" {
  name                  = "stop_gce_instance"
  description           = "A function that stops GCE instances for given zones in the project"
  runtime               = "python37"

  available_memory_mb   = 128
  source_archive_bucket = "${var.storage_bucket}"
  source_archive_object = "${google_storage_bucket_object.stop_gce_instance.self_link}"
  timeout               = 60
  entry_point           = "stop_gce_instances"
  labels = {
    app = "GCP_lab_keeper"
  }
  event_trigger = {
      event_type = "google.pubsub.topic.publish"
      resource = "${google_pubsub_topic.trigger_topic.name}"
  }
}