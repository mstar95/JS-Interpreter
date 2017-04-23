from reader import Reader
from token import Token
from tokenType import TokenType
from keyWords import keyWords, simpleSigns

class Lexer:
    def __init__(self, filename):
        self.reader = Reader(filename)
        self.lineNo = 0
        self.signNo = 0
    def nextToken(self):
        token = Token()
        token.line = self.reader.lineNo
        token.pos = self.reader.signNo
        sign = self.reader.nextSign()
        while(str.isspace(sign)):
            sign = self.reader.nextSign()
        if not sign:
            token.type = TokenType.EndOfFile
            return token
        buffer = ""
        if str.isalpha(sign):
            while(True):
                buffer += sign
                sign = self.reader.nextSign()
                if not str.isalnum(sign):
                    break
            if buffer in keyWords:
                token.type = keyWords[buffer]
            else:
                token.type = TokenType.Identifier
                token.value = buffer
            self.reader.seek()
        elif str.isdigit(sign):
            while(True):
                buffer += sign
                sign = self.reader.nextSign()
                if not str.isdigit(sign):
                    break
            token.type = TokenType.NumberLiteral
            token.value = buffer
        elif sign == "'":
            while(True):
                sign = self.reader.nextSign()
                if sign == "'":
                    break
                if not str.isalnum(sign):
                    return token
                buffer += sign
            token.type = TokenType.String
            token.value = buffer
        elif sign == '=':
            if (self.reader.nextSign() == '='):
                token.type = TokenType.Equality
            else:
                self.reader.seek()
                token.type = TokenType.Assignment
        elif sign == '!':
            if (self.reader.nextSign() == '='):
                token.type = TokenType.Inequality
            else:
                self.reader.seek()
                token.type = TokenType.Negation
        elif sign == '|':
            if (self.reader.nextSign() == '|'):
                token.type = TokenType.Or
            else:
                self.reader.seek()
                token.type = TokenType.Invalid
        elif sign == '&':
            if (self.reader.nextSign() == '&'):
                token.type = TokenType.And
            else:
                self.reader.seek()
                token.type = TokenType.Invalid
        elif sign == '<':
            if (self.reader.nextSign() == '='):
                token.type = TokenType.LessOrEqual
            else:
                self.reader.seek()
                token.type = TokenType.Less
        elif sign == '>':
            if (self.reader.nextSign() == '='):
                token.type = TokenType.GreaterOrEqual
            else:
                self.reader.seek()
                token.type = TokenType.Greater
        elif sign in simpleSigns:
            token.type = simpleSigns[sign]
        return token
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        