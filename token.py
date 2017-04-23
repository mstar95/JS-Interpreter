from tokenType import TokenType
class Token:
    def __init__(self):
        self.type = TokenType.Invalid
        self.value = ""
        self.line = 0
        self.pos = 0