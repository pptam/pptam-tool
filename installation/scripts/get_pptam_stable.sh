#!/bin/bash 
set -e

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=PPTAM%20Setup
echo "  ____  ____ _____  _    __  __   ____       _               ";
echo " |  _ \|  _ \_   _|/ \  |  \/  | / ___|  ___| |_ _   _ _ __  ";
echo " | |_) | |_) || | / _ \ | |\/| | \___ \ / _ \ __| | | | '_ \ ";
echo " |  __/|  __/ | |/ ___ \| |  | |  ___) |  __/ |_| |_| | |_) |";
echo " |_|   |_|    |_/_/   \_\_|  |_| |____/ \___|\__|\__,_| .__/ ";
echo "                                                      |_|    ";

# Cloning PPTAM from github
cd ~
sudo rm -rf pptam-tool
git clone https://github.com/pptam/pptam-tool.git

# Copy configuration for this specific vagrant setup
\cp /vagrant/configuration/configuration.ini ~/pptam-tool/configuration/configuration.ini
cd ~/pptam-tool/configuration
./ini2json.sh 

cd ~/pptam-tool
echo Done.