@echo off
call python ini2json.py 
call python create_test.py
::call python create_test.py --configuration ../configuration/configuration.json %1 %2 %3 %4 %5 %6 %7 %8 %9