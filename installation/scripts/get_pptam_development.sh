#!/bin/bash 
set -e

./get_pptam_stable.sh

cd ~/pptam-tool
git checkout development
