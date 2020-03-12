# Reads a configuration file.
# Create the JSON files with the information from file.
# @author: jahic

import json 

from WriteToFile import WriteToFile
from ReadFromFile import ReadFromFile
from ParseConfiguration import ParseConfiguration

# Path to the configuration file
configurationFilePath = ""

print("Start.")

json_file = open("configurationExample.json", "w", encoding="utf-8")
configuration={}
configuration["faban"]={}
configuration["faban"]["cpuLimitation"]=90

configuration["docker"]={}
configuration["docker"]["numberOfUsers"]=1

configuration["systemUnderTest"]={}
configuration["systemUnderTest"]["IP"]="192.168.0.1"

json.dump(configuration, json_file, ensure_ascii=False)
json_file.close()

json_file = open("configurationExample.json", "r", encoding="utf-8")
configurationExample = json.load(json_file)
json_file.close()

print(configurationExample)
print(configurationExample["systemUnderTest"]["IP"])

parseConfiguration = ParseConfiguration("configuration.txt")
dictionaryConf = parseConfiguration.getJSON_Dictionary()
json_file = open("configurationExample.json", "w", encoding="utf-8")
json.dump(dictionaryConf, json_file, ensure_ascii=False)
json_file.close()
