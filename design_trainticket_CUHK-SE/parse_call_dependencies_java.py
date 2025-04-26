#!/usr/bin/env python3

import os
import re

def extract_service_dependencies(root_dir, subfolders):
    pattern = re.compile(r'getServiceUrl\s*\(\s*"([^"]+)"\s*\)')
    service_names = {}

    for subfolder in subfolders:
        full_path = os.path.join(root_dir, subfolder)
        for dirpath, _, filenames in os.walk(full_path):
            for filename in filenames:
                if filename.endswith("Impl.java"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.readlines()
                            for line in content:
                                if line.lstrip().startswith("//"):
                                    continue
                                matches = pattern.findall(line)
                                if matches:
                                    if subfolder not in service_names:
                                        service_names[subfolder] = []
                                    service_names[subfolder].extend(matches)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    return service_names

def run_analysis():
    root_folder = "./train-ticket"

    # We included all ts-*-service folders and excluded 
    # - the admin services since we are not interested in coupling with administrative services
    # - ts-avatar-service since it does not call any other service
    # - ts-news-service since it is written in GO
    # - ts-ticket-office-service since it is written in JavaScript
    # - ts-voucher-service since it is written in Python
    subfolders_to_traverse = [
        "ts-assurance-service", 
        "ts-auth-service", 
        "ts-basic-service", 
        "ts-cancel-service", 
        "ts-config-service", 
        "ts-consign-price-service", 
        "ts-consign-service", 
        "ts-contacts-service", 
        "ts-delivery-service", 
        "ts-execute-service", 
        "ts-food-delivery-service", 
        "ts-food-service", 
        "ts-gateway-service", 
        "ts-inside-payment-service", 
        "ts-notification-service", 
        "ts-order-other-service", 
        "ts-order-service", 
        "ts-payment-service", 
        "ts-preserve-other-service", 
        "ts-preserve-service", 
        "ts-price-service", 
        "ts-rebook-service", 
        "ts-route-plan-service", 
        "ts-route-service", 
        "ts-seat-service", 
        "ts-security-service", 
        "ts-station-food-service", 
        "ts-station-service", 
        "ts-train-food-service", 
        "ts-train-service", 
        "ts-travel-plan-service", 
        "ts-travel-service", 
        "ts-travel2-service", 
        "ts-user-service", 
        "ts-verification-code-service", 
        "ts-wait-order-service"
    ]

    results = extract_service_dependencies(root_folder, subfolders_to_traverse)

    lines = []
    for subfolder in sorted(results.keys()):
        for service in sorted(set(results[subfolder])):
            lines.append([subfolder, service])

    return lines

if __name__ == "__main__":
    for line in run_analysis():
        print(";".join(line))
