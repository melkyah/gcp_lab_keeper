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
    default = "GCP_lab_keeper_data"
}

variable "storage_bucket_location" {
    description = "Location of the cloud storage bucket in which to sotre data."
    default = "US"
}

variable "storage_bucket_class" {
    description = "Class of the cloud storage bucket in which to sotre data."
    default = "Regional"
}