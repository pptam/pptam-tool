import os


def extract_data_dependencies(root_folder, subfolders_to_traverse, entity_folder):
    # Step 1: Extract entity names from entity_folder
    entity_files = [f for f in os.listdir(entity_folder) if os.path.isfile(os.path.join(entity_folder, f)) and f.endswith(".java")]
    entity_names = {os.path.splitext(f)[0] for f in entity_files}

    entity_prefix = "edu.fudan.common.entity."
    entity_imports = {name: f"import {entity_prefix}{name};" for name in entity_names}

    # Step 2: Traverse subfolders and look for those import statements
    results = {}

    for subfolder in subfolders_to_traverse:
        subfolder_path = os.path.join(root_folder, subfolder)
        subfolder_results = []

        for dirpath, _, filenames in os.walk(subfolder_path):
            for filename in filenames:
                if filename.endswith(".java"):
                    filepath = os.path.join(dirpath, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as file:
                            content = file.read()
                            for entity_name, import_stmt in entity_imports.items():
                                if import_stmt in content:
                                    subfolder_results.append(entity_name)
                    except Exception as e:
                        print(f"Failed to read {filepath}: {e}")

        if subfolder_results:
            results[subfolder] = subfolder_results

    return results


def main():
    root_folder = "./train-ticket"
    entity_folder = os.path.join(root_folder, "ts-common/src/main/java/edu/fudan/common/entity/")

    subfolders_to_traverse = ["ts-assurance-service", "ts-auth-service", "ts-basic-service", "ts-cancel-service", "ts-config-service", "ts-consign-price-service", "ts-consign-service", "ts-contacts-service", "ts-delivery-service", "ts-execute-service", "ts-food-delivery-service", "ts-food-service", "ts-gateway-service", "ts-inside-payment-service", "ts-notification-service", "ts-order-other-service", "ts-order-service", "ts-payment-service", "ts-preserve-other-service", "ts-preserve-service", "ts-price-service", "ts-rebook-service", "ts-route-plan-service", "ts-route-service", "ts-seat-service", "ts-security-service", "ts-station-food-service", "ts-station-service", "ts-train-food-service", "ts-train-service", "ts-travel-plan-service", "ts-travel-service", "ts-travel2-service", "ts-user-service", "ts-verification-code-service", "ts-wait-order-service"]
    results = extract_data_dependencies(root_folder, subfolders_to_traverse, entity_folder)
    return results


if __name__ == "__main__":
    for line in main():
        print(line)
