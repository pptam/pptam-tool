import logging
import docker

def ready(current_configuration, output, test_id): 
    logging.info(f"Testing if SUT is correctly deployed.")

    sut_hostname = current_configuration["docker_test_hostname"]
    docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
    tests = current_configuration["test_if_image_is_present"].split()

    for test in tests:
        logging.info(f"Verifying if container {test} exists.")

        found = False
        for container in docker_client.containers.list():
            logging.info(f"Checking if {test} is in {container.name}")
            if test in container.name:
                found = True

        if not found:
            logging.critical(f"Could not find a container called {test} within the running containers.")
            return False

    return True