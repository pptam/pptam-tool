import logging
import os
import jinja2
from lib import run_external_applicaton

def get_files(current_configuration, design_path, output, test_id):
    if os.path.exists(os.path.join(design_path, "locustfile.py.jinja")):
        template_loader = jinja2.FileSystemLoader(searchpath=design_path)
        template_environment = jinja2.Environment(loader=template_loader)
        template_file = "locustfile.py.jinja"
        template = template_environment.get_template(template_file)
        outputText = template.render(design_path=os.path.abspath(design_path))
        with open(os.path.join(design_path, "locustfile.py"), "w") as f:
            f.write(outputText)

    return ["locustfile.py"]

def run(current_configuration, design_path, output, test_id):
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
        f'locust --locustfile {driver} --host {host} --users {load} --spawn-rate {spawn_rate} --run-time {run_time}s --headless --only-summary --csv {csv_prefix} --csv-full-history --logfile "{log_file}" --loglevel DEBUG --html {csv_prefix}.html > {out_file} 2>&1', False)


