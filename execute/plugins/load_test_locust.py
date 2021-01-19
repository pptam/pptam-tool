import logging
import os
from lib import run_external_applicaton

def get_configuration_files(global_plugin_state, current_configuration, output, test_id):
    return ["locustfile.py"]

def run(global_plugin_state, current_configuration, output, test_id):
    driver = f"{output}/locustfile.py"
    host = current_configuration["locust_host_url"]
    load = current_configuration["load"]
    spawn_rate = current_configuration["spawn_rate_per_second"]
    run_time = current_configuration["run_time_in_seconds"]
    log_file = os.path.splitext(driver)[0] + ".log"
    out_file = os.path.splitext(driver)[0] + ".out"
    csv_prefix = os.path.join(os.path.dirname(driver), "result")
    logging.info(f"Running the load test for {test_id}, with {load} users, running for {run_time} seconds.")
    run_external_applicaton(
        f'~/.local/bin/locust --locustfile {driver} --host {host} --users {load} --spawn-rate {spawn_rate} --run-time {run_time}s --headless --only-summary --csv {csv_prefix} --csv-full-history --logfile "{log_file}" --loglevel DEBUG >> {out_file} 2> {out_file}', False)


