import os, fnmatch
import re
import sys
def findReplaceIPL(directory=os.path.join(sys.path[0]), filePattern="*.log"):
    print('searching .log files...')
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                filedata = f.read()
            filedata = re.sub(r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))|http\S+", "x.x.x.x", filedata)
            with open(filepath, "w") as f:
                f.write(filedata)

def findReplaceIPJ(directory=os.path.join(sys.path[0]), filePattern="*.json"):
    print("searching .json files...")
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                filedata = f.read()
            filedata = re.sub(r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))|http\S+", "x.x.x.x", filedata)
            with open(filepath, "w") as f:
                f.write(filedata)

def findReplaceIPI(directory=os.path.join(sys.path[0]), filePattern="*.ini"):
    print("searching .ini files...")
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                filedata = f.read()
            filedata = re.sub(r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))|http\S+", "x.x.x.x", filedata)
            with open(filepath, "w") as f:
                f.write(filedata)

def findReplaceIPP(directory=os.path.join(sys.path[0]), filePattern="*.pem"):
    print("searching .pem files...\n")
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                filedata = f.read()
            filedata = re.sub(r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))|http\S+", "x.x.x.x", filedata)
            with open(filepath, "w") as f:
                f.write(filedata)

print("\nRemoving ip/hostnames from files...")
findReplaceIPL()

findReplaceIPJ()

findReplaceIPI()

findReplaceIPP()

print("ip/hostnames removed\n")