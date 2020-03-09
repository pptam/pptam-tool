# Test basic file operations: write and read.
# Test overwrite option in write.
# To run this test, in terminal run: python -m unittest FileHandler_test
import unittest

from FileHandler import FileHandler
from WriteToFile import WriteToFile
from ReadFromFile import ReadFromFile

class FileHandler_test(unittest.TestCase):
	def test_FileHandlerContructorGetFileName(self):
		fileName = "testFile.txt"
		fileHandler = FileHandler(fileName);
		self.assertEqual(fileHandler.getFileName(), fileName)

	def test_write_read(self):
		fileName = "testFile.txt"
		writeToFile = WriteToFile(fileName)
		writeToFile.writeLine("Test1")
		readFromFile = ReadFromFile(fileName)
		readFromFile = readFromFile.readLines()
		self.assertTrue(readFromFile)
	
	def test_overwrite_read(self):
		fileName = "testFile.txt"
		writeToFile = WriteToFile(fileName)
		writeToFile.writeLine("Test1")
		writeToFile.overwriteTheExistingFile()
		readFromFile = ReadFromFile(fileName)
		readFromFile = readFromFile.readLines()
		self.assertFalse(readFromFile)
