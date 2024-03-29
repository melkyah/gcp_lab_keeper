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

from pprint import pprint
import re

from googleapiclient import discovery

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# TODO: Manage credentials using service account

CREDENTIALS = GoogleCredentials.get_application_default()

SERVICE = discovery.build('compute', 'v1', credentials=CREDENTIALS)

# Project ID for this request.
PROJECT = 'prod-host-4f86'  # TODO: Make this an input parameter.

# The list of the zone prefixes for this request.
WANTED_ZONES_PREFIXES = ['us']  # TODO: Make this an input parameter.


def stop_gce_instances(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """
    import base64

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'

    # Get a list of zone names
    zone_list = _request_zones(PROJECT)

    # Get only wanted zones
    target_zones = _filter_zones(WANTED_ZONES_PREFIXES, zone_list)

    # Get a list of instances for each target zone
    instances_list = _request_instances(PROJECT, target_zones)

    # Create a list of instances by status
    instance_status_list = _get_instances_bystatus(instances_list)

    # Stop running VMs
    _stop_running_instances(instance_status_list, PROJECT)


def _request_instances(project, target_zones):
    """Make an API call to return all existing instances for a zone in a project."""
    instance_list = []
    pprint(f"Looking for instances in project {project}.")

    for zone in target_zones:
        instance_request = SERVICE.instances().list(project=project, zone=zone)

        while instance_request is not None:
            response = instance_request.execute()

            if 'items' in response:
                for instance in response['items']:

                    instance_list.append(instance)

                instance_request = SERVICE.instances().list_next(previous_request=instance_request,
                                                                 previous_response=response)
                pprint(f"{len(response['items'])} instances found in {zone}.")

            else:
                pprint(f"No instances found in zone {zone}. Continuing...")
                break

    pprint(f"{len(instance_list)} instances found in project {project}.")
    return instance_list


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


def _get_instances_bystatus(instance_list):
    """Take an instance object list and return a dictionary with
        statuses as keys and a list of instances as its values."""

    instances_bystatus = {}
    pprint(f"Checking status for {len(instance_list)} instances.")

    # Create a list of returned statuses
    status_list = []
    for instance in instance_list:
        if instance.get("status", None) not in status_list:
            status_list.append(instance.get("status", None))

    # Create a dictionary containing instances and zone by status
    for key in status_list:
        value = []
        for instance in instance_list:
            if instance.get("status", None) == key:
                instance_data = {}
                instance_name = instance.get("name", None)
                zone_name = instance.get("zone", None).split('/')[-1]
                instance_data["name"] = instance_name
                instance_data["zone"] = zone_name
                value.append(instance_data)

        instances_bystatus[key] = value

    # Print formatted contents of dictionary
    for status in instances_bystatus:
        pprint(
            f"{status} instances: {', '.join(map(str, instances_bystatus[status]))}")

    return instances_bystatus


def _stop_running_instances(instance_status_list, project):
    """Stop compute engine instances in RUNNING state."""
    # TODO: Check if instances in PROVISIONING, STAGING and REPAIRING
    #  states can and need to be stopped.

    if "RUNNING" in instance_status_list.keys():
        for running_instance in instance_status_list["RUNNING"]:
            instance = running_instance.get("name", None)
            zone = running_instance.get("zone", None)

            request = SERVICE.instances().stop(project=project, zone=zone, instance=instance)
            pprint(f"Stopping instance {instance} in zone {zone}...")
            response = request.execute()
    else:
        pprint(f"There are no running instances in project {project}.")

    return
