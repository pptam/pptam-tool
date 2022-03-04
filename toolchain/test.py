#!/usr/bin/env python3
 
import logging
import docker
import threading
import os
import json
import time
from datetime import datetime
import sched, time

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
    file_to_write = os.path.join(output, f"docker_stats.csv")

    if not os.path.isfile(file_to_write) and not is_verbose:
        with open(file_to_write, "w") as f:
            f.write("timestamp, service, cpu_perc, mem_perc\n")

    with open(file_to_write, "a") as f:
        logging.debug(f"Collecting Docker stats of {container.name}.")

        stats = None
        try:
            stats = container.stats(stream=False) # takes about 2s
            if (stats != None):
                if not is_verbose:
                    timestamp = stats["read"]
                    cpu_perc = calculate_cpu_percent_norm(stats)
                    mem_perc = int(stats["memory_stats"]["usage"]) / int(stats["memory_stats"]["limit"]) * 100
                    f.write(f"{timestamp},{service_name},{str(cpu_perc)},{str(mem_perc)}\n")
                else:
                    f.write(f"{json.dumps(stats, indent=2)}\n")

        except Exception as e:
            logging.critical(f"Exception in Docker stats: {e}")

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)

# output = "."
# test_id = "123"
# is_verbose = True
# docker_client = docker.DockerClient(base_url=f"socks4.inf.unibz.it:2375")
# for container in docker_client.containers.list():
#     service_name = extract_service_name(container.name, test_id)
#     if ("-mongo" not in service_name) and ("-admin" not in service_name):
#         collect_stats(output, service_name, container) 

# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)

# Not verbose, all:
# Current Time = 12:18:16
# Current Time = 12:20:32
# 2 min, 16 sec

# Verbose, all:
# Current Time = 12:21:02
# Current Time = 12:23:18
# 2 min, 16 sec

# Verbose, only relevant
# Current Time = 12:24:32
# Current Time = 12:25:49
# 1 min, 17 sec

s = sched.scheduler()
def print_time():
    print("Current Time =", datetime.now().strftime("%H:%M:%S"))

def print_some_times():
    print("a =", datetime.now().strftime("%H:%M:%S"))

    s.enter(5, 1, print_time)
    s.enter(6, 1, print_time)
    s.enter(7, 1, print_time)

    s.run()
    print("b =", datetime.now().strftime("%H:%M:%S"))

print_some_times()