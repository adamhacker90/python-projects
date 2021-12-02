import logging
from logging.handlers import RotatingFileHandler
import requests
import json
import time
import os
import sys
import names
import uuid
import random as r
from requests.packages.urllib3.exceptions import InsecureRequestWarning #used to allow insecure https
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #used to allow insecure https


 
 ####################### Logging Configuration #######################
rfh = logging.handlers.RotatingFileHandler(

    filename=('C:/CallAnnotate/Exportlogs.txt'),
    mode='a',
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding=None,
    delay=0

)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-5s %(levelname)-5s %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[
        rfh
    ]
)

logger = logging.getLogger('main')

logger.debug("test")


if os.path.exists("C:/CallAnnotate/calls.text"):
      os.remove("C:/CallAnnotate/calls.text")
else:
  print("calls.txt is not present - proceeding")

if os.path.exists("C:/CallAnnotate/calls.json"):
      os.remove("C:/CallAnnotate/calls.json")
else:
  print("calls.json is not present - proceeding")



####################### Recorder Configuration #######################
with open('C:/CallAnnotate/config.json') as json_file:
    data = json.load(json_file)
ipAddress = (data['Recorder']['ipAddress'])
u = (data['Recorder']['login'])
p = (data['Recorder']['password'])
skip = (data['Search']['resultsToSkip'])
searchMode = (data['Search']['searchMode'])
startTime = (data['Search']['startTime'])
endTime = (data['Search']['endTime'])

####################### Get Token #######################
url = "http://%s:1480/api/v1/sessions/login" % (ipAddress)
payload = ""
headers = {
  'username': u,
  'password': p
}
response = requests.request("POST", url, headers=headers, data=payload)
response.json()
jsonResponse = response.json()
x = (jsonResponse["authToken"])
print(x)

####################### Annotate #######################

for callId in range(2366,91040):
  loopstart1 = time.perf_counter()
  username = names.get_full_name()
  #callIdvalue = callId
  ph_no = []
  ph_no.append(r.randint(6, 9))
  for i in range(1, 10):
    ph_no.append(r.randint(0, 9)) 
  for i in ph_no:
      print(i, end="")
  telephoneNumber = i
  
  url = "http://%s:1480/api/v1/annotation/call" % (ipAddress) #url with callId variable from json
  payload= json.dumps({
  "callID": "%s" % (callId),
  "annotationFields": [
    {
      "fieldName": "96",
      "fieldData": "%s" % (username)
    },
    {
      "fieldName": "20",
      "fieldData": "%s" % (telephoneNumber)
    },
    {
      "fieldName": "1001",
      "fieldData": "%s" % str(uuid.uuid4())
    },
    {
      "fieldName": "221",
      "fieldData": "%s" % str(uuid.uuid4())
    }
    ]
  })
  headers = {
  'authToken': x,
  'Content-Type': 'application/json'
  }
  response = requests.request("POST", url, headers=headers, data=payload)
  time.sleep(0.1) # Sleep for 1 second



finishalltimer = time.perf_counter()
#logging.debug(f'Total time to complete {round(finishalltimer-startalltimer, 2)} second(s)')
