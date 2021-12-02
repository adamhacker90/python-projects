#!/bin/bash

### Python to pull config from collector
python3 ./pull_config.py

### Python to pull logs from elastic, eventstore, Health Alerts, etc.
python ./diag.py

### Sys Variables for Configs ###
loc="/home/rbv-admin/getlogs"
log=$(date +"%Y_%m_%d_%H_%M_%S")

cd /home/rbv-admin/getlogs
### Exports the PODs logs to a .log filename ###
echo "Exporting pod logs..."
pods=$(kubectl get pods --no-headers -o custom-columns=":metadata.name")

### Grabbing POD names and Exporting the logs from the PODs, giving the file name of .log ###  
for pod in $pods ; do kubectl logs $pod >> $pod-${log}.log ; done

### Remove ip/hostname from files
python ./scrub_ip.py

### This is describing file types and compressing those file types ### 
#find . -iname '*.log' -print0 | xargs -0 tar -zcvf $loc/"MasterNode-$log.tar.gz"
tar -zcvf $loc/"MasterNode-$log.tar.gz" *.log *.json *.ini *.pem

cd $loc
### Removing all the log files from the current directory ###
rm -Rf *.log *.json *.ini *.pem

