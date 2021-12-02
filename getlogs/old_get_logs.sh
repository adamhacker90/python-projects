#!/bin/bash
loc="/home/rbv-admin/getlogs"
log=`date +%m%d%y` # Today's date

cd /home/rbv-admin/getlogs
pods=$(kubectl get pods --no-headers -o custom-columns=":metadata.name")

for pod in $pods ; do kubectl logs $pod >> $pod.log ; done

cd /home/rbv-admin/getlogs
find $loc | xargs tar -zcvf "$(date '+%Y-%m-%d').tar.gz"


