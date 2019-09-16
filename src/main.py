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

"""
    This module gets a list of instances running in a given GCP project and shuts them down.
"""

from pprint import pprint
import re

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# TODO: Manage credentials using service account

CREDENTIALS = GoogleCredentials.get_application_default()

SERVICE = discovery.build('compute', 'v1', credentials=CREDENTIALS)

# Project ID for this request.
PROJECT = 'prod-host-4f86'  # TODO: Make this an input parameter.

# The list of the zone prefixes for this request.
WANTED_ZONES_PREFIXES = ['us']  # TODO: Make this an input parameter.

def request_instances(project, target_zones):
    """Make an API call to return all existing instances for a zone in a project."""
    instance_list = []
    pprint(f"Looking for instances in project {project}.")

    for zone in target_zones:
        instance_request = SERVICE.instances().list(project=project, zone=zone)

        while instance_request is not None:
            response = instance_request.execute()

            if 'items' in response:
                for instance in response['items']:
                    # TODO: Change code below to process each `instance` resource:

                    instance_list.append(instance)

                instance_request = SERVICE.instances().list_next(previous_request=instance_request,
                                                                 previous_response=response)
                pprint(f"{len(response['items'])} instances found in {zone}.")

            else:
                pprint(f"No instances in {zone}. Continuing...")
                break

    pprint(f"{len(instance_list)} instances found in project {project}.")
    return instance_list # TODO: This function still doesn't return anything

def _request_zones(project):
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

def _filter_zones(wanted_zones_prefix, zone_list):
    """Filter unwanted zones from a zone list using a prefix."""
    target_zones = []

    for zone in zone_list:
        for prefix in wanted_zones_prefix:
            pattern = re.compile(f'^{prefix}')
            if pattern.match(zone):
                target_zones.append(zone)

    return target_zones

def get_instances_bystatus(instance_list):
    """Take an instance object list and return a dictionary with
        statuses as keys and a list of instances as its values."""

    instances_bystatus = {}
    pprint(f"Checking status for {len(instance_list)} instances.")

    # Create a list of returned statuses
    status_list = []
    for instance in instance_list:
        if instance.get("status", None) not in status_list:
            status_list.append(instance.get("status", None))

    # Create a dictionary containing instances by status
    for key in status_list:
        value = []
        for instance in instance_list:
            if instance.get("status", None) == key:
                value.append(instance.get("name", None))

        instances_bystatus[key] = value

    # Print formatted contents of dictionary
    for status in instances_bystatus:
        pprint(f"{status} instances: {', '.join(map(str, instances_bystatus[status]))}")



def main():
    """Main"""
    # Get a list of zone names
    zone_list = _request_zones(PROJECT)

    # Get only wanted zones
    target_zones = _filter_zones(WANTED_ZONES_PREFIXES, zone_list)

    # Get a list of instances for each target zone
    instances_list = request_instances(PROJECT, target_zones)

    # Create a list of instances by status
    get_instances_bystatus(instances_list)

    return

if __name__ == '__main__':
    main()
