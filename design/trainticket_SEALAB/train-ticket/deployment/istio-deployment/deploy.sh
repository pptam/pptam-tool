#!/usr/bin/env bash
kubectl apply -f ./train_ticket_gateway.yaml
kubectl apply -f ./destination-rule-all-v1.yaml
kubectl apply -f ./virtual-service-gateway.yaml
kubectl apply -f ./virtual-services-all-v1.yaml