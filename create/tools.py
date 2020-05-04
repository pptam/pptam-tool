def replace_values_in_file(file, replacements):
    for replacement in replacements:
        replace_value_in_file(file, replacement["search_for"], replacement["replace_with"])


def replace_value_in_file(file, search_for, replace_with):
    with open(file, "r") as f:
        content = f.read()
        content = content.replace(search_for, replace_with)
    with open(file, "w") as f:
        f.write(content)