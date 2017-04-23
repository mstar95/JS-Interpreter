class Reader:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.lineNo = 0
        self.signNo = 0
    def nextSign(self):
        while(True):
            self.seekPos = self.file.tell()
            sign = self.file.read(1)  
            if sign == '\n':
                self.lineNo += 1
                self.signNo = 0
                return " "
            self.signNo += 1
            return sign
    def seek(self):
        self.file.seek(self.seekPos)