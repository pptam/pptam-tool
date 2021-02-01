import logging
import requests
import json
import os
import time

def after(global_plugin_state, current_configuration, output, test_id): 
    jaeger_host = current_configuration["jaeger_host_url"]
    jaeger_services = current_configuration["jaeger_services"].split(" ")
    service_to_test = current_configuration["jaeger_test_if_service_is_present"]

    all_services = []
    for _ in range(60):   
        try:
            session = requests.Session()
            session.headers.update({'accept': 'application/json'})
            session.headers.update({'content-type': 'application/json'})
    
            logging.info(f"Contacting Jaeger host {jaeger_host}/api/services")
            service_request = session.get(f"{jaeger_host}/api/services")
            all_services = service_request.json()["data"]
            
            if all_services is None:
                logging.critical(f"Cannot determine Jaeger services.")
            else:
                if not (service_to_test in all_services):
                    logging.critical(f"Service {service_to_test} is not in the list of services.")
                else:
                    break

        except Exception as e:
                self.logging.critical(f"Exception while determining Jaeger services: {e}")

        time.sleep(60)
    
    if (all_services != None) and (service_to_test in all_services):
        for service in all_services:
            if ("all" in jaeger_services) or (service in jaeger_services):
                if f"!{service}" in jaeger_services:
                    logging.debug(f"Skipping service {service}.")
                else:
                    file_to_write = os.path.join(output, f"jaeger_{service}.log")  

                    try:
                        logging.info(f"Wrinting Jaeger data for service {service}.")
                        with open(file_to_write, "a") as f:
                            request = session.get(f"{jaeger_host}/api/traces?service=" + service)
                            data = json.loads(request.content)["data"]
                            f.write(json.dumps(data, indent=2))
           
                    except Exception as e2:
                        logging.critical(f"Exception while reading Jaeger data for service {service}: {e2}")   
    else:
        logging.critical(f"Cannot store Jaeger service data.")   