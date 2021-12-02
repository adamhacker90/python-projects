import paramiko
from stat import S_ISDIR
from getpass import getpass
import os
import sys

# Open a transport
host = input("\nInput collector ip address: ")
port = 22
transport = paramiko.Transport((host,port))

# Auth
username = input("Username: ")
password = getpass()
transport.connect(None,username,password)

# Go!    
sftp = paramiko.SFTPClient.from_transport(transport) 
print("\nLogin Successful")

# function to pull all files in dir
def download_dir(remote_dir, local_dir):
    os.path.exists(local_dir) or os.makedirs(local_dir)
    dir_items = sftp.listdir_attr(remote_dir)
    for item in dir_items:
        # assuming the local system is Windows and the remote system is Linux
        # os.path.join won't help here, so construct remote_path manually
        remote_path = remote_dir + '/' + item.filename         
        local_path = os.path.join(local_dir, item.filename)
        if S_ISDIR(item.st_mode):
            download_dir(remote_path, local_path)
        else:
            sftp.get(remote_path, local_path)

# Specify directories
input_remote = input("\nSpecify directory path on server to copy: ")
input_home = os.path.join(sys.path[0])
# input_home = input("Specify save path on machine: ")
download_dir(input_remote, input_home)
print(f"\nData successfully exported to {input_home}\n")


# # Logic for FTP  
# print("Enter: get, put, or get_dir")
# response = input()
# if response == "get_dir":
#     download_dir("/home/rbv-admin/sip-active/config","C:/Users/ahacker/Documents/config")
# elif response == "get":
#     filepath = input()
#     localpath = input()
#     sftp.get(filepath,localpath)
# elif response == "put":
#     filepath = input()
#     localpath = input()
#     sftp.put(localpath,filepath)
# else:
#     while response not in {"get", "put", "get_dir"}:
#         response = input("Please enter get, put, or get_dir \n")


# # Download single file
# filepath = "/home/rbv-admin/sip-active/config/*"
# localpath = "C:/Users/ahacker/Documents/config/"
# sftp.get(filepath,localpath)

# # Upload single file
# filepath = "/home/foo.jpg"
# localpath = "/home/pony.jpg"
# sftp.put(localpath,filepath)

# Close
if sftp: sftp.close()
if transport: transport.close()