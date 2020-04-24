# Read from file (file that was passed as a constructor).
# Copy line per line into an array of strings.

from FileHandler import FileHandler

class ReadFromFile(FileHandler):
    def __init__(self, name):
        FileHandler.__init__(self, name)
        #super(FileHandler, self).__init__(name)

    def readLines(self): 
        # Open file.
        print("Try to open "+self.fileName)
        f = open(self.fileName, "r")
        print(f.readline())
        try:
            with open(self.fileName, "r") as f:
                content = f.readlines()
                print("Content")
                # Remove whitespace characters like `\n` at the end of each line.
                content = [x.strip() for x in content] 
                f.close()
                return content
        except:
            print("Cannot read from file "+self.fileName+"-")
            return -1