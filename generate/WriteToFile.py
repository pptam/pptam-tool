# Write to file (file name used as a constructor).
# Write line per line.
# Add lines at the end of the file.
from generate.FileHandler import FileHandler


class WriteToFile(FileHandler):
    def __init__(self, name):
        FileHandler.__init__(self, name)

    def writeLine(self, lineToWrite):
        # Open file and append lines.
        try:
            with open(self.fileName, 'a') as f:
                f.write(lineToWrite+"\n")
                f.close()
        except:
            print("Cannot write to file "+self.fileName+"-")

    # Create a new file.
    def overwriteTheExistingFile(self):
        open(self.fileName, 'w')
