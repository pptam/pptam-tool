#!/bin/bash 

cd ./faban/master/bin/

# Make sure this command is run as sudoer, which is required for the docker commands within the script.
SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi
$SUDO /startup.sh

cd ../../../

