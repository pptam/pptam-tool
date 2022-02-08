import logging
import os
import time
import pathlib
from lib import run_external_applicaton

def setup_all(global_plugin_state, current_configuration, design_path, test_id):
    deployment_descriptor = os.path.join(pathlib.Path(__file__).parent.absolute(), "portainer.yml")        
    run_external_applicaton(f"docker stack deploy --compose-file={deployment_descriptor} portainer")

def teardown_all(global_plugin_state, current_configuration, design_path, test_id):    
    run_external_applicaton(f"docker stack rm portainer")
    run_external_applicaton(f"docker volume rm portainer_portainer_data")
    
    