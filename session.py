from datetime import datetime

from colors import Color

class Session:
    userId = ""
    key = ""
    loginTime = datetime.now()
    logoutTime = datetime.now()
    loginLine = ""
    logoutLine = ""
    active = False

    def __init__(self,data=""):
        if data != "":
            self.key = data.split("session ")[1].split(" ")[0]
            self.userId = data.split("user ")[1].split(".")[0]
            self.loginTime = datetime.strptime(data.split(" ubuntu")[0], '%b %d %H:%M:%S').replace(year=datetime.now().year)
            self.loginLine = data
            self.active = True
    
    
    def logout(self, data):
        self.logoutTime = datetime.strptime(data.split(" ubuntu")[0], '%b %d %H:%M:%S').replace(year=datetime.now().year)
        self.logoutLine = data
        self.active = False
    
    def __str__(self):
        return self.output(self)

    def output(self):
        color = Color()
        out = color.toBold("User Id: ") + self.userId + "\n"
        out += color.toBold("Login time: ") + str(self.loginTime.strftime('%b %d %H:%M:%S'))
        if not self.active:
            out += "\n" + color.toBold("Logout time: ") + str(self.logoutTime.strftime('%b %d %H:%M:%S'))
        return out
    
    def toJSON(self):
        out = "{"
        out += self.toKeyVal("userId",self.userId) + ","
        out += self.toKeyVal("key", self.key) + ","
        out += self.toKeyVal("loginTime", str(self.loginTime)) + ","
        out += self.toKeyVal("loginLine", str(self.loginLine)) + ","
        if not self.active:
            out += self.toKeyVal("logoutTime", str(self.logoutTime)) + ","
            out += self.toKeyVal("logoutLine", self.logoutLine) + ","
        out += self.toKeyVal("active", str(self.active).lower())
        out += "}"
        return out
    
    def toKeyVal(self,key, val):
        out = "\"" + key + "\": "
        if (not isinstance(key, int)) or val.isnumeric():
            out += "\"" + str(val) + "\""
        else:
            out += "\"" + val + "\""
        return out
    
    def fromJSON(self,data):
        self.userId = data["userId"]
        self.key = data["key"]
        self.loginTime = datetime.strptime(str(data["loginTime"]).split(".")[0], '%Y-%m-%d %H:%M:%S')
        if "logoutTime" in data:
            self.logoutTime = datetime.strptime(str(data["logoutTime"]).split(".")[0], '%Y-%m-%d %H:%M:%S')
        self.loginLine = data["loginLine"]
        if "logoutLine" in data:
            self.logoutLine = data["logoutLine"]
        self.active = True if data["active"] == "true" else False

