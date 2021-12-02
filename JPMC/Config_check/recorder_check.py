#!/usr/bin/env python3

"""Usage:

    config_check.py <path>
"""
import os
import sys
import pyfiglet
import termcolor
import logging
from logging.handlers import RotatingFileHandler
import webbrowser
import time
os.system("color")


# logging setup
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


def string_search(path, string):
    """Find a string in a path and print out some info about what it found"""
    with open(path, "r") as f:
        found = False
        for line in f.readlines():
            if str(string) in line:
                found = True
                print(termcolor.colored("Found:", "green"))
                logger.debug("Found:")
                print(termcolor.colored(f"{line}", "blue"))
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
    print(termcolor.colored("\nFile: recorder.ini", "magenta"))
    logger.debug("***SEARCH: recorder.ini***\n")
    string_search(path, "MaxSearchCriteria=300")
    string_search(path, "DBLocation=1")
    string_search(path, "Location=1")
    string_search(path, "MaxConnections=500")
    string_search(path, "NamedPipeReadTimeoutSecs=17")




if __name__ == '__main__':
    main()