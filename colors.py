class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    def toBold(self,text):
        return self.BOLD + text + self.END

    def toRed(self,text):
        return self.RED + text + self.END

    def toGreen(self,text):
        return self.GREEN + text + self.END
    
    def toBlue(self, text):
        return self.BOLD + self.BLUE + text + self.END