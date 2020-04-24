# Common methods for manipulations with files.
from distutils.dir_util import copy_tree
import random
import string
import os
import shutil
import subprocess


from configurationParser.ReadFromFile import ReadFromFile
from configurationParser.WriteToFile import WriteToFile

class CommonMethods: 
    # Saves file name.
    def __init__(self): 
        #print("CommonMethods created.")
        pass
    
        # Create folder with relative path.
    def createFolderRelPath(self, path):
        try:
            # Create target Directory
            os.mkdir(path)
            print("Directory " , path ,  " Created ")
        except FileExistsError:
            print("Directory " , path ,  " already exists")

    # Copy all files and folders from a folder to a folder.
    def copyFromFolder2Folder(self, folderOriginRelPath, folderTargetRelPath):
        currentPath = self.getCurrentPath()
        #print("copyFromFolder2Folder::folderOriginRelPath="+folderOriginRelPath)
        #print("copyFromFolder2Folder::folderTargetRelPath="+folderTargetRelPath)
        folderOriginAbsPath = os.path.join(currentPath, folderOriginRelPath)
        folderTargetAbsPath = os.path.join(currentPath, folderTargetRelPath)
        #print("copyFromFolder2Folder::folderOriginAbsPath="+folderOriginAbsPath)
        #print("copyFromFolder2Folder::folderTargetAbsPath="+folderTargetAbsPath)
        if not os.path.isdir(folderOriginAbsPath):
            print(folderOriginAbsPath+" -- no such path!")
            return
        if not os.path.isdir(folderTargetAbsPath):
            print(folderTargetAbsPath+" -- no such path!")
            return
        # Copy all from origin to destination.
        try:
            copy_tree(folderOriginAbsPath, folderTargetAbsPath)
            print("Copy "+folderOriginAbsPath+"->"+folderTargetAbsPath+" - SUCCESSFUL")
        
        except Exception as e:
            print(e)
            print("Copy failed.")

    # Move all files and folders from a folder to a folder.
    def moveFromFolder2Folder(self, folderOriginRelPath, folderTargetRelPath):
        currentPath = self.getCurrentPath()
        folderOriginAbsPath = os.path.join(currentPath, folderOriginRelPath)
        folderTargetAbsPath = os.path.join(currentPath, folderTargetRelPath)

        filesToMove = os.listdir(folderOriginRelPath)
        
        for f in filesToMove:
            shutil.move(folderOriginAbsPath+f, folderTargetRelPath)

    def removeFileRelativePath(self, pathRel):
        currentPath = self.getCurrentPath()
        pathAbs = os.path.join(currentPath, pathRel)
        #print("Remove all from "+pathAbs+".")
        
        if not os.path.isfile(pathAbs):
            print("[WARNING] CommonMethods::removeFileRelativePath::File " + pathAbs + " does not exist.")
            return
        else:
            try:
                os.remove(pathAbs)
                print("CommonMethods::removeFileRelativePath::File " + pathAbs + " - DELETED")
            except:
                print("[WARNING] CommonMethods::removeFileRelativePath::Cannot delete file " + pathAbs + ".")

    # Create temp file, instead of replacing the existing file.
    def replaceValueInFileWithTempFile(self, paramPlaceHolder, paramValue, pathToBuildProperties):
        readFromFile = None
        
        if (os.path.isfile(pathToBuildProperties+".tmp")):
            readFromFile = ReadFromFile(pathToBuildProperties+".tmp")
        elif (os.path.isfile(pathToBuildProperties)):
            readFromFile = ReadFromFile(pathToBuildProperties)
        else:
            print("replaceValueInFileWithTempFile:No file at "+pathToBuildProperties+".")
            return

        #print("Try to replace " + paramPlaceHolder + " with " + paramValue + ".")

        newFileDictionary = []

        # Rewrite the file
        # Attention: there could be several instances to replace. Replace them all.
        for line in readFromFile.readLines():
            if (paramPlaceHolder in line):
                line = line.replace(paramPlaceHolder,paramValue)
                #print("    Replace " + paramPlaceHolder + " with " + paramValue + ".")
                #print("    Result: " + line + ".")
            #else:
                #print("Line "+line+" does not contain "+paramPlaceHolder+".")

            newFileDictionary.append(line)

        pathToBuildPropertiesTmp = pathToBuildProperties+".tmp"
        writeToFile = WriteToFile(pathToBuildPropertiesTmp)
        writeToFile.overwriteTheExistingFile()

        for line in newFileDictionary:
            writeToFile.writeLine(line)

        for line in readFromFile.readLines():
            print(line)

        readFromFileTmp = ReadFromFile(pathToBuildPropertiesTmp)
        for line in readFromFile.readLines():
            print(line)

    # Read file, replace the value, overwrite the file.
    def replaceValueInFileRelPath(self, paramPlaceHolder, paramValue, pathToFileOrigin):
        readFromFile = None

        currentPath = self.getCurrentPath()
        pathToFileOriginAbs = os.path.join(currentPath, pathToFileOrigin)
        
        if (os.path.isfile(pathToFileOriginAbs)):
            readFromFile = ReadFromFile(pathToFileOriginAbs)
            # print("replaceValueInFileRelPath "+pathToFileOriginAbs+".")
        else:
            print("replaceValueInFileRelPath: No file at "+pathToFileOriginAbs+" !!!")
            return

        #print("Try to replace " + paramPlaceHolder + " with " + paramValue + ".")

        newFileDictionary = []

        # Rewrite the file
        # Attention: there could be several instances to replace. Replace them all.
        for line in readFromFile.readLines():
            if (paramPlaceHolder in line):
                line = line.replace(paramPlaceHolder,paramValue)
                #print("    Replace " + paramPlaceHolder + " with " + paramValue + ".")
                #print("    Result: " + line + ".")
            #else:
                #print("Line "+line+" does not contain "+paramPlaceHolder+".")

            newFileDictionary.append(line)

        writeToFile = WriteToFile(pathToFileOrigin)
        writeToFile.overwriteTheExistingFile()

        for line in newFileDictionary:
            writeToFile.writeLine(line)

        #for line in readFromFile.readLines():
            #print(line)

        #readFromFileTmp = ReadFromFile(pathToBuildPropertiesTmp)
        #for line in readFromFile.readLines():
            #print(line)

    def copyFile(self, fileOriginAbsPath, fileTargetAbsPath):

        #print("Copy from "+fileOriginAbsPath+" -> " +fileTargetAbsPath)
        if not os.path.isfile(fileOriginAbsPath):
            print(fileOriginAbsPath+" -- no such file!")
            return
        if not os.path.isdir(fileTargetAbsPath):
            print(fileTargetAbsPath+" -- no such target dir!")
            return
        # Copy all from origin to destination.
        try:
            shutil.copy2(fileOriginAbsPath, fileTargetAbsPath)
        except:
            print("Copy failed.")

    def copyFileRel(self, fileOriginRelPath, fileTargetRelPath):
        currentPath = self.getCurrentPath()
        fileOriginAbsPath = os.path.join(currentPath, fileOriginRelPath)
        fileTargetAbsPath = os.path.join(currentPath, fileTargetRelPath)

        #print("Copy from "+fileOriginAbsPath+" -> " +fileTargetAbsPath)
        if not os.path.isfile(fileOriginAbsPath):
            print(fileOriginAbsPath+" -- no such file!")
            return
        if not os.path.isdir(fileTargetAbsPath):
            print(fileTargetAbsPath+" -- no such target dir!")
            return
        # Copy all from origin to destination.
        try:
            shutil.copy2(fileOriginAbsPath, fileTargetAbsPath)
        except:
            print("Copy failed.")

    def randomString(self, stringLength):
        # Generate a random string of fixed length.
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join(random.choice(letters) for i in range(stringLength))
    
    # Get current path.
    def getCurrentPath(self):
        return os.path.dirname(os.path.abspath(__file__))

    # Delete all files from folder.
    def deleteFilesFromFolder(self, folderPath):
        for filename in os.listdir(folderPath):
            file_path = os.path.join(folderPath, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
                return
        print("Folder "+folderPath+" cleansed!")
