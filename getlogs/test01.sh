#!/usr/bin/env bash

DEPLOYMENT=$1

for p in $(kubectl get pods | grep ^${DEPLOYMENT}- | cut -f 1 -d ' '); do 
    echo --------------------------- 
    echo $p 
    echo --------------------------- 
    kubectl logs $p
done
