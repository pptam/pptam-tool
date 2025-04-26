#!/usr/bin/env bash
kubectl delete -f ./virtual-services-all-v1.yaml
kubectl delete -f ./destination-rule-all-v1.yaml
kubectl delete -f ./virtual-service-gateway.yaml
kubectl delete -f ./train_ticket_gateway.yaml