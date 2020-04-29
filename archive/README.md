# Tool for Production and Performance Testing Based Application Monitoring (pptam)

## Installation

The detailed installation instructions can be found in the file [Installation.md](Installation.md).

## Usage of the system

Once installed, the instructions on how to use the installed tools can be found in the file [Usage.md](Usage.md).

## Attributions
- This work has been partly supported by eSulab\-Solutions, Inc., the German Federal Ministry of Education and Research (ContinuITy project, grant 01IS17010), and the Italian Ministry of Education, Universities and Research (GAUSS project, grant 2015KWREMX). 
- The icon for the PPTAM organization was downloaded from https://www.flaticon.com/free-icon/speedometer_610106 and was made by https://www.flaticon.com/authors/vectors-market from www.flaticon.com.

## Configuration parameters
### PPTAM
- TEST_ID
- RUN_ID

### Faban
- FABAN_IP
- JAVA_HOME_FABAN
- FABAN_OUTPUT_DIR
- FABAN_MASTER
- FABAN_CLIENT
- CPU limitation (CARTS_CPUS_LIMITS):
- CPU reservation (CARTS_CPUS_RESERVATIONS):
- RAM limitation (CARTS_RAM_LIMITS):
- RAM reservation (CARTS_RAM_RESERVATIONS):

### Docker
- Number of users (NUM_USERS):
- Number of replicas (CARTS_REPLICAS):

### System under test
- System under test IP (SUT_IP):
- System under test port (SUT_PORT):
- System under test host name (SUT_HOSTNAME):