import logging
import os
import time
from lib import run_external_applicaton

def setup_all(current_configuration, design_path, test_id):
    deployment_descriptor = os.path.join(design_path, "portainer-agent-stack.yml")
    command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} portainer"
    run_external_applicaton(command_deploy_stack)

def teardown_all(current_configuration, design_path, test_id):
    command_undeploy_stack = f"docker stack rm portainer"
    run_external_applicaton(command_undeploy_stack)
    