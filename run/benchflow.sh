#!/bin/bash

# set -ex
set -e

#-----Configuration details-----#
PROPERTY_FILE=config.properties
#-----Configuration details-----#

#-----Set the correct tools if we are on OSX-----#
# DESCRIPTION OF PROBLEM: Implementations of sed, readlink, zcat, etc. are different on OS X and Linux.
# SOURCE: https://gist.github.com/bittner/5436f3dc011d43ab7551

# cross-OS compatibility (greadlink, gsed, zcat are GNU implementations for OS X)
[[ `uname` == 'Darwin' ]] && {
  which greadlink gsed gzcat > /dev/null && {
    export PATH=/usr/local/opt/coreutils/libexec/gnubin:$PATH
  } || {
    echo 'ERROR: GNU utils required for Mac. You may use homebrew to install them: brew install coreutils gnu-sed'
    exit 1
  }
}
#-----Set the correct tools if we are on OSX-----#

#-----Helper function----#

function resolve_path()
{
  local resolved=$(eval "readlink -f "$1"")
  if [[ -e "$resolved" ]]
  then
    echo "$resolved"  
  else
    echo "$1"
  fi
}  

function getProperty() {
   PROP_KEY=$1
   PROP_VALUE=`cat $PROPERTY_FILE | grep "$PROP_KEY" | cut -d'=' -f2`
   echo $PROP_VALUE
}

#-----Helper function----#

#-----Get commands and arguments-----#

RESOLVEDARGS=()
for var in "$@"
do
  resolved=$(resolve_path "$var")
  len=${#RESOLVEDARGS[@]}
  RESOLVEDARGS["$len"]="$resolved"
done

#-----Get commands and arguments-----#

#-----Business Logic functions----#

function generate_test()
{

  if [ "$#" -ne 6 ]; then
    echo "Expected 6 Parameters, passed: $@" >&2
    exit 1
  fi

  # Set configurations
  NUM_USERS=$1
  CARTS_REPLICAS=$2
  CARTS_CPUS_LIMITS=$3
  CARTS_CPUS_RESERVATIONS=$4
  CARTS_RAM_LIMITS=$5
  CARTS_RAM_RESERVATIONS=$6

  # Get a new test id
  TEST_ID=$(cat /dev/urandom | env LC_CTYPE=C tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

  echo "The generated test ID is $TEST_ID"

  # Configure the template for this test in the tmp folder
  rm -rf ./drivers/tmp/*
  cp -aR ./templates/faban/driver/ecsa/* ./drivers/tmp/

  # Configure the Faban driver
  FABAN_IP=$(getProperty "faban.ip")
  JAVA_HOME_FABAN=$(getProperty "java.home")
  sed -i.bak 's/${FABAN_IP}/'$FABAN_IP'/' ./drivers/tmp/build.properties
  sed -i.bak 's/${TEST_NAME}/'$TEST_ID'/' ./drivers/tmp/build.properties
  sed -i.bak 's/${JAVA_HOME_FABAN}/'$JAVA_HOME_FABAN'/' ./drivers/tmp/build.xml
  rm ./drivers/tmp/build.properties.bak
  rm ./drivers/tmp/build.xml.bak

  # Deploy
  sed -i.bak 's/${TEST_NAME}/'$TEST_ID'/' ./drivers/tmp/deploy/run.xml
  sed -i.bak 's/${FABAN_IP}/'$FABAN_IP'/' ./drivers/tmp/deploy/run.xml
  sed -i.bak 's/${JAVA_HOME_FABAN}/'$JAVA_HOME_FABAN'/' ./drivers/tmp/deploy/run.xml
  sed -i.bak 's/${NUM_USERS}/'$NUM_USERS'/' ./drivers/tmp/deploy/run.xml
  FABAN_OUTPUT_DIR=$(getProperty "faban.output.dir")
  sed -i.bak 's/${FABAN_OUTPUT_DIR}/'$FABAN_OUTPUT_DIR'/' ./drivers/tmp/deploy/run.xml
  SUT_IP=$(getProperty "sut.ip")
  sed -i.bak 's/${SUT_IP}/'$SUT_IP'/' ./drivers/tmp/deploy/run.xml
  SUT_PORT=$(getProperty "sut.port")
  sed -i.bak 's/${SUT_PORT}/'$SUT_PORT'/' ./drivers/tmp/deploy/run.xml
  # Config (just replace with the one generated for deploy)
  yes | cp -rf ./drivers/tmp/deploy/run.xml ./drivers/tmp/config/run.xml

  rm ./drivers/tmp/deploy/run.xml.bak

  sed -i.bak 's/${TEST_NAME}/'$TEST_ID'/' ./drivers/tmp/src/ecsa/driver/WebDriver.java
  rm ./drivers/tmp/src/ecsa/driver/WebDriver.java.bak

  # Configure the deployment descriptor
  SUT_HOSTNAME=$(getProperty "sut.hostname")
  cp -aR ./templates/deployment_descriptor/template/docker-compose.yml ./drivers/tmp/deploy
  sed -i.bak 's/${SUT_HOSTNAME}/'$SUT_HOSTNAME'/' ./drivers/tmp/deploy/docker-compose.yml
  sed -i.bak 's/${CARTS_REPLICAS}/'$CARTS_REPLICAS'/' ./drivers/tmp/deploy/docker-compose.yml
  sed -i.bak 's/${CARTS_CPUS_LIMITS}/'$CARTS_CPUS_LIMITS'/' ./drivers/tmp/deploy/docker-compose.yml
  sed -i.bak 's/${CARTS_CPUS_RESERVATIONS}/'$CARTS_CPUS_RESERVATIONS'/' ./drivers/tmp/deploy/docker-compose.yml
  sed -i.bak 's/${CARTS_RAM_LIMITS}/'$CARTS_RAM_LIMITS'/' ./drivers/tmp/deploy/docker-compose.yml
  sed -i.bak 's/${CARTS_RAM_RESERVATIONS}/'$CARTS_RAM_RESERVATIONS'/' ./drivers/tmp/deploy/docker-compose.yml

  rm ./drivers/tmp/deploy/docker-compose.yml.bak

  # create a folder for the new test and copy the tmp data
  mkdir -p ./drivers/$TEST_ID
  cp -aR ./drivers/tmp/* ./drivers/$TEST_ID
  rm -rf ./drivers/tmp/*

  # Compile and package for deploy the faban driver
  echo "Compiling the Faban driver"
  cwd=$(pwd)
  cd ./drivers/$TEST_ID
  ant deploy.jar
  cd "$cwd"

  # create a folder for the test
  mkdir -p ./to_execute/$TEST_ID
  # copy the driver jarm run.xml and deployment descriptor
  cp ./drivers/$TEST_ID/build/$TEST_ID.jar ./to_execute/$TEST_ID
  cp ./drivers/$TEST_ID/config/run.xml ./to_execute/$TEST_ID
  cp ./drivers/$TEST_ID/deploy/docker-compose.yml ./to_execute/$TEST_ID
  
}

function execute_tests()
{

  FABAN_IP=$(getProperty "faban.ip")
  FABAN_MASTER="http://$FABAN_IP:9980/";

  FABAN_CLIENT="./faban/benchflow-faban-client/target/benchflow-faban-client.jar"

  SUT_IP=$(getProperty "sut.ip")
  #STAT_COLLECTOR_PORT=$(getProperty "stat.collector.port")

  for D in `find ./to_execute/* -type d`; do
      if [ -d "${D}" ]; then
          arrD=(${D//\// })
          TEST_ID=${arrD[2]} 
          echo "Starting test: $TEST_ID"

          echo "Deploying the system under test"

          # deploy the system under test
          cwd=$(pwd)
          cd ./to_execute/$TEST_ID/
          docker stack deploy --compose-file=docker-compose.yml $TEST_ID
          # wait for the system under test to be ready
          echo "Waiting for the system to be ready"
          sleep 120
          export TEST_ID
          # BUGGY, docker service logs hangs sometimes, we have to find a better solution instead
          #CARTS_LOGS=$(docker service logs ${TEST_ID}_carts --tail all)
          cd "$cwd"

          #if [[ $CARTS_LOGS != *"initialization completed in"* ]]; then
          #  echo "The system under test did not start correclty"
          #  # undeploy the system under test
          #  cwd=$(pwd)
          #  cd ./to_execute/$TEST_ID/
          #  docker stack rm $TEST_ID
          #  cd "$cwd"
          #  continue
          #fi

          # IF the system successfully deployed, then start the test

          test_name=$TEST_ID
          driver="to_execute/$TEST_ID/$TEST_ID.jar"
          driver_conf="to_execute/$TEST_ID/run.xml"
          deployment_descriptor="to_execute/$TEST_ID/docker-compose.yml"

          echo "Deploying the load driver"

          # Deploy and start the test
          java -jar $FABAN_CLIENT $FABAN_MASTER deploy $test_name $driver $driver_conf | (read RUN_ID ; echo $RUN_ID > RUN_ID.txt)

          RUN_ID=$(cat RUN_ID.txt)
          # cleanup
          rm RUN_ID.txt

          echo "Run ID: $RUN_ID"

          # Start the resource data collection
          #echo "Data collection: "
          #curl http://$SUT_IP:$STAT_COLLECTOR_PORT/start
          #echo ""

          STATUS=""

          # For testing using Mirai
          MIRAI_STARTED=0
          SECONDS=0
          echo "Waiting for the test to be completed"

          # Wait for the test to be done
          while [ "$STATUS" != "COMPLETED" ] && [ "$STATUS" != "FAILED" ]
          do
              # Get test status
              java -jar ./faban/benchflow-faban-client/target/benchflow-faban-client.jar $FABAN_MASTER status $RUN_ID | (read STATUS ; echo $STATUS > STATUS.txt)
              STATUS=$(cat STATUS.txt)
              echo "Current STATUS: $STATUS"

              # Only used for testing with Mirai
              if [ "$STATUS" == "STARTED" ]
              then
                duration=$SECONDS
                echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."

                if [ $MIRAI_STARTED -eq 0 ]
                then

                  if [ $SECONDS -gt 180 ] 
                  then
                  #echo "RUN MIRAI!!!!"
                  MIRAI_STARTED=1

                  #../miraibot/miraibot -t 1200 -a HTTP -i 10.7.20.69 24 256 &
                  fi
                fi
              fi

              # cleanup
              rm STATUS.txt

              sleep 60
          done

          # Stop the resource data collection and store the data
          #echo "Data collection: "
          #curl http://$SUT_IP:$STAT_COLLECTOR_PORT/stop
          #echo ""

          echo "Undeploying the system under test"

          # undeploy the system under test
          cwd=$(pwd)
          cd ./to_execute/$TEST_ID/
          docker stack rm $TEST_ID
          # be sure everything is clean
          docker stack rm $(docker stack ls --format "{{.Name}}") || true
          docker rm -f -v $(docker ps -a -q) || true
          cd "$cwd"

          # saving test results
          echo "Saving test results"
          mkdir -p ./executed/$TEST_ID/faban
          java -jar ./faban/benchflow-faban-client/target/benchflow-faban-client.jar $FABAN_MASTER info $RUN_ID > executed/$TEST_ID/faban/runInfo.txt

	        cp ./faban/output/$RUN_ID/summary.xml ./executed/$TEST_ID/faban/summary.xml
          cp ./faban/output/$RUN_ID/detail.xan ./executed/$TEST_ID/faban/detail.xan
          cp ./faban/output/$RUN_ID/log.xml ./executed/$TEST_ID/faban/log.xml
          #mkdir -p ./executed/$TEST_ID/stats
          # curl http://$SUT_IP:$STAT_COLLECTOR_PORT/data > executed/$TEST_ID/stats/cpu.txt
          #cp ./services/stats/cpu.txt ./executed/$TEST_ID/stats/cpu.txt

          mv ./to_execute/$TEST_ID/ ./executed/$TEST_ID/definition

      fi
  done

}

function help_me()
{
  echo "Usage Examples: "
  echo ""
  echo "Generate Test: ./benchflow.sh generate_test <NUM_USERS> <CARTS_REPLICAS> <CARTS_CPUS_LIMITS> <CARTS_CPUS_RESERVATIONS> <CARTS_RAM_LIMITS> <CARTS_RAM_RESERVATIONS>"
  echo "Execute Tests (on Console): ./benchflow.sh execute_tests"
  echo "Execute Tests (background): nohup ./benchflow.sh execute_tests > log.out 2> log.err &"
}

#-----Business Logic functions----#

#-----Function selector----#

if [[ ! -z "$1" ]]
then
  if [[ "help" == "$1" ]]
  then
     (help_me)
  elif ( [[ "generate_test" == "$1" ]])
  then
    # NUM_USERS=$2
    # CARTS_REPLICAS=$3
    # CARTS_CPUS_LIMITS=$4
    # CARTS_CPUS_RESERVATIONS=$5
    # CARTS_RAM_LIMITS=$6
    # CARTS_RAM_RESERVATIONS=$7
     (generate_test $2 $3 $4 $5 $6 $7)
  elif ( [[ "execute_tests" == "$1" ]])
  then
     (execute_tests)
  fi
fi

#-----Function selector----#
