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

variable "project_id" {
    description = "Project in which to deploy the function."
}

variable "wanted_zone_prefixes" {
    type = "list"
    description = "List of zone prefixes in which to search for instances."
}

variable "trigger_topic_name" {
    description = "Name of the pub/sub topic that triggers the function."
    default = "stop_gce_instance_topic"
}

variable "storage_bucket" {
    description = "Cloud Storage Bucket in which to deploy function code."
}