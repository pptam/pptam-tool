import logging
import os
import time
from lib import run_external_applicaton

def prepare_all(global_plugin_state, current_configuration, design_path, test_id):
    run_external_applicaton("docker service rm $(docker service ls -q) 2>/dev/null", False)

def get_configuration_files(global_plugin_state, current_configuration, output, test_id):
    return ["docker-compose.yml"]

def setup(global_plugin_state, current_configuration, output, test_id):
    run_external_applicaton("/etc/init.d/docker restart")

def deploy(global_plugin_state, current_configuration, output, test_id):
    seconds_to_wait_for_deployment = int(current_configuration["docker_waiting_for_deployment_in_seconds"])
    deployment_descriptor = os.path.join(output, "docker-compose.yml")
    command_deploy_stack = f"docker stack deploy --with-registry-auth --compose-file={deployment_descriptor} {test_id}"
    run_external_applicaton(command_deploy_stack)
    logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
    time.sleep(seconds_to_wait_for_deployment)

def undeploy(global_plugin_state, current_configuration, output, test_id):
    seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
    command_undeploy_stack = f"docker stack rm {test_id}"
    run_external_applicaton(command_undeploy_stack)
    logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
    time.sleep(seconds_to_wait_for_undeployment)