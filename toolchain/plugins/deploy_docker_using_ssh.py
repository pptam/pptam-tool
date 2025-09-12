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

        # replace design_path with the remote design path
        target_folder = current_configuration["docker_deploy_ssh_target_folder"]
        outputText = template.render(design_path=target_folder)
        with open(os.path.join(design_path, "docker-compose.yml"), "w") as f:
            f.write(outputText)
    return ["docker-compose.yml"]

def setup(current_configuration, design_path, output, test_id):

    def run_external_remote_applicaton(command, halt_on_error=True):
        target_machine = current_configuration["docker_deploy_ssh_target_machine"]
        remote_command = f'ssh {target_machine} "{command}"'
        return run_external_application(remote_command, halt_on_error)

    logging.info(f"Preparing Docker for test {test_id}...")
    if current_configuration["docker_undeploy"]=="1":
        run_external_remote_applicaton("docker ps -q | grep . && docker stop \$(docker ps -q)", False)
        run_external_remote_applicaton("docker ps -aq | grep . && docker rm \$(docker ps -aq)", False)
        run_external_remote_applicaton("docker network ls -q | grep . && docker network prune -f", False)
        run_external_remote_applicaton("docker volume ls -q | grep . && docker volume prune -f", False)

def deploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_deploy"]=="1":
        logging.info(f"Deploying for test {test_id}.")
        seconds_to_wait_for_deployment = int(current_configuration["docker_waiting_for_deployment_in_seconds"])
        
        target_machine = current_configuration["docker_deploy_ssh_target_machine"]
        target_folder = current_configuration["docker_deploy_ssh_target_folder"]

        command_check_folder = f'ssh {target_machine} "test -d {target_folder}"'
        result = run_external_application(command_check_folder, False)
        if result != 0:
            command_copy = f"scp -r {design_path}/* {target_machine}:{target_folder}"
            run_external_application(command_copy)
        
        deployment_descriptor = os.path.join(output, "docker-compose.yml")
        target_deployment_descriptor = os.path.join(target_folder, "docker-compose.yml")
        target_deployment_descriptor = f"{target_folder}\\docker-compose.yml"
        command_copy_compose = f'scp -r {deployment_descriptor} "{target_machine}:{target_deployment_descriptor}"'
        run_external_application(command_copy_compose)

        command_deploy = f'ssh {target_machine} docker compose -f "{target_deployment_descriptor}" up -d --build'
        run_external_application(command_deploy)

        logging.info(f"Waiting for {seconds_to_wait_for_deployment} seconds to allow the application to deploy.")
        time.sleep(seconds_to_wait_for_deployment)

def undeploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_undeploy"]=="1":
        logging.info(f"Undeploying for test {test_id}.")
        seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
        
        target_machine = current_configuration["docker_deploy_ssh_target_machine"]
        target_file = os.path.join(current_configuration["docker_deploy_ssh_target_folder"], "docker-compose.yml")
        command_undeploy = f'ssh {target_machine} docker compose -f "{target_file}" down --timeout 1'
        run_external_application(command_undeploy)

        logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
        time.sleep(seconds_to_wait_for_undeployment)
