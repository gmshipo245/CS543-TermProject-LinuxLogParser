#!/usr/bin/python3

import subprocess
import argparse
import os

from authLog import *
from fileData import FileData
from colors import Color

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-p', metavar='path', type=str, default="/var/log/",
                        help='search for log files at the given path')                  
    parser.add_argument('-a', action='store_true',
                        help='print all sessions sorted by login time')
    parser.add_argument('-f', metavar='file', type=str, default="",
                        help='print data out to file') 

    args = parser.parse_args()

    #check if path is valid
    if(not os.path.isdir(args.p)):
        print(args.p + " is not a valid path")
        exit()
    #append a forward slash to the end of the path so later commands function properly
    path = args.p
    if(path[-1] != "/"):
        path = path + "/"

    try:
        #This command gets a list of auth files currently stored in /var/log/
        out = subprocess.check_output("ls " + args.p + " | grep auth", shell=True, executable='/bin/bash')
        fileNames = out.decode('utf-8').split('\n')
        fileNames.remove('')
    except:
        print("There are no log files at this directory")
        exit()

    print("Log files: " + str(fileNames))

    files = []
    for file in fileNames:
        fileData = checkLog(path,file)
        if(fileData != None):
            if(not args.a and args.f == ""):
                print(fileData)
            files.append(fileData)
    
    if(args.a):
        color = Color()
        print()
        print(color.toBold("Printing all of the sessions found"))
        allSessions = FileData("","")
        allSessions.fromFiles(files)
        print(allSessions)
    