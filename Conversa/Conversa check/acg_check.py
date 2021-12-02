import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from pprint import pprint
import paramiko

###Logging
rfh = logging.handlers.RotatingFileHandler(

    filename=(os.path.join(sys.path[0], 'log.txt')),
    mode='a',
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding=None,
    delay=0

)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-25s %(levelname)-8s %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[
        rfh
    ]
)

logger = logging.getLogger('main')

logger.debug("test")

# # f = open(os.path.join(sys.path[0], 'config.json'))

####Open json of eventstore projection names
with open(os.path.join(sys.path[0], 'config.json')) as json_file:
  data = json.load(json_file)
ipAddress = (data['Eventstore']['ipAddress'])
logger.debug(ipAddress)

###Search through eventstore and verify if running
count = 0
while count <= 1:
  count+=1
  projections = json.loads(open(os.path.join(sys.path[0], 'projections.json')).read())
  for projection in projections: 
    url = "http://%s:2113/projection/%s/statistics" % (ipAddress, projection)

    payload={}
    headers = {
      'Accept': 'application/json',
      'Authorization': 'Basic YWRtaW46Y2hhbmdlaXQ='
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    localtime = time.asctime( time.localtime(time.time()) )
    


    response.json()

    json_response = response.json()
    logger.debug(str(projection) + "  status = " + json_response["projections"][0]["status"] ) 
    print(str(projection) + "  status = " + json_response["projections"][0]["status"])
    time.sleep(1)


    ###If not running, restart
    #print(json_response["projections"][0]["status"])
    prstate1 = json_response["projections"][0]["status"]
    prstate2 = "Running"
    if prstate1 != prstate2:
      url = "http://%s:2113/projection/%s/command/enable" % (ipAddress,projection)

      payload={}
      headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46Y2hhbmdlaXQ='
      }

      response = requests.request("POST", url, headers=headers, data=payload)
      logger.debug(response.text, + " " + "Projection Restarted")
      print(response.text, + " " + "Projection Restarted")
    

print("Done")


url = "http://%s:2113/subscriptions" % (ipAddress)

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Basic YWRtaW46Y2hhbmdlaXQ='
}

response = requests.request("GET", url, headers=headers, data=payload)
response.json()
json_response = response.json()

messages = [
  { "eventStreamId": value["eventStreamId"],
    "averageItemsPerSecond": value["averageItemsPerSecond"],
    "totalItemsProcessed": value["totalItemsProcessed"],
    "lastProcessedEventNumber": value["lastProcessedEventNumber"],
    "lastKnownEventNumber": value["lastKnownEventNumber"],
    "connectionCount": value["connectionCount"]
  } for value in json_response
]

pprint(messages, sort_dicts=False)


host = "172.16.250.75"
port = 22
username = "rbv-admin"
password = "install"

c1 = "kubectl get pods"
c2 = "kubectl get events"
c3 = "kubectl logs nats-cluster-0"
c4 = "df -h"
c5 = "top -b -n1"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

stdin, stdout, stderr = ssh.exec_command(c1)
lines = stdout.readlines()
pprint(lines)
print("\n")

stdin, stdout, stderr = ssh.exec_command(c2)
lines = stdout.readlines()
pprint(lines)
print("\n")

stdin, stdout, stderr = ssh.exec_command(c3)
lines = stdout.readlines()
pprint(lines)
print("\n")

stdin, stdout, stderr = ssh.exec_command(c4)
lines = stdout.readlines()
pprint(lines)
print("\n")

stdin, stdout, stderr = ssh.exec_command(c5)
lines = stdout.readlines()
pprint(lines)
