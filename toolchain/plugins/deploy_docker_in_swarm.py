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

def setup_all(current_configuration, design_path, output, test_id):
    logging.info("Preparing Docker...")
    if current_configuration["docker_undeploy"]=="1":
        run_external_application("docker service rm $(docker service ls -q) 2>/dev/null", False)
        run_external_application("docker network rm pptam-network 2>/dev/null", False)
    
        # run_external_application("docker network create -d overlay --attachable pptam-network", False)

def setup(current_configuration, design_path, output, test_id):
    logging.info(f"Preparing Docker for test {test_id}...")
    if current_configuration["docker_undeploy"]=="1":
        #run_external_application("sudo snap restart docker")
        run_external_application("sudo service docker restart")
    
# def teardown_all(current_configuration, design_path, output, test_id):
#     if current_configuration["docker_undeploy"]=="1":
#         run_external_application("docker network rm pptam-network", False)

def deploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_deploy"]=="1":
        logging.info(f"Deploying for test {test_id}.")
        seconds_to_wait_for_deployment = int(current_configuration["docker_waiting_for_deployment_in_seconds"])
        deployment_descriptor = os.path.join(output, "docker-compose.yml")
        command_deploy_stack = f"docker stack deploy --detach=false --with-registry-auth --compose-file={deployment_descriptor} {test_id}"
        run_external_application(command_deploy_stack)
        logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
        time.sleep(seconds_to_wait_for_deployment)

def undeploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_undeploy"]=="1":
        logging.info(f"Undeploying for test {test_id}.")
        seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
        command_undeploy_stack = f"docker stack rm {test_id}"
        run_external_application(command_undeploy_stack)
        logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
        time.sleep(seconds_to_wait_for_undeployment)
