


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
