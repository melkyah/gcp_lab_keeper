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
Client for accessing Instance Manager Server.
"""

import json
import grpc
import instance_manager_pb2
import instance_manager_pb2_grpc

from lib.lab_keeper.config import Config


class InstanceManagerClient:
    """Client for accessing Instance Manager Server."""

    def __init__(self):
        """Initializes client configuration."""
        self.config = Config()

        self.host = self.config.instance_manager_server
        self.port = self.config.instance_manager_port

        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

        self.stub = instance_manager_pb2_grpc.InstanceManagerStub(self.channel)

    def _load_credentials(self, path):
        """Loads account credentials from json file in path."""

        with open(path) as json_data:
            credentials = json.load(json_data)
            json_data.close()

        return json.dumps(credentials)

    def stop_instances(self, project, zones_prefixes, credentials_path):
        """Client function to call the rpc for stop_instances."""

        credentials = self._load_credentials(credentials_path)

        stop_instances_message = instance_manager_pb2.StopInstanceRequest(
            credentials=instance_manager_pb2.Credentials(credentials=credentials),
            project=instance_manager_pb2.Project(project_id=project),
            zones=instance_manager_pb2.ZonePrefixes(prefixes=zones_prefixes)
        )

        return self.stub.StopInstances(stop_instances_message)
