# Configuration of Docker execution parameters.

class DockerConfigurationData():
	# CPU limitation (CARTS_CPUS_LIMITS): parameter of docker compose, specific to socks shop, limits how many cpus the carts microservice can use.
	cpuLimit = None
	# CPU reservation (CARTS_CPUS_RESERVATIONS): parameter of docker compose, specific to socks shop, defines how many cpus are reserved for the carts microservice.
	cpuReservation = None
	# RAM limitation (CARTS_RAM_LIMITS): parameter of docker compose, specific to socks shop, limits how much RAM the carts microservice can use.
	ramLimit = None
	# RAM reservation (CARTS_RAM_RESERVATIONS): parameter of docker compose, specific to socks shop, defines how much RAM is reserved for the carts microservice.
	ramReservation = None
	# Number of replicas (CARTS_REPLICAS): parameter of docker compose, specific to socks shop, defines how much RAM is reserved for the carts microservice
	numOfReplicas = None
	
	def __init__(self, CARTS_CPUS_LIMITS, CARTS_CPUS_RESERVATIONS, CARTS_RAM_LIMITS, CARTS_RAM_RESERVATIONS, CARTS_REPLICAS): 
		self.cpuLimit=CARTS_CPUS_LIMITS
		self.cpuReservation=CARTS_CPUS_RESERVATIONS
		self.ramLimit=CARTS_RAM_LIMITS
		self.ramReservation=CARTS_RAM_RESERVATIONS
		self.numOfReplicas=CARTS_REPLICAS

	def getCpuLimit(self):
		return self.cpuLimit
	def getCpuReservation(self):
		return self.cpuReservation
	def getRamLimit(self):
		return self.ramLimit
	def getRamReservation(self):
		return self.ramReservation
	def getNumOfReplicas(self):
		return self.numOfReplicas