#!/usr/bin/env python3

"""Usage:

    config_check.py <path>
"""
import os
import sys
import pyfiglet
import termcolor
os.system("color")
import logging
from logging.handlers import RotatingFileHandler
import webbrowser
import time
import socket
import json

myhost = socket.gethostname()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# logging setup
rfh = logging.handlers.RotatingFileHandler(

    filename=resource_path('C:/config_check/'+myhost+"_test_result.txt"),
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



def string_search(path, string):
    """Find a string in a path and print out some info about what it found"""
    with open(path, "r") as f:
        found = False
        for line in f.readlines():
            if str(string) in line:
                found = True
                print(termcolor.colored("Found:", "green"))
                logger.debug("Found:")
                print(termcolor.colored(f"{line}", "green"))
                logger.debug(f"{line}")
                break
        if not found:
            print(termcolor.colored('Not Found:', 'red'))
            logger.debug("ERROR Not Found:")
            print(termcolor.colored(f'{string} not found\n', 'red'))
            logger.debug(f"{string}\n")



def main():
    #
    # Start of actual implementation
    #

    ### Specify path and extension to search ###
    if len(sys.argv) != 2:
        print('Script expects 1 argument')
    
    path = sys.argv[1] # input("Specify directory path ")
    ### useless easter egg ###
   
    # Do some error checking

    if not os.path.isfile(path):
        print(f"'{path}' is not a valid file")
        exit(1)

    split_path = path.split('.')

    if len(split_path) != 2:
        print(f"'{path}' does not have a valid file extension")
        exit(1)
    
    ext = split_path[1]

    if ext != 'ini':
        print(f"'{path}' is not a .ini file")
        exit(1)

    ### Logic on searching files for specified string, was not able to get this to loop successfully ###      
    string = ''  
    print(termcolor.colored("\nFile: nas.ini", "magenta"))
    logger.debug("***SEARCH: nas.ini***\n")
    with open("c:/config_check/config/config.json") as json_file:
        data = json.load(json_file)
    NASWriteSizeKB = (data['JPMC']['nas']['1'])
    NASWriteWaitMS = (data['JPMC']['nas']['2'])
    Mode1 = (data['JPMC']['nas']['3']) 
    Mode2 = (data['JPMC']['nas']['4'])
    Mode3 = (data['JPMC']['nas']['5'])

    string_search(path, NASWriteSizeKB)
    string_search(path, NASWriteWaitMS)
    string_search(path, Mode1)
    string_search(path, Mode2)
    string_search(path, Mode3)
    




if __name__ == '__main__':
    main()