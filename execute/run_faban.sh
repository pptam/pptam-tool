#!/bin/bash 

cd ./faban/master/bin/

# Make sure this command is run as sudoer
SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi
$SUDO ./startup.sh