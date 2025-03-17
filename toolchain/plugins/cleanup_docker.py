import logging
import os
import time
from lib import run_external_applicaton

def setup(current_configuration, design_path, output, test_id):
    logging.info(f"Preparing Docker for test {test_id}...")
    if current_configuration["docker_undeploy"]=="1":
        run_external_applicaton("docker ps -q | grep . && docker stop $(docker ps -q)", False)
        run_external_applicaton("docker ps -aq | grep . && docker rm $(docker ps -aq)", False)
        run_external_applicaton("docker network ls -q | grep . && docker network prune -f", False)
        run_external_applicaton("docker volume ls -q | grep . && docker volume prune -f", False)
        # run_external_applicaton("sudo service docker restart")
        
