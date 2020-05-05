# execute_test.py

## Goal

This script executes test cases based on the tests defined using `create_test`.

## Requirements

- Python 3.7

## How to run

The script is stored in `execute_test.py` and `./execute_test.py -h` outputs the following:

```
usage: execute_test.py [-h] [--configuration path_to_configuration_file]
                       [--logging {1,2,3,4,5}]

Executes test cases.

optional arguments:
  -h, --help            show this help message and exit
  --configuration path_to_configuration_file
                        Configuration file
  --logging {1,2,3,4,5}
                        Logging level
```

The script is typically called without parameters, expecting `configuration.json` in the same folder. Otherwise, you have to call it passing the path to the configuration file, e.g., `./execute_test.py --configuration ../ini2json/configuration.json`.
