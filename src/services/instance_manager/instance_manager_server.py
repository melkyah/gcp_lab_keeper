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
This module manages Google Cloud Compute Engine Instances.
"""
import re
import time
import hashlib
from pprint import pprint
from concurrent import futures
from googleapiclient import discovery

import grpc
import instance_manager_pb2
import instance_manager_pb2_grpc

from lib.lab_keeper.config import Config
from lib.lab_keeper.authenticator import Authenticator


class InstanceManagerServicer(instance_manager_pb2_grpc.InstanceManagerServicer):
    """gRPC server for Instance Manager service."""

    def __init__(self, *args, **kwargs):
        self.server_port = 46001
        self.config = Config()
        self.authenticator = Authenticator()

        self.credentials = self.authenticator.make_credentials()

        self.service = discovery.build(
            'compute', 'v1', credentials=self.credentials)

    def StopInstances(self, request, context):
        """
        Implementation of the rpc StopInstances service.
        """

        target_project = request.project.project_id
        wanted_zones_prefixes = request.zones.prefixes
        zone_list = self._request_zones(target_project)
        target_zones = self._filter_zones(wanted_zones_prefixes, zone_list)
        instances_list = self._request_instances(target_project, target_zones)
        instance_status_list = self._get_instances_bystatus(instances_list)
        stopped_instances = self.stop_running_instances(
            instance_status_list, target_project)

        stopped_instances_list = []

        for instance in stopped_instances:
            instance_name = instance.get("name", None)
            instance_zone = instance.get("zone", None)

            stopped_instances_list.append(
                instance_manager_pb2.Instance(
                    name=instance_name,
                    zone=instance_zone
                )
            )

        result = instance_manager_pb2.InstanceList(
            instances=stopped_instances_list
        )

        return result

    def start_server(self):
        """
        Start the gRPC server, and prep
        it for serving incoming connections
        """
        instance_manager_server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10))
        instance_manager_pb2_grpc.add_InstanceManagerServicer_to_server(
            InstanceManagerServicer(), instance_manager_server)
        instance_manager_server.add_insecure_port(
            f'[::]:{self.server_port}')
        instance_manager_server.start()

        pprint("Instance Manager Server running...")

        try:
            while True:
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            instance_manager_server.stop(0)
            pprint("Instance Manager Server stopped...")

    def _request_instances(self, project, target_zones):
        """Make an API call to return all existing instances for a zone in a project."""
        instance_list = []
        pprint(f"Looking for instances in project {project}.")

        for zone in target_zones:
            instance_request = self.service.instances().list(project=project, zone=zone)

            while instance_request is not None:
                response = instance_request.execute()

                if 'items' in response:
                    for instance in response['items']:

                        instance_list.append(instance)

                    instance_request = self.service.instances().list_next(previous_request=instance_request,
                                                                          previous_response=response)
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
            pprint(
                f"{status} instances: {', '.join(map(str, instances_bystatus[status]))}")

        return instances_bystatus

    def stop_running_instances(self, instance_status_list, project):
        """Stop compute engine instances in RUNNING state."""
        # TODO: Check if instances in PROVISIONING, STAGING and REPAIRING
        #  states can and need to be stopped.

        stopped_instances = []

        if "RUNNING" in instance_status_list.keys():
            index = 0
            for running_instance in instance_status_list["RUNNING"]:
                instance = running_instance.get("name", None)
                zone = running_instance.get("zone", None)

                request = self.service.instances().stop(
                    project=project, zone=zone, instance=instance)
                pprint(f"Stopping instance {instance} in zone {zone}...")
                response = request.execute()

                stopped_instances.append(running_instance)
                index += 1

        else:
            pprint(f"There are no running instances in project {project}.")

        return stopped_instances


curr_server = InstanceManagerServicer()
curr_server.start_server()
