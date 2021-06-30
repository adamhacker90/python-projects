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


with open(os.path.join(sys.path[0], 'config.json')) as json_file:
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
# print(response.text)



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



##### Get Feature Sets#####

url = "https://%s/api/v1/Features/toggle" % (ip)

payload={}
headers = {
  'Content-Type': 'text/plain',
  'Authorization': 'Bearer %s' % (token)
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

print(response.text)

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



#############ingress address
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


# Zip the files from given directory that matches the filter
def zipFilesInDir(dirName, zipFileName, filter):
   # create a ZipFile object
   with ZipFile(zipFileName, 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk(dirName):
           for filename in filenames:
               if filter(filename):
                   # create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath, basename(filePath))
                   # remove files based on filter
                   os.remove(filename)

zipFilesInDir(os.path.join(sys.path[0]), "test.zip", lambda name: date_time in name)


# #####Export to zip######
# jobid = json_response["jobId"]  
# zipurl = "https://enterprisecluster.sm.redboxdev.com:443/api/v1/DiagnosticCapture/job/%s/download" % (jobid)

# payload={}
# headers = {
# 'Accept': 'text/plain, application/json, text/json',
# 'Authorization': 'Bearer %s' % (token)
# }

# response = requests.request("GET", url, headers=headers, data=payload, verify=False)

# with open(r"c:/work projects/" + str(jobid) + ".zip", 'wb') as zip:
#     zip.write(response.content)
#     zip.flush()

# print(status)
