from instance_manager_client import InstanceManagerClient

curr_client = InstanceManagerClient()

curr_client.stop_instances('prod-host-4f86', ['us'], '../credentials.json')
