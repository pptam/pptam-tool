import logging
import os
import requests
import json

def after(current_configuration, output, test_id): 
    session = requests.Session()
    session.headers.update({'accept': 'application/json'})
    session.headers.update({'content-type': 'application/json'})

    jaeger_host = current_configuration["jaeger_host_url"]
    jaeger_services = current_configuration["jaeger_services"].split(" ")
    
    service_request = session.get(f"{jaeger_host}/api/services")
    all_services = json.loads(service_request.content)["data"]

    for service in all_services:
        if (any("all" in s for s in jaeger_services) or any(service in s for s in jaeger_services)):
            file_to_write = os.path.join(output, f"jaeger_{service}.log")  

            with open(file_to_write, "a") as f:
                request = session.get(f"{jaeger_host}/api/traces?service=" + service)
                data = json.loads(request.content)["data"]
                f.write(json.dumps(data, indent=2))
            
