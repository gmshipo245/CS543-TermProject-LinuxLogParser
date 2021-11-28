#!/usr/bin/python3

import subprocess
import hashlib
import os
import json

from session import Session
from fileData import FileData
from colors import Color

def checkLog(path,file):
    colors = Color()
    fileName = file

    #Unzipping the file
    if ".gz" in file:
        print(colors.toBold("Need to Unzip file"))
        try:
            subprocess.check_output("sudo gunzip " + path + file,shell=True, executable='/bin/bash')
        except:
            print("Error trying to unzip " + path + file)
            return FileData("","" )
        fileName = file.replace(".gz","")

    print(colors.toBlue("Reading " + path + fileName + ":"))
    try:
        out = subprocess.check_output("cat " + path + fileName + " | grep logind", shell=True, executable='/bin/bash')
    except subprocess.CalledProcessError:
        print(colors.toRed("Error reading " + path + fileName))
        print("The file may be missing or did not contain any useful data.")
        return

    #Rezip the file so we don't mess with the logging system
    if ".gz" in file:
        try:
            subprocess.check_output("sudo gzip " + path + fileName,shell=True, executable='/bin/bash')
        except:
            print("Error trying to rezip " + path + file)
            return FileData("","" )
        fileName = file.replace(".gz","")
    
    #Have to decond the output from the subprocess command into a readable string
    authLogOutput = out.decode('utf-8')
    #Get the hash of the current data
    currentHash = hashlib.sha1(out).hexdigest()

    sessions = FileData(file,path)
    change = True
    
    if(not os.path.isdir(".data/")):
        os.mkdir(".data/")

    dataStoragePath = ".data/" + path.replace("/", "",1).replace("/", "_")

    if(not os.path.isdir(dataStoragePath)):
        os.mkdir(dataStoragePath)

    hashFileName = dataStoragePath + "/" + fileName + ".hash.txt"
    dataFileName = dataStoragePath + "/" + fileName + ".data.json"

    try:
        f = open(hashFileName,'r')
        oldHash = f.readline()
        if(oldHash == currentHash):
            try:
                if os.stat(dataFileName).st_size != 0:
                    f.close()
                    f = open(dataFileName,'r')
                    sessions.fromJSON(f)
                    change = False
            except: #if .authlog.txt does not exist
                pass
        else:
            f = open(hashFileName,"w")
            f.write(currentHash)
    except:
        #no old hash file
        f = open(hashFileName,"x")
        f.write(currentHash)
    
    if change:
        for line in authLogOutput.split("\n"):
            if "New session" in line:
                sessions.add(line)

            if "logged out" in line:
                key = line.split("Session ")[1].split(" ")[0]
                sessions.logout(key,line)

            #The line that meets the above case is not always present so need to check for this type            
            if  "Removed session" in line:
                key = line.split("Removed session ")[1].split(".")[0]
                sessions.logout(key,line)
    
    if not change:
        print(colors.toGreen("No Changes since last read"))
    # print(sessions)

    if change:
        try:
            f = open(dataFileName,"x")
            jsonObject = json.loads(sessions.toJSON())
            json.dump(jsonObject, f, indent=4)
        except:
            f = open(dataFileName,"w")
            jsonObject = json.loads(sessions.toJSON())
            json.dump(jsonObject, f, indent=4)

    return sessions