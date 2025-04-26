#!/usr/bin/env bash
kubectl delete -f ts-service-part1.yml
kubectl delete -f ts-service-part2-1.yml
kubectl delete -f ts-service-part2-2.yml
kubectl delete -f ts-service-part3.yml
kubectl delete -f ts-deployment-part1.yml
kubectl delete -f ts-deployment-part2-1.yml
kubectl delete -f ts-deployment-part2-2.yml
kubectl delete -f ts-deployment-part3.yml



