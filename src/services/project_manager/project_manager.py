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
This module manages Google Cloud Projects.
"""

import time
import json
from pprint import pprint
from concurrent import futures
from googleapiclient import discovery

import grpc
import project_manager_pb2
import project_manager_pb2_grpc

from lib.lab_keeper.config import Config
from lib.lab_keeper.authenticator import Authenticator

class ProjectManagerServicer(project_manager_pb2_grpc.ProjectManagerServicer):
    """gRPC server for Project Manager service."""
    def __init__(self):
        self.config = Config()
        self.authenticator = Authenticator()
        self.server_port = self.config.project_manager_port

    def start_server(self):
        """
        Start the gRPC server, and prep
        it for serving incoming connections
        """
        project_manager_server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=10))
        project_manager_pb2_grpc.add_ProjectManagerServicer_to_server(
            ProjectManagerServicer(), project_manager_server)
        project_manager_server.add_insecure_port(
            f'[::]:{self.server_port}')
        project_manager_server.start()

        pprint(f"Project Manager Server running in port {self.server_port}...")

        try:
            while True:
                time.sleep(60*60*60)
        except KeyboardInterrupt:
            project_manager_server.stop(0)
            pprint("Instance Manager Server stopped...")

    def GetProjects(self, request, context):
        """
        Returns list of projects available for user.
        """

        project_list = []

        pprint("Request received...")

        credentials = self.authenticator.make_credentials(
            json.loads(request.credentials.credentials)
        )

        service = discovery.build(
            'cloudresourcemanager', 'v1', credentials=credentials)


        request = service.projects().list(filter='lifecycleState = ACTIVE')
        response = request.execute()
        for project in response.get('projects', []):
            # TODO: Change code below to process each `project` resource:

            project_name = project.get("name", None)
            project_id = project.get("projectId", None)

            project_list.append(
                project_manager_pb2.Project(
                    name=project_name,
                    project_id=project_id
                ))

        pprint(f'Found {len(project_list)} active projects.')

        result = project_manager_pb2.ProjectList(
            projects=project_list
        )

        pprint(result)

        return result

curr_server = ProjectManagerServicer()
curr_server.start_server()
