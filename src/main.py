# Copyright 2018 GCP Instance Watcher authors.
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

from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

CREDENTIALS = GoogleCredentials.get_application_default()

SERVICE = discovery.build('compute', 'v1', credentials=CREDENTIALS)

# Project ID for this request.
PROJECT = 'prod-host-4f86'  # TODO: Update placeholder value.

# The name of the zone for this request.
ZONE = 'us-west1-b'  # TODO: Update placeholder value.

REQUEST = SERVICE.instances().list(project=PROJECT, zone=ZONE)
while REQUEST is not None:
    RESPONSE = REQUEST.execute()

    for instance in RESPONSE['items']:
        # TODO: Change code below to process each `instance` resource:
        pprint(instance)

    REQUEST = SERVICE.instances().list_next(previous_request=REQUEST, previous_response=RESPONSE)
