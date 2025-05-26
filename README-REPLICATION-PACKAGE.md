# Replication Package and Appendix for the paper "An Automated Approach for the Empirical Assessment of Correlation Metrics of Architecture and Performance in Microservice Designs"

This repository contains results of the paper "An Automated Approach for the Empirical Assessment of Correlation Metrics of Architecture and Performance in Microservice Designs", which complement the results already described in the paper. Moreover, it describes the steps to replicate the obtained results.

# Results

Each microservice system studied includes its source code, dependency parsing scripts, and the generated results:

- For each studied microservice benchmarking software:
  - DeathStarBench/hotelreservation
    - the studied source code: ./design/hotelreservation/DeathStarBench/hotelReservation
    - Scripts to parse call dependencies and data dependencies:
      - ./design/hotelreservation/parse_dependencies.py
        - Results of these scripts:
            - ./design/hotelreservation/parse_call_dependencies.csv
            - ./design/hotelreservation/parse_data_dependencies.csv

  - Trainticket, version by the CUHK-SE group:
    - the studied source code: ./design/CUHK-SE/trainticket
    - Scripts to parse call dependencies and data dependencies:
      - ./design/trainticket/parse_dependencies.py. This script has to be executed with the trainticket version to analyze. In this case `./CUHK-SE`.
        - Results of these scripts:
            - ./design/CUHK-SE/parse_call_dependencies.csv
            - ./design/CUHK-SE/parse_data_dependencies.csv

  - Trainticket, version by the FUDAN group:
    - the studied source code: ./design/FUDAN/trainticket. Since we analyze two versions of the FUDAN group, there are two shell scripts to switch to the to versions using `git checkout "tags/0.2.0"` or `git checkout "tags/v1.0.0"`. After switching, the same parsing scripts are executed.
    - Scripts to parse call dependencies and data dependencies:
      - ./design/trainticket/parse_dependencies.py. This script has to be executed with the trainticket version to analyze. In this case `./FUDAN/parse_tag020` (to analyze the v0.2.0) and `./FUDAN/parse_tag100`.
        - Results of these scripts:
            - ./design/FUDAN/parse_tag020/parse_call_dependencies.csv
            - ./design/FUDAN/parse_tag020/parse_data_dependencies.csv
            - ./design/FUDAN/parse_tag100/parse_call_dependencies.csv
            - ./design/FUDAN/parse_tag100/parse_data_dependencies.csv
    
  - Trainticket, version by the SEALAB group:
    - the studied source code: ./design/SEALAB/trainticket
    - Scripts to parse call dependencies and data dependencies:
      - ./design/trainticket/parse_dependencies.py. This script has to be executed with the trainticket version to analyze. In this case `./SEALAB`.
        - Results of these scripts:
            - ./design/SEALAB/parse_call_dependencies.csv
            - ./design/SEALAB/parse_data_dependencies.csv

- Current PPTAM used to collect all performance data reported in this paper: ./toolchain
- Analysis results:
    - Call profile of Hotelreservation (Fig. 2 in the paper): ./toolchain/graph-hotelreservation.pdf
    - Call profile of CUHK_SE: ./toolchain/graph-trainticket-CUHK-SE.pdf
    - Call profile of FUDAN_tag002: ./toolchain/graph-trainticket-FUDAN_tag002.pdf
    - Call profile of FUDAN_tag100: ./toolchain/graph-trainticket-FUDAN_tag100.pdf
    - Call profile of SEALAB: ./toolchain/graph-trainticket-SEALAB.pdf

    - Mean normalized distance vs load of Hotelreservation: ./toolchain/hotelreservation-nd.pdf
    - Mean normalized distance vs load of CUHK_SE: ./toolchain/trainticket-CUHK-SE-nd.pdf
    - Mean normalized distance vs load of FUDAN_tag002: ./toolchain/trainticket-FUDAN_tag002-nd.pdf
    - Mean normalized distance vs load of FUDAN_tag100: ./toolchain/trainticket-FUDAN_tag100-nd.pdf
    - Mean normalized distance vs load of SEALAB: ./toolchain/trainticket-SEALAB-nd.pdf

    - Maximum response time vs load of Hotelreservation: ./toolchain/hotelreservation-nd.pdf
    - Maximum response time vs load of CUHK_SE: ./toolchain/trainticket-CUHK-SE-nd.pdf
    - Maximum response time vs load of FUDAN_tag002: ./toolchain/trainticket-FUDAN_tag002-nd.pdf
    - Maximum response time vs load of FUDAN_tag100: ./toolchain/trainticket-FUDAN_tag100-nd.pdf
    - Maximum response time vs load of SEALAB: ./toolchain/trainticket-SEALAB-nd.pdf

    - Slope vs normalized distance of Hotelreservation: ./toolchain/hotelreservation-slope-vs-nd.pdf
    - Slope vs normalized distance of CUHK_SE: ./toolchain/trainticket-CUHK-SE-slope-vs-nd.pdf
    - Slope vs normalized distance of FUDAN_tag002: ./toolchain/trainticket-FUDAN_tag002-slope-vs-nd.pdf
    - Slope vs normalized distance of FUDAN_tag100: ./toolchain/trainticket-FUDAN_tag100-slope-vs-nd.pdf
    - Slope vs normalized distance of SEALAB: ./toolchain/trainticket-SEALAB-slope-vs-nd.pdf

    - Performance results of Hotelreservation: ./toolchain/performance-results-hotelreservation.md
    - Performance results of CUHK_SE: ./toolchain/performance-results-trainticket-CUHK-SE.md
    - Performance results of FUDAN_tag002: ./toolchain/performance-results-trainticket-FUDAN_tag002.md
    - Performance results of FUDAN_tag100: ./toolchain/performance-results-trainticket-FUDAN_tag100.md
    - Performance results of SEALAB: ./toolchain/performance-results-trainticket-SEALAB.md

    - Performance testing results for hotelreservation: ./toolchain/executed/hotelreservation
    - Performance testing results for CUHK_SE: ./toolchain/executed/CUHK-SE-Group-TrainTicket_PPTAM_31-03-2025/executed
    - Performance testing results for FUDAN_tag002: ./toolchain/executed/FundaSELab-TrainTicket_v0.2.0_PPTAM_29-03-2025/executed
    - Performance testing results for FUDAN_tag100: ./toolchain/executed/FundaSELab-TrainTicket_v1.0.0_PPTAM_10-05-2025/executed
    - Performance testing results for SEALAB: ./toolchain/executed/SEALAB-Group-TrainTicket_PPTAM_14-04-2025/executed

    - VM stat data for three versions of the trainticket implementations
      - CPU utilization for CUHK_SE: ./toolchain/executed/CUHK-SE-Group-TrainTicket_PPTAM_31-03-2025/vmstat_physical-output_31-03-2025_CPUutil.png
      - CPU utilization for FUDAN_tag002: ./toolchain/executed/FundaSELab-TrainTicket_v0.2.0_PPTAM_29-03-2025/vmstat_physical-output_29-03-2025_CPUutil.png
      - CPU utilization for SEALAB: ./toolchain/executed/SEALAB-Group-TrainTicket_PPTAM_14-04-2025/vmstat_physical-output_14-04-2025_CPUutil.png

# Steps to replicate

Based on Fig. 1 of the paper, the steps to replicate the results are as follows:

1. Measure the performance of each microservice in each studied software
2. Identify antipatterns in the communication structure among these microservices
3. Study the correlation of low performance with architectural antipatterns 

## Step 1: Measure the performance of each microservice in each studied software using PPTAM

For this step, we used PPTAM, an open source tool to conduct performance studies. PPTAM requires the creation of "design" folders in which all data for each test is contained. We used these design folders to store also the data we needed in our study.

The following design folders are present:
- ./design/hotelreservation
- ./design/SEALAB
- ./design/FUDAN (with the scripts ./design/trainticket/FUDAN/switch_to_tag002.sh and ./design/trainticket/FUDAN/switch_to_tag100.sh to switch versions)
- ./design/CUHK-SE

The response times for each benchmarking application are then obtained running the test scenarios defined in the locustfile.py defined in each design folder.
To run PPTAM, run ./toolchain/execute.py, indicating the design folder to execute. The results will be stored in the ./toolchain/executed folder. 

## Step 2: 

### Step 2a: extract dependencies between microservices through parsing

Prerequisites:
- Docker installed
- Python 3 installed (for running the parse_dependencies.py script)
- Maven dependencies cached locally (~/.m2)

Steps:

1. Build the Projects

    ```
    cd ./design/trainticket/CUHK-SE/trainticket/ && docker run --platform linux/amd64 -it --rm -v $(pwd):/usr/src/mymaven -v ~/.m2:/root/.m2 -w /usr/src/mymaven maven:3.6.3-openjdk-8 mvn clean install -Dmaven.test.skip=true
    
    cd ../../SEALAB/trainticket/ && docker run --platform linux/amd64 -it --rm -v $(pwd):/usr/src/mymaven -v ~/.m2:/root/.m2 -w /usr/src/mymaven maven:3.6.3-openjdk-8 mvn clean install -Dmaven.test.skip=true
    
    cd ../../FUDAN/trainticket/ && switch_to_tag002.sh && docker run --platform linux/amd64 -it --rm -v $(pwd):/usr/src/mymaven -v ~/.m2:/root/.m2 -w /usr/src/mymaven maven:3.6.3-openjdk-8 mvn clean install -Dmaven.test.skip=true
    ```
    For FUDAN, after all is calculated, run ./design/trainticket/FUDAN/switch_to_tag100.sh and repeat the calculations.

2. Calculate Dependencies

    Use the provided Python script parse_dependencies.py to extract dependencies for each project:

    ```
    ./design/trainticket/parse_dependencies.py ./CUHK-SE
    ./design/trainticket/parse_dependencies.py ./FUDAN/parse_tag002
    ./design/trainticket/parse_dependencies.py ./FUDAN/parse_tag100
    ./design/trainticket/parse_dependencies.py ./SEALAB
    ./design/hotelreservation/parse_dependencies.py
    ```

    Notes:
    - The maven:3.6.3-openjdk-8 image is used to ensure compatibility with the projects.
    - The -Dmaven.test.skip=true flag is used to skip tests during build to speed up the process.
    - Ensure that the parse_dependencies.py script is executable (chmod +x parse_dependencies.py) if needed.

### Step 2b: study antipatterns using DV8

Convert the parsed dependencies to the DV8 format, first the calls:

```
./calls2dv8.py ../design/hotelreservation/call_dependencies.csv ./call_dependencies-hotelreservation.json
./calls2dv8.py ../design/trainticket/CUHK-SE/call_dependencies.csv ./call_dependencies-trainticket-CUHK-SE.json
./calls2dv8.py ../design/trainticket/FUDAN/parse_tag002/call_dependencies.csv ./call_dependencies-trainticket-FUDAN_tag002.json
./calls2dv8.py ../design/trainticket/FUDAN/parse_tag100/call_dependencies.csv ./call_dependencies-trainticket-FUDAN_tag100.json
./calls2dv8.py ../design/trainticket/SEALAB/call_dependencies.csv ./call_dependencies-trainticket-SEALAB.json
```

Then convert data dependencies (when microservices use the same data structures they pass eachother): 

```
./datadependencies2dv8.py ../design/hotelreservation/data_dependencies.csv ./data_dependencies-hotelreservation.json
./datadependencies2dv8.py ../design/trainticket/CUHK-SE/data_dependencies.csv ./data_dependencies-trainticket-CUHK-SE.json
./datadependencies2dv8.py ../design/trainticket/FUDAN/parse_tag002/data_dependencies.csv ./data_dependencies-trainticket-FUDAN_tag002.json
./datadependencies2dv8.py ../design/trainticket/FUDAN/parse_tag100/data_dependencies.csv ./data_dependencies-trainticket-FUDAN_tag100.json
./datadependencies2dv8.py ../design/trainticket/SEALAB/data_dependencies.csv ./data_dependencies-trainticket-SEALAB.json
```

Now convert the extracted data to a matrix:

```
/Applications/DV8/bin/dv8-console core:convert-matrix ./call_dependencies-hotelreservation.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./call_dependencies-trainticket-CUHK-SE.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./call_dependencies-trainticket-FUDAN_tag002.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./call_dependencies-trainticket-FUDAN_tag100.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./call_dependencies-trainticket-SEALAB.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./data_dependencies-hotelreservation.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./data_dependencies-trainticket-CUHK-SE.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./data_dependencies-trainticket-FUDAN_tag002.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./data_dependencies-trainticket-FUDAN_tag100.json
/Applications/DV8/bin/dv8-console core:convert-matrix ./data_dependencies-trainticket-SEALAB.json
```

And merge all dependencies into one single matrix:

```
/Applications/DV8/bin/dv8-console core:merge-matrix -outputFile dependencies-trainticket-CUHK-SE.dv8-dsm ./call_dependencies-trainticket-CUHK-SE.dv8-dsm ./data_dependencies-trainticket-CUHK-SE.dv8-dsm
/Applications/DV8/bin/dv8-console core:merge-matrix -outputFile dependencies-trainticket-FUDAN_tag002.dv8-dsm ./call_dependencies-trainticket-FUDAN_tag002.dv8-dsm ./data_dependencies-trainticket-FUDAN_tag002.dv8-dsm
/Applications/DV8/bin/dv8-console core:merge-matrix -outputFile dependencies-trainticket-FUDAN_tag100.dv8-dsm ./call_dependencies-trainticket-FUDAN_tag100.dv8-dsm ./data_dependencies-trainticket-FUDAN_tag100.dv8-dsm
/Applications/DV8/bin/dv8-console core:merge-matrix -outputFile dependencies-trainticket-SEALAB.dv8-dsm ./call_dependencies-trainticket-SEALAB.dv8-dsm ./data_dependencies-trainticket-SEALAB.dv8-dsm
```

Now, let's identify antipatterns (e.g., cliques):

```
mkdir dv8-hotelreservation
mkdir dv8-trainticket-CUHK-SE
mkdir dv8-trainticket-FUDAN_tag002
mkdir dv8-trainticket-FUDAN_tag100
mkdir dv8-trainticket-SEALAB

/Applications/DV8/bin/dv8-console arch-issue -outputFolder ./dv8-hotelreservation ./dependencies-hotelreservation.dv8-dsm  
/Applications/DV8/bin/dv8-console arch-issue -outputFolder ./dv8-trainticket-CUHK-SE ./dependencies-trainticket-CUHK-SE.dv8-dsm
/Applications/DV8/bin/dv8-console arch-issue -outputFolder ./dv8-trainticket-FUDAN_tag002 ./dependencies-trainticket-FUDAN_tag002.dv8-dsm
/Applications/DV8/bin/dv8-console arch-issue -outputFolder ./dv8-trainticket-FUDAN_tag100 ./dependencies-trainticket-FUDAN_tag100.dv8-dsm
/Applications/DV8/bin/dv8-console arch-issue -outputFolder ./dv8-trainticket-SEALAB ./dependencies-trainticket-SEALAB.dv8-dsm
```

## Step 3: Study the correlation of low performance with architectural antipatterns 

Let's visualize all calls between microservices:

```
./calls2graph2.py ../design/hotelreservation/call_dependencies.csv ./graph-hotelreservation.pdf --width 2 --cropleft 7 --cropbottom 10 --cropright 7 --croptop 5 --optimizeorder
./calls2graph2.py ../design/trainticket/CUHK-SE/call_dependencies.csv ./graph-trainticket-CUHK-SE.pdf --width 6.5 --cropleft 18 --cropbottom 10 --cropright 16 --croptop 5
./calls2graph2.py ../design/trainticket/FUDAN/parse_tag002/call_dependencies.csv ./graph-trainticket-FUDAN_tag002.pdf --width 6.5 --cropleft 18 --cropbottom 10 --cropright 17.1 --croptop 5
./calls2graph2.py ../design/trainticket/FUDAN/parse_tag100/call_dependencies.csv ./graph-trainticket-FUDAN_tag100.pdf --width 6.5 --cropleft 18 --cropbottom 10 --cropright 17.1 --croptop 5
./calls2graph2.py ../design/trainticket/SEALAB/call_dependencies.csv ./graph-trainticket-SEALAB.pdf --width 6.5 --cropleft 18 --cropbottom 10 --cropright 17 --croptop 5 
```

We now execute ./toolchain/analyze_performance_correlation.ipynb for each design folder and obtain the various charts and tables described above. The following instructions are just for formatting purposes:

```
./crop.py --cropleft 8 --cropright 4 --croptop 8 --cropbottom 8 ./hotelreservation-max_response_times.pdf ./hotelreservation-max_response_times2.pdf
./crop.py --cropleft 8 --cropright 4 --croptop 8 --cropbottom 8 ./hotelreservation-nd.pdf ./hotelreservation-nd2.pdf
./crop.py --cropleft 1 --cropright 8 --croptop 8 --cropbottom 8 ./hotelreservation-slope-vs-nd.pdf ./hotelreservation-slope-vs-nd2.pdf
rm hotelreservation-max_response_times.pdf 
rm hotelreservation-nd.pdf 
rm hotelreservation-slope-vs-nd.pdf 
mv hotelreservation-max_response_times2.pdf hotelreservation-max_response_times.pdf
mv hotelreservation-nd2.pdf hotelreservation-nd.pdf
mv hotelreservation-slope-vs-nd2.pdf hotelreservation-slope-vs-nd.pdf

./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-CUHK-SE-max_response_times.pdf trainticket-CUHK-SE-max_response_times2.pdf
./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-CUHK-SE-nd.pdf trainticket-CUHK-SE-nd2.pdf
./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-CUHK-SE-slope-vs-nd.pdf trainticket-CUHK-SE-slope-vs-nd2.pdf
rm trainticket-CUHK-SE-max_response_times.pdf 
rm trainticket-CUHK-SE-nd.pdf 
rm trainticket-CUHK-SE-slope-vs-nd.pdf 
mv trainticket-CUHK-SE-max_response_times2.pdf trainticket-CUHK-SE-max_response_times.pdf
mv trainticket-CUHK-SE-nd2.pdf trainticket-CUHK-SE-nd.pdf
mv trainticket-CUHK-SE-slope-vs-nd2.pdf trainticket-CUHK-SE-slope-vs-nd.pdf

./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-FUDAN-max_response_times.pdf trainticket-FUDAN-max_response_times2.pdf
./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-FUDAN-nd.pdf trainticket-FUDAN-nd2.pdf
./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-FUDAN-slope-vs-nd.pdf trainticket-FUDAN-slope-vs-nd2.pdf
rm trainticket-FUDAN-max_response_times.pdf 
rm trainticket-FUDAN-nd.pdf 
rm trainticket-FUDAN-slope-vs-nd.pdf 
mv trainticket-FUDAN-max_response_times2.pdf trainticket-FUDAN-max_response_times.pdf
mv trainticket-FUDAN-nd2.pdf trainticket-FUDAN-nd.pdf
mv trainticket-FUDAN-slope-vs-nd2.pdf trainticket-FUDAN-slope-vs-nd.pdf

./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-SEALAB-max_response_times.pdf trainticket-SEALAB-max_response_times2.pdf
./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-SEALAB-nd.pdf trainticket-SEALAB-nd2.pdf
./crop.py --cropleft 8 --cropright 8 --croptop 8 --cropbottom 8 trainticket-SEALAB-slope-vs-nd.pdf trainticket-SEALAB-slope-vs-nd2.pdf
rm trainticket-SEALAB-max_response_times.pdf 
rm trainticket-SEALAB-nd.pdf 
rm trainticket-SEALAB-slope-vs-nd.pdf 
mv trainticket-SEALAB-max_response_times2.pdf trainticket-SEALAB-max_response_times.pdf
mv trainticket-SEALAB-nd2.pdf trainticket-SEALAB-nd.pdf
mv trainticket-SEALAB-slope-vs-nd2.pdf trainticket-SEALAB-slope-vs-nd.pdf