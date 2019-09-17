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
    This module contains the implementation of authentication managing components.
"""

import json

from google.oauth2 import service_account

from config import Config


class Authenticator:
    """
        Manages GCP credentials.
    """

    def __init__(self):
        """Initialze parameters"""
        self.config = Config()
        self.credentials_path = self.config.credentials

    def make_credentials(self):
        """Creates GCP credentials from a JSON key file"""
        with open(self.credentials_path) as source:
            info = json.load(source)

        credentials = service_account.Credentials.from_service_account_info(
            info)

        return credentials
