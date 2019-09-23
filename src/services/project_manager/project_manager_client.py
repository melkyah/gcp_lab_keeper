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
Client for accessing Project Manager Server.
"""

import json
import grpc
import project_manager_pb2
import project_manager_pb2_grpc

from lib.lab_keeper.config import Config

class ProjectManagerClient:
    """Client for accessing Project Manager Server."""

    def __init__(self):
        """Initializes client configuration."""
        self.config = Config()

        self.host = self.config.project_manager_server
        self.port = self.config.project_manager_port

        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')

        self.stub = project_manager_pb2_grpc.ProjectManagerStub(self.channel)

    def _load_credentials(self, path):
        """Loads account credentials from json file in path."""

        with open(path) as json_data:
            credentials = json.load(json_data)
            json_data.close()

        return json.dumps(credentials)

    def get_projects(self, credentials_path):
        """Client function to call the rpc for get_projects."""

        credentials = self._load_credentials(credentials_path)

        get_projects_message = project_manager_pb2.GetProjectRequest(
            credentials=project_manager_pb2.Credentials(credentials=credentials))

        return self.stub.GetProjects(get_projects_message)
