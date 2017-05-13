from lexer import Lexer
from parser import Parser
from semCheck import SemCheck
lexer = Lexer("xd.js")
#for i in range(1,10):
#    token = lexer.nextToken()
 #   print(token.type,token.value)
parser = Parser(lexer)
semcheck = SemCheck()
syntaxTree = parser.parse()
mainBlock = semcheck.check(syntaxTree)
definedFunctions = dict()
#for it in checkResult:
#    print(it)
#    definedFunctions[it.name] =  it
#for i in checkResult:
mainBlock.execute(None,dict())