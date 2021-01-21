import logging
import docker
import threading
import os
import json
import time

class CollectionTask:       
    def __init__(self, current_configuration, logging, docker, threading, os, json, time): 
        self._running = True
        logging.info(f"Started Docker stats in background.")

        sut_hostname = current_configuration["docker_stats_hostname"]
        self.docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
        self.containers_to_watch = current_configuration["docker_stats_containers"].split()
        self.is_verbose = current_configuration["docker_stats_verbose"]=="1"
        self.sleep_between_stats_reading_in_seconds = int(current_configuration["docker_stats_sleep_between_stats_reading_in_seconds"])

        self.logging = logging
        self.docker = docker
        self.threading = threading
        self.os = os
        self.json = json
        self.time = time

    def terminate(self): 
        self.logging.info(f"Stopping Docker stats in background.")
        self._running = False
    
    def run(self, output, test_id): 

        def collect_stats(output, service_name, container):
            file_to_write = self.os.path.join(output, f"docker_stats.csv")   

            if not self.os.path.isfile(file_to_write) and not self.is_verbose:
                with open(file_to_write, "w") as f:                
                    f.write("timestamp, service, cpu_usage, memory_usage, memory_limit\n")
                    f.close()

            with open(file_to_write, "a") as f:        
                self.logging.info(f"Collecting Docker stats of {container.name}.")
                
                try:
                    stats = container.stats(stream=False) # takes about 2s
                    if (stats!=None):
                        if not self.is_verbose:
                            timestamp = stats["read"]
                            cpu_usage = stats["cpu_stats"]["cpu_usage"]["total_usage"]
                            memory_usage = stats["memory_stats"]["usage"]
                            memory_limit = stats["memory_stats"]["limit"]
                            f.write(f"{timestamp}, {service_name}, {cpu_usage}, {memory_usage}, {memory_limit}\n")
                        else:
                            f.write(f"{json.dumps(stats, indent=2)}\n")
                    else:
                        self.logging.critical(f"Cannot collect Docker stats.")
                except Exception as e:
                    self.logging.critical(f"Exception in Docker stats: {e}")

            f.close()

        iteration = 1
        
        while self._running:
            self.logging.info(f"Collecting Docker stats #{iteration} in background.")
            iteration = iteration + 1

            try:         
                for container in self.docker_client.containers.list():      
                    if (any("all" in s for s in self.containers_to_watch) or any(test in container.name for test in self.containers_to_watch)):
                        service_name = container.name[len(test_id)+1:]
                        last_dot = service_name.rfind(".")
                        if last_dot > 0:
                            service_name = service_name[0:last_dot-2]
                        
                        collect_stats(output, service_name, container)
  
            except Exception as e:
                self.logging.critical(f"Exception in Docker stats: {e}")

            self.time.sleep(self.sleep_between_stats_reading_in_seconds)

data_collection = None

def before(global_plugin_state, current_configuration, output, test_id):
    data_collection = CollectionTask(current_configuration, logging, docker, threading, os, json, time) 
    t = threading.Thread(target = data_collection.run, args =(output, test_id), daemon=True) 
    t.start()

    global_plugin_state["docker_stats_data_collection_class"] = data_collection

def after(global_plugin_state, current_configuration, output, test_id):
    global_plugin_state["docker_stats_data_collection_class"].terminate()
    del global_plugin_state["docker_stats_data_collection_class"]