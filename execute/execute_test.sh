#!/bin/bash 

# Make sure this command is run as sudoer, which is required for the docker commands within the script.
SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
    echo Running execute_test.py with sudo...
fi
$SUDO ./execute_test.py --configuration ../configuration/configuration.json $1 $2 $3 $4 $5 $6 $7 $8 $9



