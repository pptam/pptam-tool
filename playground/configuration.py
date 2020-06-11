#!/usr/bin/env python
import configparser

config = configparser.ConfigParser()
config.read("../design/configuration.ini")
print(config["DEFAULT"].keys())