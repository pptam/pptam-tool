@echo off
cd ../ini2json
call python ini2json.py 
cd ../create
call python create_test.py --configuration ../ini2json/configuration.json %1 %2 %3 %4 %5 %6 %7 %8 %9