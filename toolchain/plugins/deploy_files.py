import logging

def get_configuration_files(current_configuration, design_path, output, test_id):
    files_to_include = current_configuration["files_to_include"]
    if files_to_include!=None and files_to_include!="":
        return files_to_include.split()
    else:
        return []
