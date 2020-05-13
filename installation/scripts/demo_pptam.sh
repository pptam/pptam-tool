#!/bin/bash 
set -e

clear

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=PPTAM%20demo
echo "  ____  ____ _____  _    __  __       _                      ";
echo " |  _ \|  _ \_   _|/ \  |  \/  |   __| | ___ _ __ ___   ___  ";
echo " | |_) | |_) || | / _ \ | |\/| |  / _\` |/ _ \ '_ \` _ \ / _ \ ";
echo " |  __/|  __/ | |/ ___ \| |  | | | (_| |  __/ | | | | | (_) |";
echo " |_|   |_|    |_/_/   \_\_|  |_|  \__,_|\___|_| |_| |_|\___/ ";
echo "                                                             ";

echo "This script demonstrates the execution of PPTAM. Moreover, it is a good starting point to construct your own testing infrastructure." | fold -w 80 -s 
echo
echo "To use PPTAM, one has to define which software has to be studied. The so called \"software under test\" (SUT) has to be deployable using Docker Compose (https://docs.docker.com/compose/). For this demo, the software \"Sock Shop\" (https://github.com/microservices-demo/microservices-demo) has already been set up."  | fold -w 80 -s 
echo
read -p "Press enter to continue"
echo
echo "Before we start, we need to install PPTAM. To do this, we run the following commands:" | fold -w 80 -s 
echo "cd /vagrant/scripts/"
echo "./get_pptam_development.sh"
echo
echo "The second " | fold -w 80 -s 

