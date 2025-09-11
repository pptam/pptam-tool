#!/bin/bash 

# http://patorjk.com/software/taag/#p=display&c=echo&f=Standard&t=PPTAM%20Setup
echo "  ____  ____ _____  _    __  __   ____       _               ";
echo " |  _ \\|  _ \\_   _|/ \\  |  \\/  | / ___|  ___| |_ _   _ _ __  ";
echo " | |_) | |_) || | / _ \\ | |\\/| | \\___ \\ / _ \\ __| | | | '_ \\ ";
echo " |  __/|  __/ | |/ ___ \\| |  | |  ___) |  __/ |_| |_| | |_) |";
echo " |_|   |_|    |_/_/   \\_\\_|  |_| |____/ \\___|\\__|\\__,_| .__/ ";
echo "                                                      |_|    ";

# Cloning PPTAM from github
cd ~
git clone --depth 1 https://github.com/pptam/pptam-tool.git

cd pptam-tool
echo Done.