import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
import sys
import os
import logging
from logging.handlers import RotatingFileHandler
 
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

# f = open(os.path.join(sys.path[0], 'config.json'))


with open(os.path.join(sys.path[0], 'config.json')) as json_file:
  data = json.load(json_file)
ipAddress = (data['Eventstore']['ipAddress'])
logger.debug(ipAddress)

while True:
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
    
    time.sleep(2)

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