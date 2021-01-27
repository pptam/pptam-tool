import logging
import os
import time
from lib import run_external_applicaton

def setup_all(global_plugin_state, current_configuration, design_path, test_id):
    deployment_descriptor = os.path.join(design_path, "portainer-agent-stack.yml")    
    if os.path.exists(deployment_descriptor):
        logging.info(f"Deploying Portainer.")
        command_deploy_stack = f"docker stack deploy --compose-file={deployment_descriptor} portainer"
        run_external_applicaton(command_deploy_stack)
    else:
        logging.info(f"Not deploying Portainer since {deployment_descriptor} does not exist.")

def teardown_all(global_plugin_state, current_configuration, design_path, test_id):
    deployment_descriptor = os.path.join(design_path, "portainer-agent-stack.yml")
    if os.path.exists(deployment_descriptor):
        logging.info(f"Undeploying Portainer.")
        command_undeploy_stack = f"docker stack rm portainer"
        run_external_applicaton(command_undeploy_stack)
    else:
        logging.info(f"Not undeploying Portainer since {deployment_descriptor} does not exist.")
    