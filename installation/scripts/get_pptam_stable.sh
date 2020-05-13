#!/bin/bash 
set -e

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=PPTAM%20installation
echo "  ____  ____ _____  _    __  __   _           _        _ _       _   _             ";
echo " |  _ \|  _ \_   _|/ \  |  \/  | (_)_ __  ___| |_ __ _| | | __ _| |_(_) ___  _ __  ";
echo " | |_) | |_) || | / _ \ | |\/| | | | '_ \/ __| __/ _\` | | |/ _\` | __| |/ _ \| '_ \ ";
echo " |  __/|  __/ | |/ ___ \| |  | | | | | | \__ \ || (_| | | | (_| | |_| | (_) | | | |";
echo " |_|   |_|    |_/_/   \_\_|  |_| |_|_| |_|___/\__\__,_|_|_|\__,_|\__|_|\___/|_| |_|";
echo "                                                                                   ";

# Cloning PPTAM from github
cd ~
sudo rm -rf pptam-tool
git clone https://github.com/pptam/pptam-tool.git

# Copy configuration for this specific vagrant setup
\cp /vagrant/configuration/configuration.ini ~/pptam-tool/ini2json/configuration.ini
cd ~/pptam-tool/ini2json
./ini2json.sh 

cd ~/pptam-tool
echo Done.