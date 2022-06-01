import logging
import docker
import os
import json
import time
import sched
import threading
from queue import Queue
from datetime import datetime
import dateutil.parser

def measure_worker(configuration, output, test_id, write_queue):
    logging.info(f"Collecting Docker stats in background.")

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

    def collect_stats_of_single_container(write_queue, service_name, container_to_analyze, collection_timestamp):
        stats = None
        # try:
        stats = container_to_analyze.stats(stream=False) 
        if (stats != None):
            reading_timestamp_as_iso_date = stats["read"]
            reading_timestamp_as_datetime = dateutil.parser.isoparse(reading_timestamp_as_iso_date)
            reading_timestamp = datetime.timestamp(reading_timestamp_as_datetime)

            cpu_usage_in_percent = calculate_cpu_percent_norm(stats)
            mem_usage = int(stats["memory_stats"]["usage"])
            mem_limit = int(stats["memory_stats"]["limit"])
            mem_usage_in_percent = mem_usage / mem_limit * 100

            a = "{:.2f}".format(cpu_usage_in_percent)
            b = "{:.2f}".format(mem_usage_in_percent)
            c = "{:.2f}".format(mem_usage)
            d = "{:.2f}".format(mem_limit)
            write_queue.put(f"{collection_timestamp},{reading_timestamp},{service_name},{a},{b},{c},{d}\n")
            # f.write(f"{json.dumps(stats, indent=2)}\n")

        # except Exception as e:
        #     logging.critical(f"Exception in Docker stats: {e}")

    def collect_stats(write_queue):
        logging.info(f"Running Docker stats.")

        collection_timestamp = datetime.timestamp(datetime.utcnow())

        containers_to_watch = configuration["docker_stats_containers"].split()
        sut_hostname = configuration["docker_stats_hostname"]
        docker_client = docker.DockerClient(base_url=f"{sut_hostname}:2375")
        for container in docker_client.containers.list():
            service_name = container.name[len(test_id)+2:]
            first_dot = service_name.find(".")
            if first_dot > 0:
                service_name = service_name[0:first_dot]

            if ("all" in containers_to_watch) or (service_name in containers_to_watch):
                if f"!{service_name}" in containers_to_watch:
                    logging.debug(f"Skipping container {container.name}.")
                else:
                    logging.debug(f"Collecting stats of container {container.name}.")
                    data_collection_of_one_container = threading.Thread(target = collect_stats_of_single_container, args=(write_queue, service_name, container, collection_timestamp), daemon=True)
                    data_collection_of_one_container.start()

    docker_stats_run_every_number_of_seconds = int(configuration["docker_stats_run_every_number_of_seconds"])
    run_time_in_seconds = int(configuration["run_time_in_seconds"])
    number_of_calls = 1 + (run_time_in_seconds // docker_stats_run_every_number_of_seconds)
    logging.info(f"Scheduling Docker stats for #{number_of_calls} times.")

    scheduler_for_docker_stats = sched.scheduler()        
    for i in range(number_of_calls):
        logging.info(f"Scheduling Docker stats after #{i*docker_stats_run_every_number_of_seconds} seconds.")
        scheduler_for_docker_stats.enter(i*docker_stats_run_every_number_of_seconds, 1, collect_stats, argument=(write_queue,))

    scheduler_for_docker_stats.run()

def queue_worker(write_queue, output):
    logging.info(f"Waiting for Docker stats results.")

    file_to_write = os.path.join(output, f"docker_stats.csv")
    with open(file_to_write, "w") as f:
        f.write("collected,timestamp,service,cpu_usage_percent,memory_usage_percent,memory_usage,memory_limit\n")

    with open(file_to_write, "a") as f:
        while True:
            item = write_queue.get()
            f.write(item)
            f.flush()

def before(current_configuration, output, test_id):    
    write_queue = Queue()
    threading.Thread(target=queue_worker, args=(write_queue, output), daemon=True).start()
    threading.Thread(target=measure_worker, args=(current_configuration, output, test_id, write_queue), daemon=True).start()
    
def after(current_configuration, output, test_id):  
    logging.info(f"Stopping Docker stats.")
    
    


