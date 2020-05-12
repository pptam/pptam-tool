#!/bin/bash 

cd ./faban/master/bin/

# Make sure this command is run as sudoer
SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
    echo Running run_raban.sh with sudo...
fi
$SUDO kill $(ps aux | grep 'execute/faban' | awk '{print $2}')
$SUDO ./startup.sh