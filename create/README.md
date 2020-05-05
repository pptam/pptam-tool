# create_test.py

## Goal

This script creates test cases based on the template files stored in the folder `templates`.

## Requirements

- Python 3.7

## How to run

The script is stored in `create_test.py` and `./create_test.py -h` outputs the following:

```
usage: create_test.py [-h] [--configuration path_to_configuration_file]
                      [--logging {1,2,3,4,5}]
                      [--overwrite key=value [key=value ...]]

Creates test cases.

optional arguments:
  -h, --help            show this help message and exit
  --configuration path_to_configuration_file
                        Configuration file
  --logging {1,2,3,4,5}
                        Logging level
  --overwrite key=value [key=value ...]
                        Configuration values, which overwrite the values in
                        the configuration file. Format: name1=value1
                        name2=value2 ...
```

The script is typically called without parameters, expecting `configuration.json` in the same folder. Otherwise, you have to call it passing the path to the configuration file, e.g., `./create_test.py --configuration ../ini2json/configuration.json`.
