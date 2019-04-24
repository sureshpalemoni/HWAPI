#!/bin/bash
kubectl create -f k8s/secret.yml 
kubectl create -f k8s/postgres.yaml
kubectl create -f k8s/helloworld.yaml
