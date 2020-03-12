# Read from file (file that was passed as a constructor).
# Create a Python dictionary, ready for writting to a JSON file.

from FileHandler import FileHandler
from ReadFromFile import ReadFromFile

class ParseConfiguration(FileHandler):
    def __init__(self, name):
        FileHandler.__init__(self, name)
	
    def getJSON_Dictionary(self):
        readFromFile = ReadFromFile(self.fileName)
        # Dictionary.
        configurationJSON={}
        configurationJSON["PPTAM_Configuration"]={}
        configurationJSON["Faban_Configuration"]={}
        configurationJSON["Docker_Configuration"]={}
        for line in readFromFile.readLines():
            # Avoid comments and empty spaces.
            if line.startswith("#") or len(line)==0:
                continue
            print(line)
            if line.startswith("FABAN_IP"):
                FABAN_IP = line.split("=")
                configurationJSON["PPTAM_Configuration"]["FABAN_IP"]=FABAN_IP[1]
                print("Add FABAN IP to the configuration.")
            elif line.startswith("FABAN_IP"):
                FABAN_IP = line.split("=")
                configurationJSON["PPTAM_Configuration"]["FABAN_IP"]=FABAN_IP[1]
            print("New step")
        return configurationJSON
