#!/bin/bash
FOLDER="../design_trainticket_FUDAN/parse_tag100"
CSV_PATH="$FOLDER/service_calls.csv"

if [[ ! -f "$CSV_PATH" ]]; then
  echo "Error: $CSV_PATH not found!" >&2
  exit 2
fi

echo "Running convertcalls2dv8.py with $CSV_PATH..."
python3 convertcalls2dv8.py "$CSV_PATH" "Call"

# /Applications/DV8/bin/dv8-console core:convert-matrix ./service_calls.json 
# /Applications/DV8/bin/dv8-console arch-issue -cliqueDepends * -outputFolder ./dv8 ./service_calls.dv8-dsm 
