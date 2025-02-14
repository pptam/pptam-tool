import logging
import docker

def ready(current_configuration, design_path, output, test_id):
    logging.debug(f"Testing if SUT is correctly deployed.")

    sut_hostname = current_configuration["docker_test_hostname"]
    logging.info("01")
    client = docker.DockerClient(base_url=f"tcp://{sut_hostname}:2375")
    logging.info("02")
    tests = current_configuration["docker_test_if_image_is_present"].split()
    logging.info("03")

    for container_name in tests:
        logging.info(f"Checking if any running container contains '{container_name}' in its name.")            

        try:
            running_containers = client.containers.list()

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

    logging.info("3")
    return True