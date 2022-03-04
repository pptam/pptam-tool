import logging
import docker
import threading
import os
import json
import time

class CollectionTask:
    def __init__(self, current_configuration, logging, docker, threading, os, json, time):
        self._running = True
        sut_hostname = current_configuration["docker_stats_hostname"]
        self.docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
        self.containers_to_watch = current_configuration["docker_stats_containers"].split()
        self.is_verbose = current_configuration["docker_stats_verbose"] == "1"
        self.sleep_between_stats_reading_in_seconds = int(current_configuration["docker_stats_sleep_between_stats_reading_in_seconds"])

        self.logging = logging
        self.docker = docker
        self.threading = threading
        self.os = os
        self.json = json
        self.time = time

    def terminate(self):
        self._running = False

    def run(self, output, test_id):

        def calculate_cpu_percent_norm(d):
            # The field cpu_count is not always present. If used, we need to check that it is present.
            # cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
            cpu_percent = 0.0
            cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                        float(d["precpu_stats"]["cpu_usage"]["total_usage"])
            system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                           float(d["precpu_stats"]["system_cpu_usage"])
            if system_delta > 0.0:
                cpu_percent = cpu_delta / system_delta * 100.0 #* cpu_count
            return cpu_percent

        def extract_service_name(container, test_id):
            service_name = container[len(test_id)+1:]
            last_dot = service_name.rfind(".")
            if last_dot > 0:
                service_name = service_name[0:last_dot-2]
            return service_name

        def collect_stats(output, service_name, container):
            file_to_write = self.os.path.join(output, f"docker_stats.csv")

            if not self.os.path.isfile(file_to_write) and not self.is_verbose:
                with open(file_to_write, "w") as f:
                    f.write("timestamp, service, cpu_perc, mem_perc\n")

            with open(file_to_write, "a") as f:
                self.logging.debug(f"Collecting Docker stats of {container.name}.")

                stats = None
                try:
                    stats = container.stats(stream=False) # takes about 2s
                    if (stats != None):
                        if not self.is_verbose:
                            timestamp = stats["read"]
                            cpu_perc = calculate_cpu_percent_norm(stats)
                            mem_perc = int(stats["memory_stats"]["usage"]) / int(stats["memory_stats"]["limit"]) * 100
                            f.write(f"{timestamp},{service_name},{str(cpu_perc)},{str(mem_perc)}\n")
                        else:
                            f.write(f"{self.json.dumps(stats, indent=2)}\n")

                except Exception as e:
                    self.logging.critical(f"Exception in Docker stats: {e}")

        def measure():
            print("Collecting Docker stats at ", datetime.now().strftime("%H:%M:%S"))

            try:
                for container in self.docker_client.containers.list():
                    service_name = extract_service_name(container.name, test_id)

                    if ("all" in self.containers_to_watch) or (service_name in self.containers_to_watch):
                        if f"!{service_name}" in self.containers_to_watch:
                            logging.debug(f"Skipping container {container.name}.")
                        else:
                            collect_stats(output, service_name, container)

            except Exception as e:
                self.logging.critical(f"Exception in Docker stats: {e}")

        self.logging.info(f"Collecting Docker stats #{iteration} in background.")
        s = sched.scheduler()
        
        s.enter(5, 1, print_time)
        s.enter(6, 1, print_time)
        s.enter(7, 1, print_time)

        s.run()

            

            

data_collection = None

def before(global_plugin_state, current_configuration, output, test_id):    
    data_collection = CollectionTask(current_configuration, logging, docker, threading, os, json, time)
    t = threading.Thread(target = data_collection.run, args =(output, test_id), daemon=True)
    t.start()

    global_plugin_state["docker_stats_data_collection_class"] = data_collection

def after(global_plugin_state, current_configuration, output, test_id):    
    global_plugin_state["docker_stats_data_collection_class"].terminate()
    del global_plugin_state["docker_stats_data_collection_class"]
