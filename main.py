from lexer import Lexer
from keyWords import keyWords
from tokenType import TokenType

lexer = Lexer("xd.json")
while(True):
    token = lexer.nextToken()
    print(token.type, token.value)
    if token.type == TokenType.EndOfFile:
        break