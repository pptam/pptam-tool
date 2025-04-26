#!/bin/bash

TT_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source "$TT_ROOT/utils.sh"

namespace="$1"

kubectl delete -f deployment/kubernetes-manifests/quickstart-k8s/yamls -n $namespace

helm ls -n $namespace | grep ts- | awk '{print $1}' | xargs helm uninstall -n $namespace

helm uninstall $rabbitmqRelease -n $namespace
helm uninstall $nacosRelease -n $namespace
helm uninstall $nacosDBRelease -n $namespace


kubectl delete -f deployment/kubernetes-manifests/skywalking -n $namespace

