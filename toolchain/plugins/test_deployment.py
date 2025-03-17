import logging
import docker

def ready(current_configuration, design_path, output, test_id):
    docker_daemon_base_url = current_configuration["docker_daemon_base_url"]
    logging.debug(f"Testing if SUT is correctly deployed connecting to {docker_daemon_base_url}.")
    
    # The docker url is often tcp://localhost:2375 on Windows or unix:///var/run/docker.sock on Linux or Mac
    client = docker.DockerClient(base_url=docker_daemon_base_url)
    tests = current_configuration["docker_test_if_image_is_present"].split()

    for container_name in tests:
        logging.info(f"Checking if any running container contains '{container_name}' in its name.")            

        try:
            running_containers = client.containers.list()
            logging.info(f"Running containers: {[c.name for c in running_containers]}.")   

            matching_containers = [
                container for container in running_containers if container_name in container.name
            ]

            if matching_containers:
                logging.info(f"Found a running container matching '{container_name}': {[c.name for c in matching_containers]}")
            else:
                logging.critical(f"No running container contains '{container_name}' in its name.")
                return False

        except docker.errors.APIError as e:
            logging.critical(f"Docker API error: {repr(e)}")
            return False

    return True