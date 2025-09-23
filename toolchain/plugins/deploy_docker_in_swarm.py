import logging
import os
import time
import jinja2
import requests
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
        collect_containers_pids(output,current_configuration)

def undeploy(current_configuration, design_path, output, test_id):
    if current_configuration["docker_undeploy"]=="1":
        logging.info(f"Undeploying for test {test_id}.")
        seconds_to_wait_for_undeployment = int(current_configuration["docker_waiting_for_undeployment_in_seconds"])
        command_undeploy_stack = f"docker stack rm {test_id}"
        run_external_application(command_undeploy_stack)
        logging.info(f"Waiting for {seconds_to_wait_for_undeployment} seconds to allow the application to undeploy.")
        time.sleep(seconds_to_wait_for_undeployment)

       
def get_docker_pids_base_url(configuration):
    host_value = configuration.get("docker_pids_hostname")
    if not host_value:
        raise ValueError("DOCKER_PIDS_HOSTNAME not configured")
    
    if host_value.startswith("http://") or host_value.startswith("https://"):
        base = host_value
    else:
        base = f"http://{host_value}"
    
    if ":" not in base.split("//", 1)[-1]:
        base = f"{base}:8080"
    
    return base.rstrip("/")

def collect_containers_pids(output_path, configuration):
    logging.info("Collecting container → PID mapping via HTTP.")
    
    base_url = get_docker_pids_base_url(configuration)
    endpoint_url = f"{base_url}/"  # Assuming the JSON is served at the root path
    file_path = os.path.join(output_path, "containers_pids.csv")
    
    try:
        logging.info(f"Fetching container data from {endpoint_url}")
        response = requests.get(endpoint_url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse JSON response
        data = response.json()
        
        # Check if there's an error in the response
        if "error" in data:
            logging.error(f"Error from scaphandre endpoint: {data['error']}")
            raise Exception(data["error"])
        
        # Write CSV file
        with open(file_path, "w") as f:
            f.write("container_id,container_name,pid\n")
            
            containers = data.get("containers", [])
            if not containers:
                logging.warning("No containers found in the response")
            
            for container in containers:
                cid = container.get("id", "")
                cname = container.get("names", "")
                pid = container.get("pid")
                
                if pid is not None:
                    f.write(f"{cid},{cname},{pid}\n")
                else:
                    f.write(f"{cid},{cname},\n")
                    logging.warning(f"No PID available for container {cid}")
        
        logging.info(f"✅ Container PID mapping written to {file_path}")
        
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")
        # Create empty CSV file in case of failure
        with open(file_path, "w") as f:
            f.write("container_id,container_name,pid\n")
        raise
    except Exception as e:
        logging.error(f"Failed to collect container PIDs: {e}")
        # Create empty CSV file in case of failure
        with open(file_path, "w") as f:
            f.write("container_id,container_name,pid\n")
        raise