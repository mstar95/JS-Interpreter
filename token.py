from tokenType import TokenType
class Token:
    def __init__(self,tokenType = TokenType.Invalid):
        self.type = tokenType
        self.value = ""
        self.line = 0
        self.pos = 0