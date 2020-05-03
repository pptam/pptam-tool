# ini2json.py

## Goal

This script converts a configuration file written using the ini format into json.

## Requirements

- Python 3.7

## How to run

The script is stored in `ini2json.py` and `./ini2json.py -h` outputs the following:

```
usage: ini2json.py [-h] [--input ini_file] [--output json_file]

Converts ini files to json.

optional arguments:
  -h, --help          show this help message and exit
  --input ini_file    The file path of the ini file to read.
  --output json_file  The file path of the json file to write.
```

The script is typically called without parameters, expecting `configuration.ini` in the same folder. Otherwise, you have to call it passing the path to the input file, e.g., `./ini2json.py --input settings.ini`.
