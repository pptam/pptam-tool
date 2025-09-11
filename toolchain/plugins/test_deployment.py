import logging
import requests

def ready(current_configuration, design_path, output, test_id):
    cadvisor_hostname = current_configuration["cadvisor_hostname"]
    logging.debug(f"Testing if SUT is correctly deployed connecting to {cadvisor_hostname}.")

    url = f"http://{cadvisor_hostname}:8080/api/v1.3/docker/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        logging.critical(f"HTTP error when connecting to cAdvisor API: {repr(e)}")
        return False

    container_names_to_check = current_configuration["test_if_image_is_present"].split()
    found_aliases = []
    if isinstance(data, dict):
        for container_info in data.values():
            aliases = container_info.get("aliases") or []
            for alias in aliases:
                if alias:
                    found_aliases.append(alias)

    for container_name in container_names_to_check:
        if not any(container_name in alias for alias in found_aliases):
            logging.critical(f"No running container contains '{container_name}' in its name.")
            return False

    return True