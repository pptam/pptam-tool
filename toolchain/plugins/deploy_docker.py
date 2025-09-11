import logging
import os
import time
import jinja2
from lib import run_external_application

def get_files(current_configuration, design_path, output, test_id):
    if os.path.exists(os.path.join(design_path, "docker-compose.yml.jinja")):
        template_loader = jinja2.FileSystemLoader(searchpath=design_path)
        template_environment = jinja2.Environment(loader=template_loader)
        template_file = "docker-compose.yml.jinja"
        template = template_environment.get_template(template_file)
        outputText = template.render(design_path=os.path.abspath(design_path))
        with open(os.path.join(design_path, "docker-compose.yml"), "w") as f:
            f.write(outputText)
            
    return ["docker-compose.yml"]

def setup(current_configuration, design_path, output, test_id):
    logging.info(f"Preparing Docker for test {test_id}...")
    if current_configuration["docker_undeploy"]=="1":
        run_external_application("docker ps -q | grep . && docker stop $(docker ps -q)", False)
        run_external_application("docker ps -aq | grep . && docker rm $(docker ps -aq)", False)
        run_external_application("docker network ls -q | grep . && docker network prune -f", False)
        run_external_application("docker volume ls -q | grep . && docker volume prune -f", False)

def deploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_deploy"]=="1":
        logging.info(f"Deploying for test {test_id}.")
        seconds_to_wait_for_deployment = int(current_configuration["docker_waiting_for_deployment_in_seconds"])
        deployment_descriptor = os.path.join(output, "docker-compose.yml")
        command_deploy = f"docker compose --file {deployment_descriptor} up --detach"
        run_external_application(command_deploy)
        logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
        time.sleep(seconds_to_wait_for_deployment)

# def undeploy(current_configuration, design_path, output, test_id):
#     if current_configuration["docker_undeploy"]=="1":
#         logging.info(f"Undeploying for test {test_id}.")
#         seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
#         deployment_descriptor = os.path.join(output, "docker-compose.yml")
#         command_undeploy = f"docker compose --file {deployment_descriptor} down --timeout 1"
#         run_external_application(command_undeploy)
#         logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
#         time.sleep(seconds_to_wait_for_undeployment)
