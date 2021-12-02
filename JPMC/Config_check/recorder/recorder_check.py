#!/usr/bin/env python

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
    with open("c:/config_check/config/config.json") as json_file:
        data = json.load(json_file)
    MaxSearchCriteria = (data['JPMC']['recorder']['1a'])
    DBLocation = (data['JPMC']['recorder']['1a'])
    Location = (data['JPMC']['recorder']['1a'])
    MaxConnections = (data['JPMC']['recorder']['1a'])
    NamedPipeReadTimeoutSecs = (data['JPMC']['recorder']['1a'])
    LogSearchProgress = (data['JPMC']['recorder']['1a'])
    r10423 = (data['JPMC']['recorder']['1'])
    r10424 = (data['JPMC']['recorder']['2'])
    r10425 = (data['JPMC']['recorder']['3'])
    r10426 = (data['JPMC']['recorder']['4'])
    r10427 = (data['JPMC']['recorder']['5'])
    r10428 = (data['JPMC']['recorder']['6'])
    r10429 = (data['JPMC']['recorder']['7'])
    r10430 = (data['JPMC']['recorder']['8'])
    r10431 = (data['JPMC']['recorder']['9'])
    r10432 = (data['JPMC']['recorder']['10'])
    r10433 = (data['JPMC']['recorder']['11'])
    r10434 = (data['JPMC']['recorder']['12'])
    r10435 = (data['JPMC']['recorder']['13'])
    r10436 = (data['JPMC']['recorder']['14'])
    r10437 = (data['JPMC']['recorder']['15'])
    r10438 = (data['JPMC']['recorder']['16'])
    r10439 = (data['JPMC']['recorder']['17'])
    r10442 = (data['JPMC']['recorder']['18'])
    r10443 = (data['JPMC']['recorder']['19'])
    r10445 = (data['JPMC']['recorder']['20'])
    r10446 = (data['JPMC']['recorder']['21'])
    r10447 = (data['JPMC']['recorder']['22'])
    r10448 = (data['JPMC']['recorder']['23'])
    r10449 = (data['JPMC']['recorder']['24'])
    r10450 = (data['JPMC']['recorder']['25'])
    r10452 = (data['JPMC']['recorder']['26'])
    r10453 = (data['JPMC']['recorder']['27'])
    r10456 = (data['JPMC']['recorder']['28'])
    r10458 = (data['JPMC']['recorder']['29'])
    r10461 = (data['JPMC']['recorder']['30'])
    r10482 = (data['JPMC']['recorder']['31'])
    r10483 = (data['JPMC']['recorder']['32'])
    r10485 = (data['JPMC']['recorder']['33'])
    r10486 = (data['JPMC']['recorder']['34'])
    r10487 = (data['JPMC']['recorder']['35'])
    r10488 = (data['JPMC']['recorder']['36'])
    r10489 = (data['JPMC']['recorder']['37'])
    r10490 = (data['JPMC']['recorder']['38'])
    r10491 = (data['JPMC']['recorder']['39'])
    r10492 = (data['JPMC']['recorder']['40'])
    r10493 = (data['JPMC']['recorder']['41'])
    r10494 = (data['JPMC']['recorder']['42'])
    r10495 = (data['JPMC']['recorder']['43'])
    r10496 = (data['JPMC']['recorder']['44'])
    r10497 = (data['JPMC']['recorder']['45'])
    r10498 = (data['JPMC']['recorder']['46'])
    r10499 = (data['JPMC']['recorder']['47'])
    r10500 = (data['JPMC']['recorder']['48'])
    r10504 = (data['JPMC']['recorder']['49'])
    r10505 = (data['JPMC']['recorder']['50'])
    r10506 = (data['JPMC']['recorder']['51'])
    r10507 = (data['JPMC']['recorder']['52'])
    r10508 = (data['JPMC']['recorder']['53'])
    r10509 = (data['JPMC']['recorder']['54'])
    r10510 = (data['JPMC']['recorder']['55'])
    r10512 = (data['JPMC']['recorder']['56'])
    r10513 = (data['JPMC']['recorder']['57'])
    r10514 = (data['JPMC']['recorder']['58'])
    r10520 = (data['JPMC']['recorder']['59'])
    r10528 = (data['JPMC']['recorder']['60'])
    r10601 = (data['JPMC']['recorder']['61'])

    string_search(path, MaxSearchCriteria)
    string_search(path, DBLocation)
    string_search(path, Location)
    string_search(path, MaxConnections)
    string_search(path, NamedPipeReadTimeoutSecs)
    string_search(path, LogSearchProgress)
    string_search(path, r10423)
    string_search(path, r10424)
    string_search(path, r10425)
    string_search(path, r10426)
    string_search(path, r10427)
    string_search(path, r10428)
    string_search(path, r10429)
    string_search(path, r10430)
    string_search(path, r10431)
    string_search(path, r10432)
    string_search(path, r10433)
    string_search(path, r10434)
    string_search(path, r10435)
    string_search(path, r10436)
    string_search(path, r10437)
    string_search(path, r10438)
    string_search(path, r10439)
    string_search(path, r10442)
    string_search(path, r10443)
    string_search(path, r10445)
    string_search(path, r10446)
    string_search(path, r10447)
    string_search(path, r10448)
    string_search(path, r10449)
    string_search(path, r10450)
    string_search(path, r10452)
    string_search(path, r10453)
    string_search(path, r10456)
    string_search(path, r10458)
    string_search(path, r10461)
    string_search(path, r10482)
    string_search(path, r10483)
    string_search(path, r10485)
    string_search(path, r10486)
    string_search(path, r10487)
    string_search(path, r10488)
    string_search(path, r10489)
    string_search(path, r10490)
    string_search(path, r10491)
    string_search(path, r10492)
    string_search(path, r10493)
    string_search(path, r10494)
    string_search(path, r10495)
    string_search(path, r10496)
    string_search(path, r10497)
    string_search(path, r10498)
    string_search(path, r10499)
    string_search(path, r10500)
    string_search(path, r10504)
    string_search(path, r10505)
    string_search(path, r10506)
    string_search(path, r10507)
    string_search(path, r10508)
    string_search(path, r10509)
    string_search(path, r10510)
    string_search(path, r10512)
    string_search(path, r10513)
    string_search(path, r10514)
    string_search(path, r10520)
    string_search(path, r10528)
    string_search(path, r10601)




if __name__ == '__main__':
    main()