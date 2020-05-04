#!/bin/bash 
cd ../ini2json
./ini2json.py 
cd ../create
./create_test.py --configuration ../ini2json/configuration.json $1 $2 $3 $4 $5 $6 $7 $8 $9