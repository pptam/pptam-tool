# README

This replication package contains the Jupyter Notebook file that executes the calculations as reported in the paper "Scalability Testing Automation using Multivariate Characterization and Detection of Software Performance Antipatterns".

## Contents

This replication package contains the following files:

- README.txt: this readme file;
- scalability-analysis.ipynb: the main file to perform the analysis;
- baseline40-80-jan2022.csv: the baseline;
- hiccup-no-stiffle-40-80v1.csv: simulation results containing a hiccup antipattern;
- expensive_db_200_30-load40-80-agg.csv: simulation results containing an expensive db antipattern;
- Files containing predicted antipattern data based on the analytical model:
  - spadata-blob.csv: predicted data for the blob antipattern;
  - spadata-continuous.csv: predicted data for the continous violated requirements antipattern;
  - spadata-empty-semi-trucks.csv: predicted data for the empty semi trucks antipattern;
  - spadata-expensive-db.csv: predicted data for the expensive db antipattern;
  - spadata-hiccups.csv: predicted data for the application hiccups antipattern;
  - spadata-stifle.csv: predicted data for the stifle antipattern;
  - spadata-traffic-jam.csv: predicted data for the traffic jam antipattern;
- spadata.csv: normalized distance and slope of the predicted data for each antipattern;

## Execution

To execute scalability-analysis.ipynb we used Visual Studio Code (https://code.visualstudio.com, version: 1.66.2) with the Jupyter Extension for Visual Studio Code (v2022.3.1000901801). Open the file scalability-analysis.ipynb and click on "Run All".

To increase replicability, we also attach the versions of the Python packages, obtained through the command "pip list > packages.txt". In case you are not able to run the Jupyter notebook without errors, please verify that you have the same versions of the python packages as we assume in our script.