import logging
import docker
import threading
import os
import json
import time

def collect_data(current_configuration, output, test_id, logging, docker, threading, os, json, time):
    logging.info(f"Started Docker stats in background.")
    logging.info("!!!!")
    logging.info(test_id)

    sut_hostname = current_configuration["docker_stats_hostname"]
    docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
    containers_to_watch = current_configuration["docker_stats_containers"].split()

    is_verbose = current_configuration["docker_stats_verbose"]=="1"
    sleep_between_stats_reading_in_seconds = int(current_configuration["docker_stats_sleep_between_stats_reading_in_seconds"])

    global continue_measurement
    continue_measurement = True
    
    while continue_measurement:
        time.sleep(sleep_between_stats_reading_in_seconds)

        logging.info(f"Collecting Docker stats #{i+1} in background.")
        try:                    
            for container in docker_client.containers.list():                
                if (containers_to_watch=="all") or any(test in container.name for test in containers_to_watch):
                    file_to_write = os.path.join(output, f"docker_stats_{container}.log")  
                    if not os.path.isfile(file_to_write) and not is_verbose:
                        with open(file_to_write, "w") as f:                
                            f.write("timestamp, container, cpu_usage, memory_usage, memory_limit\n")
                            f.close()

                    with open(file_to_write, "a") as f:        
                        logging.info(f"Collecting Docker stats of {container.name}.")
                        
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
                    f.close()
        except Exception as e:
            logging.info(f"Exception in Docker stats: {e}")

    logging.info(f"Stopped Docker stats in background.")

def before(current_configuration, output, test_id):
    stats = threading.Thread(target=collect_data, args=(current_configuration, output, test_id, logging, docker, threading, os, json, time), daemon=True)
    stats.start()

def after(current_configuration, output, test_id):
    global continue_measurement
    continue_measurement = False