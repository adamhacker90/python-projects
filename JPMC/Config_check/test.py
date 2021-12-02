import pyfiglet
import os
import termcolor
os.system("color")

### Title ###
header = pyfiglet.figlet_format("DIRECTORY SEARCHER 3000", font = "slant")
header = termcolor.colored(header, color="magenta")
print(header)

### Specify path and extension to search
path = input("Specify directory path ")
ext = input("Input file extension ")

###Logic on finding finles in directory ####
files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(ext)]
if files:
    print(termcolor.colored("\nFound:", "green"))
    print(termcolor.colored(files, "blue"))
else:
    print(termcolor.colored("Nothing found", "red"))
    quit()

### Logic on searching files for specified string ###
string = input("\nInput string to search ")
for file in files:
    with open(file, "r") as f:
        for line in f.readlines():
            if str(string) in line:
                print(termcolor.colored("\nFound:", "green"))
                print(termcolor.colored(f"{line} @ {file}", "blue"))
