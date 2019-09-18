from instance_manager_client import InstanceManagerClient

curr_client = InstanceManagerClient()

curr_client.stop_instances('i-incentive-253222', ['us'])
