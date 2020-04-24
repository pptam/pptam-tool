# Configuration of Faban execution parameters.

class FabanConfigurationData():
	# Number of users (NUM_USERS): Number of users generated to simulate the test.
	numberOfUsers = None
	
	def __init__(self, NUM_USERS): 
		self.numberOfUsers=NUM_USERS

	def getNumberOfUsers(self):
		return self.numberOfUsers
