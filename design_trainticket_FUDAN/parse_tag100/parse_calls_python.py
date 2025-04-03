import os
import re

def extract_service_names(root_dir, subfolders):
    pattern = re.compile(r'http://(ts-[a-zA-Z0-9\-]+-service)')
    service_names = {}

    for subfolder in subfolders:
        full_path = os.path.join(root_dir, subfolder)
        for dirpath, _, filenames in os.walk(full_path):
            for filename in filenames:
                if filename.endswith(".py"):
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

def main():
    root_folder = "../train-ticket"

    subfolders_to_traverse = [
        "ts-voucher-service"
    ]

    results = extract_service_names(root_folder, subfolders_to_traverse)

    lines = []
    for subfolder in sorted(results.keys()):
        for service in sorted(set(results[subfolder])):
            lines.append([subfolder, service])

    return lines

if __name__ == "__main__":
    for line in main():
        print(line)
