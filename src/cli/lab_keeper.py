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

"""
    This module gets a list of instances running in a given GCP project and shuts them down.
"""

from pprint import pprint
import re

from googleapiclient import discovery

from lib.lab_keeper.config import Config
from lib.lab_keeper.authenticator import Authenticator


class LabKeeper:
    """This class manages GCP Compute Engine resources."""

    def __init__(self):
        """Initialize Lab Keeper parameters."""
        self.config = Config()
        self.authenticator = Authenticator()

        self.credentials = self.authenticator.make_credentials()

        self.service = discovery.build(
            'compute', 'v1', credentials=self.credentials)

        # List of Project IDs for this request.
        self.project_list = self.config.project_list

        # The list of the zone prefixes for this request.
        self.wanted_zone_prefixes = self.config.zone_prefixes

        # VM Label and value for shutdown flagging.
        self.label_key = self.config.label_key
        self.label_value = self.config.label_value


    def _request_instances(self, project, target_zones, label_key, label_value):
        """Make an API call to return all existing instances for a zone in a project."""
        instance_list = []
        pprint(f"Looking for instances in project {project}.")
        pprint(f"Looking for instances with label '{label_key}'='{label_value}'")

        for zone in target_zones:
            instance_request = self.service.instances().list(
                project=project, zone=zone, filter=f"labels.{label_key} = {label_value}")

            while instance_request is not None:
                response = instance_request.execute()

                if 'items' in response:
                    for instance in response['items']:

                        instance_list.append(instance)

                    instance_request = self.service.instances().list_next(
                        previous_request=instance_request, previous_response=response)
                    pprint(
                        f"{len(response['items'])} instances found in {zone}.")

                else:
                    pprint(f"No instances found in zone {zone}. Continuing...")
                    break

        pprint(f"{len(instance_list)} instances found in project {project}.")
        return instance_list

    def _request_zones(self, project):
        """Make an API call to return all available zones for a project."""
        zone_request = self.service.zones().list(project=project)
        while zone_request is not None:
            response = zone_request.execute()
            zone_list = []

            for zone in response['items']:
                # Puts all zone names inside a list.
                zone_list.append(zone.get('name', None))

            zone_request = self.service.zones().list_next(previous_request=zone_request,
                                                          previous_response=response)

            return zone_list

    def _filter_zones(self, wanted_zones_prefix, zone_list):
        """Filter unwanted zones from a zone list using a prefix."""
        target_zones = []

        for zone in zone_list:
            for prefix in wanted_zones_prefix:
                pattern = re.compile(f'^{prefix}')
                if pattern.match(zone):
                    target_zones.append(zone)

        return target_zones

    def _get_instances_bystatus(self, instance_list):
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
            pprint("######################")
            pprint(
                f"{status} instances:")
            pprint("######################")
            for instance in instances_bystatus[status]:
                pprint(f"{instance['name']} in {instance['zone']}")

        return instances_bystatus

    def stop_running_instances(self, instance_status_list, project):
        """Stop compute engine instances in RUNNING state."""
        # TODO: Check if instances in PROVISIONING, STAGING and REPAIRING
        #  states can and need to be stopped.

        if "RUNNING" in instance_status_list.keys():
            for running_instance in instance_status_list["RUNNING"]:
                instance = running_instance.get("name", None)
                zone = running_instance.get("zone", None)

                request = self.service.instances().stop(
                    project=project, zone=zone, instance=instance)
                pprint(f"Stopping instance {instance} in zone {zone}...")
                response = request.execute()
        else:
            pprint(f"There are no running instances in project {project}.")

        return

    def main(self):
        """Main"""
        # Get a list of zone names
        zone_list = self._request_zones(self.project_list[0])

        # Get only wanted zones
        target_zones = self._filter_zones(self.wanted_zone_prefixes, zone_list)

        # Get a list of instances for each target by project
        instances_list_projects = {}
        for project in self.project_list:
            instances = self._request_instances(
                project, target_zones, self.label_key, self.label_value)
            instances_list_projects[project] = instances

        # Create a list of instances by status by project
        instance_status_list_projects = {}
        for project in instances_list_projects:
            instance_status_list = self._get_instances_bystatus(instances_list_projects[project])
            instance_status_list_projects[project] = instance_status_list

        # Stop running VMs
        for project in instance_status_list_projects:
            self.stop_running_instances(instance_status_list_projects[project], project)

        return


if __name__ == '__main__':
    # Create a Lab Keeper instance, and run it.
    lk = LabKeeper()
    lk.main()
