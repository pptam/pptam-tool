import logging
import os
import time
import jinja2
from lib import run_external_applicaton

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
   
def deploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_deploy"]=="1":
        logging.info(f"Deploying for test {test_id}.")
        seconds_to_wait_for_deployment = int(current_configuration["docker_waiting_for_deployment_in_seconds"])
        deployment_descriptor = os.path.join(output, "docker-compose.yml")

        target_machine = current_configuration["docker_deploy_ssh_target_machine"]
        target_file = os.path.join(current_configuration["docker_deploy_ssh_target_folder"], "docker-compose.yml")

        command_copy = f"scp {deployment_descriptor} {target_machine}:{target_file}"
        run_external_applicaton(command_copy)
                
        command_deploy = f"ssh {target_machine} docker compose -f {target_file} up -d"
        run_external_applicaton(command_deploy)

        logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
        time.sleep(seconds_to_wait_for_deployment)

def undeploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_undeploy"]=="1":
        logging.info(f"Undeploying for test {test_id}.")
        seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
        
        target_machine = current_configuration["docker_deploy_ssh_target_machine"]
        target_file = os.path.join(current_configuration["docker_deploy_ssh_target_folder"], "docker-compose.yml")
        command_undeploy = f"ssh {target_machine} docker compose -f {target_file} down --timeout 1"
        run_external_applicaton(command_undeploy)

        logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
        time.sleep(seconds_to_wait_for_undeployment)
