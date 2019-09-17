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

variable "project_id" {
  description = "Project in which to deploy the modules."
}

variable "storage_bucket_name" {
  description = "Name of the cloud storage bucket in which to sotre data."
  default     = "gcp-lab-keeper-data"
}

variable "storage_bucket_location" {
  description = "Location of the cloud storage bucket in which to sotre data."
  default     = "us-west1"
}

variable "storage_bucket_class" {
  description = "Class of the cloud storage bucket in which to sotre data."
  default     = "REGIONAL"
}

variable "region" {
  description = "region for function deployment."
  default     = "us-central1"
}

# Variables for stop_gce_instance_function

variable "enable_stop_gce_instance" {
  description = "Enables deployment of stop_gce_instance function."
  type        = bool
  default     = false
}

variable "wanted_zone_prefixes" {
  type        = "list"
  description = "List of zone prefixes in which to search for instances."
}

variable "trigger_topic_name" {
  description = "Name of the pub/sub topic that triggers the function."
  default     = "stop-gce-instance-topic"
}

variable "cron_schedule_string" {
  description = "String for schedule in unix cron format. Default runs daily at 8 PM."
  default     = "0 20 * * *"
}

variable "scheduler_timezone" {
  description = "Time zone for the scheduler."
  default     = "America/New_York"
}

variable "scheduler_region" {
  description = "region for function deployment."
  default     = "us-central1"
}