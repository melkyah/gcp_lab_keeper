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
This module handles application configuration values.
"""


class Config:
    """
    This class handles base configuration.
    """

    def __init__(self):
        """Initialize settings."""
        # TODO: This only works when standing in lab_keeper.py directory.
        self.credentials = 'D:\Projects\lab-keeper\gcp_instance_watcher\src\services\credentials.json'
        self.instance_manager_server = 'localhost'
        self.instance_manager_port = '46001'
