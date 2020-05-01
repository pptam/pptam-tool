# Creates an empty file.
# If the file exists, it owerwrites it.
import os

class FileHandler: 
    fileName = ""
    # Saves file name.
    def __init__(self, name): 
        if type(name) not in [str]:
            raise TypeError("The file name must be a string.")
        self.fileName = name
        if os.path.exists(self.fileName):
            #print("The file with path:"+self.fileName+" already exists.")    
            pass        
        else:
            try:
                with open(self.fileName, 'w', encoding="utf-8") as f:
                    print("Created file "+self.fileName+".")
                    f.close()
            except:
                print("Cannot open file "+self.fileName+".")
    
    def getFileName(self):
        return self.fileName;
