#!/bin/bash 
cd ./executed
for n in *; do printf './store.py --skip-history ./executed/%s\n' "$n"; done > ../store_to_do.sh
chmod uog+x ../store_to_do.sh
cd ..
bash ./store_to_do.sh
rm ./store_to_do.sh