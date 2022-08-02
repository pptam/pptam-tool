import logging
import os
import time
from lib import run_external_applicaton

def get_configuration_files(current_configuration, design_path, output, test_id):
    return ["docker-compose.yml"]
   
def deploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_deploy"]=="1":
        logging.info(f"Deploying for test {test_id}.")
        seconds_to_wait_for_deployment = int(current_configuration["docker_waiting_for_deployment_in_seconds"])
        deployment_descriptor = os.path.join(output, "docker-compose.yml")
        command_deploy_stack = f"docker stack deploy --with-registry-auth --compose-file={deployment_descriptor} {test_id}"
        run_external_applicaton(command_deploy_stack)
        logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
        time.sleep(seconds_to_wait_for_deployment)

def undeploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_undeploy"]=="1":
        logging.info(f"Undeploying for test {test_id}.")
        seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
        command_undeploy_stack = f"docker stack rm {test_id}"
        run_external_applicaton(command_undeploy_stack)
        logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
        time.sleep(seconds_to_wait_for_undeployment)
