#!/usr/bin/env python

import json
import sys
import argparse
from configparser import ConfigParser
import logging
from datetime import datetime
import uuid
from os import path


def covertIni2Json(iniFile, jsonOutput):
   # print("covertIni2Json: I("+iniFile+") -> O("+jsonOutput)
    parser = argparse.ArgumentParser(description="Converts ini files to json.")
    parser.add_argument("--input", metavar="ini_file", help="The file path of the ini file to read.", default=iniFile)
    parser.add_argument("--output", metavar="json_file", help="The file path of the json file to write.", default=jsonOutput)
    parser.add_argument("--logging", help="Logging level", type=int, choices=range(1, 6), default=2)
    args = parser.parse_args()
    
    logging.basicConfig(format='%(message)s', level=args.logging * 10)
    
    with open(args.input, "r") as f:
        configuration = ConfigParser()
        configuration.read_file(f)
    
    result = {}
    
    for section in configuration.sections():
        result[section] = {}
        for name, value in configuration.items(section):
            result[section][name] = [x.strip() for x in value.split() if x]
            if len(result[section][name]) == 1:
                result[section][name] = result[section][name][0]
            elif len(result[section][name]) == 0:
                result[section][name] = ''
    
    with open(args.output, "w") as f:
        f.writelines(json.dumps(result, indent=2))
    
    logging.info(f"Configuration was written to the file {args.output}.")

if __name__ == "__main__":
    # Configuration of PPTAM
    configurationTxt = "../configuration/configuration.ini"
    configurationJson = "../configuration/configuration.json"
    covertIni2Json(configurationTxt, configurationJson)
    
    # Test campaign template
    testCampaignTemplateTxt = "../configuration/testCampaignTemplate.ini"
    testCampaignTemplateJson = "../configuration/testCampaignTemplate.json"
    covertIni2Json(testCampaignTemplateTxt, testCampaignTemplateJson)
    
    # Metric measurement template
    measurementMetricTemplateTxt = "../configuration/measurementMetricTemplate.ini"
    measurementMetricTemplateJson = "../configuration/measurementMetricTemplate.json"
    covertIni2Json(measurementMetricTemplateTxt, measurementMetricTemplateJson)
    
    
    
    
    deploymentTxt = "../configuration/thirdParty/deployment.ini"
    deploymentJson = "../configuration/thirdParty/deployment.json"
    covertIni2Json(deploymentTxt, deploymentJson)
    
    executionAndMeasurementTxt = "../configuration/thirdParty/executionAndMeasurement.ini"
    executionAndMeasurementJson = "../configuration/thirdParty/executionAndMeasurement.json"
    covertIni2Json(executionAndMeasurementTxt, executionAndMeasurementJson)
    
    sutTxt = "../configuration/thirdParty/sut.ini"
    sutJson = "../configuration/thirdParty/sut.json"
    covertIni2Json(sutTxt, sutJson)    
#    testCampaignConfWithMetricConfGenerated = "../configuration/testCampaignConfWithMetricConfGenerated.ini"
#    covertIni2Json(testCampaignConfWithMetricConfGenerated, "../configuration/testCampaignConfWithMetricConfGenerated.json")