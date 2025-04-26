#!/usr/bin/env bash
kubectl label namespace default istio-injection=enabled
kubectl apply -f ts-deployment-part1.yml

kubectl apply -f ts-deployment-part2-1.yml
kubectl apply -f ts-deployment-part2-2.yml
kubectl apply -f ts-deployment-part3.yml

kubectl apply -f ts-service-part1.yml
kubectl apply -f ts-service-part2-1.yml
kubectl apply -f ts-service-part2-2.yml
kubectl apply -f ts-service-part3.yml