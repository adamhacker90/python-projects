import requests
import time
import sys
import os
import json
from getpass import getpass

username = input("Username: ")
password = getpass()

### Send email ###
def send_email(SUBJECT, TEXT):

    import smtplib

    gmail_user = username
    gmail_pwd = password
    FROM = "redboxdaemon@gmail.com"
    TO = ["ahacker@redboxvoice.com" ]
    
    ### Prepare message ###
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    ### Connect to SMTP and send ###
    try:
        #server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.quit()
        server.close()
        print('successfully sent mail')
    except:
        print("failed to send mail")  

### API Status Check ###
try:
    while True:
    ### Login ###
        with open(os.path.join(sys.path[0], "config\config.json")) as json_file:
            data = json.load(json_file)
        ip = (data['Recorder']['ipAddress'])
        u = (data['Recorder']['login'])
        p = (data['Recorder']['password'])

        url = "http://%s:1480/api/v1/sessions/login" % (ip)

        payload = ""
        headers = {
        'username': u,
        'password': p
        } 

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        time1 = response.elapsed.total_seconds()
        status = response.status_code
        # print(response)
        # print(status)
        # print(time)

    ### Logic Check ###
        print("\nAttempting to connect, may take up to 45 seconds...\n")
        if status != 200:     
            print(f"status: {status}, closing connection")
            response.close()
            send_email("API connection failure", f"Status code other than 200 OK recieved status: {status}. Trying again in 15 minutes")
            time.sleep(5)
            break

        elif time1 > 45:
            print("Connection attempt exceeded 45 seconds")
            response.close()
            send_email("API connection failure", "Connection attempt exceeded 45 seconds")
            time.sleep(5)
            
        else:
            print(f"Connected:\n{response.text}\n{status} OK\n{time1} seconds")
            time.sleep(5)
                  
except:
    print("Something went wrong, could not connect")
    send_email("API connection failure", "Could not initiate connection to the server or program was terminated.")