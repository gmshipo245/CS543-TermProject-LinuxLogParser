import json

from session import Session
from colors import Color

class FileData:

    def __init__(self,file,path):
        self.file = file
        self.path = path
        self.sessionArray = []

    def fromFiles(self, files):
        for file in files:
            for session in file.sessionArray:
                self.sessionArray.append(session)
        self.sessionArray.sort(key=lambda x: x.loginTime)

    
    def add(self,data):
        self.sessionArray.append(Session(data))

    def get(self,key):
        for s in self.sessionArray:
            if s.key == key:
                return s
    
    def empty(self):
        return len(self.sessionArray) == 0

    def length(self):
        return len(self.sessionArray)
    
    def logout(self,key,data):
        for s in self.sessionArray:
            if s.key == key and s.active:
                s.logout(data)
                break

    def __str__(self):
        color = Color()
        if not self.empty():
            print(color.toBold("Sessions:"))
            i = 0
            out = ""
            for s in self.sessionArray:
                out += s.output()
                i += 1
                if i != self.length():
                    out += "\n\n"
            return out
        else:
            return ""
    
    def toJSON(self):
        out = "{\"sessions\":["

        for i, s in enumerate(self.sessionArray):
            out += s.toJSON()
            if i+1 != len(self.sessionArray):
                out += ","
        out += "]}"
        return out
    
    def fromJSON(self,file):
        fileData = json.load(file)
        for d in fileData["sessions"]:
            newSession = Session()
            newSession.fromJSON(d)

            self.sessionArray.append(newSession)