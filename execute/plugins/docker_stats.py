import logging
import docker
import threading
import os
import time
import json
    
def before(current_configuration, output, test_id):
    sut_hostname = current_configuration["docker_stats_hostname"]
    docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
    file_to_write = os.path.join(output, "docker_stats.log")  
    
    global run_docker_stats_in_background
    run_docker_stats_in_background = threading.Thread(target=get_docker_stats, args=(
            current_configuration,
            docker_client,            
            file_to_write,
            time, #Necessary, because of https://stackoverflow.com/questions/17084260/imported-modules-become-none-when-running-a-function/17531377
            json
        ), daemon=True)
    run_docker_stats_in_background.start()

def get_docker_stats(current_configuration, client, file_to_write, time, json):
    sleep_between_stats_reading_in_seconds = int(current_configuration["docker_stats_sleep_between_stats_reading_in_seconds"])
    is_verbose = current_configuration["docker_stats_verbose"]=="1"
    
    while True:
        with open(file_to_write, "a") as f:
            if not is_verbose:
                f.write("timestamp, container, cpu_usage, memory_usage, memory_limit\n")
            for container in client.containers.list():
                stats = container.stats(stream=False) # takes about 2s
                if (stats!=None):
                    if not is_verbose:
                        timestamp = stats["read"]
                        container = container.name
                        cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
                        memory_usage = stats["memory_stats"]["usage"]
                        memory_limit = stats["memory_stats"]["limit"]
                        f.write(f"{timestamp}, {container}, {cpu_usage}, {memory_usage}, {memory_limit}\n")
                    else:
                        f.write(f"{json.dumps(stats, indent=2)}\n")

        time.sleep(sleep_between_stats_reading_in_seconds) 
