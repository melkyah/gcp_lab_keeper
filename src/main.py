"""This module gets a list of instances running in a given GCP project and shuts them down."""

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
import re

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

CREDENTIALS = GoogleCredentials.get_application_default()

SERVICE = discovery.build('compute', 'v1', credentials=CREDENTIALS)

# Project ID for this request.
PROJECT = 'prod-host-4f86'  # TODO: Make this an input parameter.

# The list of the zone prefixes for this request.
WANTED_ZONES_PREFIXES = ['us']  # TODO: Make this an input parameter.

def request_instances(project, zone):
    """Make an API call to return all existing instances for a zone in a project."""

    instance_request = SERVICE.instances().list(project=project, zone=zone)

    while instance_request is not None:
        response = instance_request.execute()

        if 'items' in response:
            for instance in response['items']:
                # TODO: Change code below to process each `instance` resource:

                pprint(instance)

            instance_request = SERVICE.instances().list_next(previous_request=instance_request,
                                                             previous_response=response)
        return # TODO: This function still doesn't return anything

def request_zones(project):
    """Make an API call to return all available zones for a project."""
    zone_request = SERVICE.zones().list(project=project)
    while zone_request is not None:
        response = zone_request.execute()
        zone_list = []
        for zone in response['items']:
            # Puts all zone names inside a list.
            zone_list.append(zone.get('name', None))

        zone_request = SERVICE.zones().list_next(previous_request=zone_request,
                                                 previous_response=response)

        return zone_list

def filter_zones(wanted_zones_prefix, zone_list):
    """Filter unwanted zones from a zone list using a prefix."""
    target_zones = []

    for zone in zone_list:
        for prefix in wanted_zones_prefix:
            pattern = re.compile(f'^{prefix}')
            if pattern.match(zone):
                target_zones.append(zone)

    return target_zones

# Get a list of zone names
ZONE_LIST = request_zones(PROJECT)

# Get only wanted zones
TARGET_ZONES = filter_zones(WANTED_ZONES_PREFIXES, ZONE_LIST)

# Get a list of instances for each target zone
for zone in TARGET_ZONES:
    request_instances(PROJECT, zone)
