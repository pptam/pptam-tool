#!/bin/bash

TT_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source "$TT_ROOT/utils.sh"



namespace="$1"
args="$2"

argNone=1
argDB=0
argMonitoring=0
argTracing=0
argAll=0

function quick_start {
  echo "quick start"
  deploy_infrastructures  $namespace
  deploy_tt_mysql_all_in_one  $namespace
  deploy_tt_secret  $namespace
  deploy_tt_svc $namespace
  deploy_tt_dp  $namespace
}

function deploy_all {
  deploy_infrastructures  $namespace
  deploy_tt_mysql_each_service  $namespace
  deploy_tt_secret  $namespace
  deploy_tt_svc $namespace
  deploy_tt_dp_sw  $namespace
  deploy_tracing  $namespace
  deploy_monitoring
}


function deploy {
    if [ $argNone == 1 ]; then
      quick_start
      exit $?
    fi

    if [ $argAll == 1 ]; then
      deploy_all
      exit $?
    fi

    deploy_infrastructures $namespace

    if [ $argDB == 1 ]; then
      deploy_tt_mysql_each_service  $namespace
    else
      deploy_tt_mysql_all_in_one $namespace
    fi

    deploy_tt_secret  $namespace
    deploy_tt_svc $namespace

    if [ $argTracing == 1 ]; then
      deploy_tt_dp_sw  $namespace
      deploy_tracing  $namespace
    else
      deploy_tt_dp $namespace
    fi

    if [ $argMonitoring == 1 ]; then
      deploy_monitoring
    fi
}

#deploy
function parse_args {
    echo "Parse DeployArgs"
    for arg in $args
    do
      echo $arg
      case $arg in
      "--all")
        argAll=1
        ;;
      "--independent-db")
        argDB=1
        ;;
      "--with-monitoring")
        argMonitoring=1
        ;;
      "--with-tracing")
        argTracing=1
        ;;
      esac
    done
}

echo "args num: $#"
if [ $# == 2 ]; then
  argNone=0
  parse_args $args
fi
deploy