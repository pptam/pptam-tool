import logging
import docker
import threading
import os
import json
import time

def setup(current_configuration, output):
    logging.debug(f"Plugin #{os.path.basename(__file__)}: setup")
    
def before(current_configuration, output):
    logging.debug(f"Plugin #{os.path.basename(__file__)}: before")

    sut_hostname = current_configuration["docker_sut_hostname"]
    docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
    
    global run_docker_stats_in_background
    run_docker_stats_in_background = threading.Thread(target=get_docker_stats, args=(
            docker_client,            
            output,
            True
        ), daemon=True)
    run_docker_stats_in_background.start()

def get_docker_stats(client, output_path, verbose = False):
    while True:
        with open(os.path.join(output_path, "docker_stats.log"), "a") as f:
            if not verbose:
                f.write("timestamp, container, cpu_usage, memory_usage, memory_limit\n")
            for container in client.containers.list():
                stats = container.stats(stream=False) # takes about 2s
                if not verbose:
                    timestamp = stats["read"]
                    container = container.name
                    cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
                    memory_usage = stats["memory_stats"]["usage"]
                    memory_limit = stats["memory_stats"]["limit"]
                    f.write(f"{timestamp}, {container}, {cpu_usage}, {memory_usage}, {memory_limit}\n")
                else:
                    f.write(json.dumps(stats) + '\n')

        time.sleep(10)  # Configure


def shutdown(current_configuration, output):
    logging.debug(f"Plugin #{os.path.basename(__file__)}: shutdown")
