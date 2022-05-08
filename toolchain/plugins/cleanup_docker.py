import logging
import os
import time
from lib import run_external_applicaton

def setup_all(current_configuration, design_path, test_id):
    logging.info(f"Preparing Docker...")
    if current_configuration["docker_undeploy"]=="1":
        run_external_applicaton("docker service rm $(docker service ls -q) 2>/dev/null", False)
        run_external_applicaton("docker network rm pptam-network 2>/dev/null", False)
    
        # run_external_applicaton("docker network create -d overlay --attachable pptam-network", False)

def setup(current_configuration, output, test_id):
    logging.info(f"Preparing Docker for test {test_id}...")
    if current_configuration["docker_undeploy"]=="1":
        run_external_applicaton("/etc/init.d/docker restart")
    
# def teardown_all(current_configuration, design_path, test_id):
#     if current_configuration["docker_undeploy"]=="1":
#         run_external_applicaton("docker network rm pptam-network", False)