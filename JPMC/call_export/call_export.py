import logging
from logging.handlers import RotatingFileHandler
import requests
import json
import time
import os
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning #used to allow insecure https
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #used to allow insecure https

 
 ####################### Logging Configuration #######################
rfh = logging.handlers.RotatingFileHandler(

    # filename=('C:/CallExport2/Exportlogs.txt'),
    filename= (os.path.join(sys.path[0], "Exportlogs") + ".txt"),
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

####################### Recorder Configuration #######################
"""
parsing config.json info 
"""
# with open('C:/CallExport2/config.json') as json_file:
with open(os.path.join(sys.path[0], "config\config.json")) as json_file:
    data = json.load(json_file)
ipAddress = (data['Recorder']['ipAddress'])
u = (data['Recorder']['login'])
p = (data['Recorder']['password'])
skip = (data['Search']['resultsToSkip'])
searchMode = (data['Search']['searchMode'])
startTime = (data['Search']['startTime'])
endTime = (data['Search']['endTime'])
fieldname = (data['Search']['criteriaList'][0]['fieldName'])
fieldData = (data['Search']['criteriaList'][0]['fieldData'])
print(ipAddress)



def search():
    """
    searches quantify api, in conjuciton with json_write(), to find and export user
    specified data
    """
    ####################### Start Search #######################
    try:
        url = "http://%s:1480/api/v1/search" % (ipAddress)
        payload = json.dumps({
        "resultsToSkip": skip,
        "searchMode": searchMode,
        "startTime": startTime,
        "endTime": endTime, 
        "criteriaList": [
            {
            "fieldName": fieldname,
            "fieldData": fieldData
            }
        ]
        })
        headers = {
            'authToken': x,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        time.sleep (30) #sleep for 1minute before asking for data



        ####################### Search Status #######################
        url = "http://%s:1480/api/v1/search/status" % (ipAddress)
        payload = {}
        headers = {
            'authToken': x
            }
        response = requests.request("GET", url, headers=headers, data=payload)
        response.json()
        total_response = response.json()
        print(total_response)
        total = total_response["resultsFound"]
        print(total)
        print(f"Found {total} results")
        logging.debug(f"Found {total} results")
        calltotal = int(total) #convert string to int 
        logging.debug(calltotal)
    


        ####################### Search Results #######################
        url = "http://%s:1480/api/v1/search/results" % (ipAddress)
        payload = {}
        headers = {
            'authToken': x
            }
        response = requests.request("GET", url, headers=headers, data=payload)
        response.json()
        jsonResponse = response.json()

        #iterate over the callIds for the total provided in status 

        startalltimer = time.perf_counter()

        for i in range(calltotal):
            start = time.perf_counter()
            response = jsonResponse["callIDs"][i]["callID"]

            logging.debug(response)
            with open(os.path.join(sys.path[0], "calls") + ".text", "a") as file:
            # with open(r"C:/CallExport2/calls.text", 'a') as file:  #Save to local file name
                file.write(str(response))
                file.write("\n")
                file.flush()

            #time.sleep(0.1)

        f = open(os.path.join(sys.path[0], "calls") + ".text", "r")
        # f = open("C:/CallExport2/calls.text", "r")
        content = f.read()
        splitcontent = content.splitlines()
        logging.debug(splitcontent)
        with open(os.path.join(sys.path[0], "calls") + ".json", "a") as fout:
        # with open("C:/CallExport2/calls.json", 'a') as fout:
            json.dump(splitcontent, fout, indent=4)
            finish = time.perf_counter()
            logging.debug(f'Search perfomed in {round(finish-start, 2)} second(s)')
        del total
        del calltotal
        
            
    except:
        logging.debug("FAILED: Couldn't parse results. Check if data is present and filter settings are correct")
        sys.exit("FAILED: Couldn't parse results. Check if data is present and filter settings are correct")
        ####################### Get Audio & Metadata #######################
    try:
        # callIds = json.loads(open('C:/CallExport2/calls.json').read())
        callIds = json.loads(open(os.path.join(sys.path[0], "calls.json")).read())
        for callId in callIds:
            loopstart1 = time.perf_counter()
            url = "http://%s:1480/api/v1/search/callaudioWav/%s" % (ipAddress,callId) #url with callId variable from json
            payload={}
            headers = {
            'authToken': x,
            'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            music = response.content
            with open(os.path.join(sys.path[0], "ExportedFiles/") + str(callId) + ".wav", "ab") as file:
            # with open(r"C:/CallExport2/ExportedFiles/"+ str(callId) + ".wav", 'ab') as file: #Save to local file name
                file.write(response.content)
                file.flush()
            loopfinish1 = time.perf_counter()
            logging.debug(f'audio downloaded for {str(callId)} {round(loopfinish1-loopstart1, 2)} second(s)')
            print(f'audio downloaded for {str(callId)} {round(loopfinish1-loopstart1, 2)} second(s)')
            url = "http://%s:1480/api/v1/search/calldetails/%s" % (ipAddress,callId) #url with callId variable from json
            payload={}
            headers = {
            'authToken': x,
            'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            music = response.content
            with open(os.path.join(sys.path[0], "ExportedFiles/") + str(callId) + ".json", "ab") as file:
            # with open(r"C:/CallExport2/ExportedFiles/"+ str(callId) + ".json", 'ab') as file: #Save to local file name
                file.write(response.content)
                file.flush()
                time.sleep(0.1) # Sleep for 1 second
    except:
        logging.debug("FAILED: something went wrong. Verify ./ExportedFiles exists")
        sys.exit("FAILED: something went wrong. Verify ./ExportedFiles exists")

    finishalltimer = time.perf_counter()
    logging.debug(f'Total time to complete {round(finishalltimer-startalltimer, 2)} second(s)')
    print(f'Total time to complete {round(finishalltimer-startalltimer, 2)} second(s)')
    

def json_write(fieldname):
    """
    modifies config.json fieldname in order to search via agentExtension,
    channel, and call guid
    """
    a_file = open(os.path.join(sys.path[0], "config\config") + ".json", "r")
    json_object = json.load(a_file)
    a_file.close()

    json_object['Search']['criteriaList'][0]['fieldName'] = str(fieldname)
    json_object['Search']['criteriaList'][0]['fieldData'] = num
    print("Searching...")

    a_file = open(os.path.join(sys.path[0], "config\config") + ".json", "w")
    json.dump(json_object, a_file)
    a_file.close()

####################### Get Token #######################
try:
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
except:
    logging.debug("[WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
    sys.exit("[WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond")
    

########## Search Logic ##########
"""
Search logic:
while true:
    try
    except
    if
    elif
    else
decisions are made in the elif and else statements (others are checking for errors),While True loop is 
then repeated in each elif/else statement for further choices
"""
agent_search= 1
guid= 2
while True:
    try:
        print("\nSpecify search option (1 or 2):")
        print("(1) Agent search\n(2) Call guid")
        user_input = int(input())
    except:
        print("Input not a number, please try again")
        # try again
        continue
    if user_input > 2:
        print("Input not 1 or 2")
    ### agent search ###
    elif user_input == 1:
        while True:
            try:
                print("\nSpecify search option (1 or 2):")
                print("(1) Extension\n(2) Channel")
                user_input = int(input())
            except:
                print("Input not a number, please try again")
                # try again
                continue
            if user_input > 2:
                print("Input not 1 or 2")
            ### Extension search ###
            elif user_input == 1:
                num = input("Input Agent Extension: ")
                json_write(19)
                search()
                break
            ### Channel search ###
            else:
                num = input("Input Channel: ")
                json_write(24)
                search()
                break
        break
    ### guid search ###
    else:
        while True:
            try:
                print("\nSpecify search option (1 or 2):")
                print("(1) Agent search\n(2) Call guid")
                user_input = int(input())
            except:
                print("Input not a number, please try again")
                # try again
                continue
            if user_input > 2:
                print("Input not 1 or 2")
            elif user_input == 1:
                num = input("Input call guid: ")
                json_write(52)
                search()
                break
            else:
                break
        break


os.remove(os.path.join(sys.path[0], "calls.json"))
os.remove(os.path.join(sys.path[0], "calls.text"))
sys.exit(0)