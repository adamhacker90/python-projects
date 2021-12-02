# from conversa_diag.obj import token
import requests
import json
import time
from zipfile import ZipFile
from datetime import datetime
import os
from os.path import basename
import sys
import logging
from logging.handlers import RotatingFileHandler
from requests.packages.urllib3.exceptions import InsecureRequestWarning #used to allow insecure https
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #used to allow insecure https
# import paramiko
# from stat import S_ISDIR
# from getpass import getpass


# # Open a transport
# host = input("\nInput collector ip address: ")
# port = 22
# transport = paramiko.Transport((host,port))

# # Auth
# username = input("Username: ")
# password = getpass()
# transport.connect(None,username,password)

# # Go!    
# sftp = paramiko.SFTPClient.from_transport(transport) 
# print("\nLogin Successful")

# # function to pull all files in dir
# def download_dir(remote_dir, local_dir):
#     os.path.exists(local_dir) or os.makedirs(local_dir)
#     dir_items = sftp.listdir_attr(remote_dir)
#     for item in dir_items:
#         # assuming the local system is Windows and the remote system is Linux
#         # os.path.join won't help here, so construct remote_path manually
#         remote_path = remote_dir + '/' + item.filename         
#         local_path = os.path.join(local_dir, item.filename)
#         if S_ISDIR(item.st_mode):
#             download_dir(remote_path, local_path)
#         else:
#             sftp.get(remote_path, local_path)

# # Specify directories
# input_remote = input("\nSpecify directory path on server to copy: ")
# input_home = os.path.join(sys.path[0])
# # input_home = input("Specify save path on machine: ")
# download_dir(input_remote, input_home)
# print(f"\nData successfully exported to {input_home}\n")


# # # Logic for FTP  
# # print("Enter: get, put, or get_dir")
# # response = input()
# # if response == "get_dir":
# #     download_dir("/home/rbv-admin/sip-active/config","C:/Users/ahacker/Documents/config")
# # elif response == "get":
# #     filepath = input()
# #     localpath = input()
# #     sftp.get(filepath,localpath)
# # elif response == "put":
# #     filepath = input()
# #     localpath = input()
# #     sftp.put(localpath,filepath)
# # else:
# #     while response not in {"get", "put", "get_dir"}:
# #         response = input("Please enter get, put, or get_dir \n")


# # # Download single file
# # filepath = "/home/rbv-admin/sip-active/config/*"
# # localpath = "C:/Users/ahacker/Documents/config/"
# # sftp.get(filepath,localpath)

# # # Upload single file
# # filepath = "/home/foo.jpg"
# # localpath = "/home/pony.jpg"
# # sftp.put(localpath,filepath)

# # Close
# if sftp: sftp.close()
# if transport: transport.close()




# rfh = logging.handlers.RotatingFileHandler(

#     filename=(os.path.join(sys.path[0], 'log.txt')),
#     mode='a',
#     maxBytes=5*1024*1024,
#     backupCount=2,
#     encoding=None,
#     delay=0

# )
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s %(name)-25s %(levelname)-8s %(message)s",
#     datefmt="%y-%m-%d %H:%M:%S",
#     handlers=[
#         rfh
#     ]
# )

# logger = logging.getLogger('main')

# logger.debug("test")



# try:
with open(os.path.join(sys.path[0], 'config/config.json')) as json_file:
  data = json.load(json_file)
ip = (data['conversa']['ipAddress'])

#####Token Request######
url = "https://%s/identity/connect/token" % (ip)

payload='grant_type=client_credentials&client_id=credentials_grant&client_secret=Q2xpZW50IENyZWRlbnRpYWxzIEdyYW50&scope=auth_api_gateway'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)
response.json()
json_response = response.json()
token = (json_response["access_token"])
print(response.text)
# except:
#     print("Token could not be generated")


# #####Time input to specify Diag pull range#####
# print("\nInput start and end date/time:\n YYYY-MM-DDT<hour>\n Example: 2019-05-05T11\n")
# # datestart = input("start date/time: ")
# # dateend = input("end date/time: ")

# url = "https://enterprisecluster.sm.redboxdev.com:443/api/v1/DiagnosticCapture/job"

# payload = json.dumps({
#   "From": "2021-05-05T11:00:00.000000+01:00", #"%s" % (datestart),
#   "To": "2021-06-29T11:00:00.000000+01:00" #"%s" % (dateend)
# })
# headers = {
#   'Content-Type': 'application/json-patch+json',
#   'Authorization': 'Bearer %s' % (token)
# }

# response = requests.request("POST", url, headers=headers, data=payload, verify=False)
# response.json()
# json_response = response.json()


  
# status = json_response["status"]
# status2 = "Processing"
# status3 = json_response["Report already is running"][0]
# print(response.json())
# if True:
#   print(status)
# else:
#   print(status3)  



#####Health Alerts######
try:
  print("Exporting health alerts...")
  url = "https://%s:443/api/v1/alerts" % (ip)

  payload = json.dumps({
    "query": {
      "query_string": {
        "query": "*"
      }
    },
    "size": 500,
    "from": 0,
    "sort": [
      {
        "@timestamp": {
          "unmapped_type": "keyword",
          "order": "desc"
        }
      }
    ]
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json-patch+json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  response.json()
  json_response = response.json()
  now = datetime.now()
  day = now.strftime("%d")
  month = now.strftime("%m")
  year = now.strftime("%Y")
  hour = now.strftime("%H")
  minute = now.strftime("%M")
  date_time = now.strftime("%m_%d_%Y__%H_%M")
  # print(now)
  # # localtime = time.asctime( time.localtime(time.time()) )

  with open(os.path.join(sys.path[0], "conversa_alerts_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()
except:
  print("Failed exporting health alerts")


##### Get Feature Sets#####
try:
  print("Exporting feature sets...")
  url = "https://%s/api/v1/Features/toggle" % (ip)

  payload={}
  headers = {
    'Content-Type': 'text/plain',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("GET", url, headers=headers, data=payload, verify=False)

  with open(os.path.join(sys.path[0], "features_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()



  url = "https://%s/api/v1/Audit" % (ip)
  payload={}
  headers = {
    'Content-Type': 'text/plain',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "audit_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()





  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "1"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "search_playback_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()



  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "2"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "call_admin_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()





  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "3"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "recording_admin_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()


  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "4"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "health_monitoring_alerts_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()




    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "5"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "api_subscriptions_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()



    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "6"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "role_mgmt_") + str(date_time) + ".json", "w") as file:  
    file.write(response.text)
    file.flush()



  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "7"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "system_config_") + str(date_time) + ".json", "w") as file:  
    file.write(response.text)
    file.flush()




  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "8"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "transcription_") + str(date_time) + ".json", "w") as file:  
    file.write(response.text)
    file.flush()




    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "9"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "authorization_") + str(date_time) + ".json", "w") as file:     
    file.write(response.text)
    file.flush()



    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "10"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "policy_engine_") + str(date_time) + ".json", "w") as file:   
    file.write(response.text)
    file.flush()




    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "11"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "ad_metadata_capture_") + str(date_time) + ".json", "w") as file: 
    file.write(response.text)
    file.flush()




  url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "12"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "email_sending_") + str(date_time) + ".json", "w") as file: 
    file.write(response.text)
    file.flush()




    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "13"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "usage_metrics_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()




    url = "https://%s:443/api/v1/Audit" % (ip)

  payload = json.dumps({
    "sortableFilter": {
      "sortBy": "timestamp",
      "sortOrder": "desc"
    },
    "searchGroups": [
      {
        "operator": "and",
        "subGroups": [
          {
            "operator": "or",
            "searchParam": {
              "logicalOperator": "Contains",
              "field": "actionCategoryId",
              "value": "14"
            }
          }
        ]
      }
    ],
    "pageableFilter": {
      "page": 1,
      "pageSize": 500
    }
  })
  headers = {
    'Accept': 'text/plain, application/json, text/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer %s' % (token)
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)


  with open(os.path.join(sys.path[0], "diagnostic_capture_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()
except:
  print("Failed exporting feature sets")


#############ingress address/Eventstore############
try:
  print("Exporting eventstore projection status...")
  url = "http://%s:2113/projections/any" % (ip)

  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic YWRtaW46Y2hhbmdlaXQ='
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  with open(os.path.join(sys.path[0], "eventstore_projection_status_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()
except:
  print("Failed exporting eventsore projection status")


try:
  print("Exporting elastic logs...")
  url = "http://%s/elasticsearch/_cat/health" % (ip)

  payload={}
  headers = {
    'Authorization': 'Basic cmJyYWRtaW46UjhSdDM1dCE='
  }

  response = requests.request("GET", url, headers=headers, data=payload, verify=False)
  with open(os.path.join(sys.path[0], "elastic_health_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()




    url = "http://%s/elasticsearch/_cluster/state" %  (ip)

  payload={}
  headers = {
    'Authorization': 'Basic cmJyYWRtaW46UjhSdDM1dCE='
  }

  response = requests.request("GET", url, headers=headers, data=payload, verify=False)
  with open(os.path.join(sys.path[0], "elastic_cluster_state_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()






  url = "https://%s/elasticsearch/_search" % (ip)

  payload = json.dumps({
    "query": {
      "query_string": {
        "query": "*"
      }
    },
    "size": 1000,
    "from": 0,
    "sort": [
      {
        "@timestamp": {
          "unmapped_type": "keyword",
          "order": "desc"
        }
      }
    ]
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic cmJyYWRtaW46UjhSdDM1dCE='
  }

  response = requests.request("GET", url, headers=headers, data=payload, verify=False)

  response = requests.request("GET", url, headers=headers, data=payload, verify=False)
  with open(os.path.join(sys.path[0], "elastalert_error_") + str(date_time) + ".json", "w") as file:
    file.write(response.text)
    file.flush()
except:
  print("Failed exporting elastic search logs")





# # Zip the files from given directory that matches the filter
# def zipFilesInDir(dirName, zipFileName, filter):
#    # create a ZipFile object
#    with ZipFile(zipFileName, 'w') as zipObj:
#        # Iterate over all the files in directory
#        for folderName, subfolders, filenames in os.walk(dirName):
#            for filename in filenames:
#                if filter(filename):
#                    # create complete filepath of file in directory
#                    filePath = os.path.join(folderName, filename)
#                    # Add file to zip
#                    zipObj.write(filePath, basename(filePath))
#                    # remove files based on filter
#                    os.remove(filename)

# zipFilesInDir(os.path.join(sys.path[0]), "test.zip", lambda name: date_time in name)