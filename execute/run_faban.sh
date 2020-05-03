#!/bin/bash 

cd ./faban/master/bin/

SUDO=''
if (( $EUID != 0 )); then
    SUDO='sudo'
fi
$SUDO ./startup.sh