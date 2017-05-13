from tokenType import TokenType
from token import Token
from AST import *

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.previousToken = Token()
        
    def resetPreviousToken(self):
        self.previousToken = Token()
        self.previousToken.type = TokenType.Undefined
        self.previousToken.value = ""
        self.previousToken.line = 0
        self.previousToken.pos = 0
        
    def parse(self):
        self.resetPreviousToken()
        syntaxTree = Program()
        syntaxTree.mainBlock = self.parseStatementBlock(True)
        return syntaxTree

    def parseFunction(self):
        node = FunDefinition()
        tempToken = self.accept({ TokenType.Function})
        tempToken = self.accept({ TokenType.Identifier })
        node.setName(tempToken.value)
        node.setParameters(self.parseParameters())
        node.setBlock(self.parseStatementBlock())
        return node
    
    def accept(self,acceptable):
        if self.hasBufferedToken():
            token = self.previousToken
            self.resetPreviousToken()
            print(token.type)
        else:
            token = self.lexer.nextToken()
            print(token.type)

        if self.isAcceptable(token, acceptable):
            return token
        else:
            raise Exception('Invalid syntax', token.type, token.value)
            
    def peek(self,acceptable):
        if not self.hasBufferedToken():
            self.previousToken = self.lexer.nextToken()
        return self.isAcceptable(self.previousToken, acceptable)

    def peekFail(self):
        token = self.previousToken
        raise Exception('Unexpected  token ',token.type)
    
    def getPeeked(self):
        if not self.hasBufferedToken():
            raise Exception('Nothing peeked')
        return self.previousToken
    
    def error(self):
        raise Exception('Invalid syntax')
        
    def hasBufferedToken(self):
        return self.previousToken.type != TokenType.Undefined

    def isAcceptable(self,token, acceptable):
        return token.type in acceptable

    def parseParameters(self):
        parametersNames = []
        self.accept({ TokenType.ParenthOpen })

        tempToken = self.accept({ TokenType.ParenthClose, TokenType.Identifier })
        if tempToken.type != TokenType.ParenthClose:
            parametersNames.append(tempToken.value)
            while True:
                tempToken = self.accept({ TokenType.ParenthClose, TokenType.Comma })
                if tempToken.type == TokenType.ParenthClose:
                    break
                tempToken = self.accept({ TokenType.Identifier })
                parametersNames.append(tempToken.value)
        return parametersNames
    
    def parseStatementBlock(self,isFirst=False):
        node = StatementBlock()
        if not isFirst:
            self.accept({ TokenType.BracketOpen })
        while True:
            if not self.peek({TokenType.If,TokenType.While,TokenType.Return,
                TokenType.Var,TokenType.BracketOpen,TokenType.Identifier,
                TokenType.Continue,TokenType.Break,TokenType.Function, TokenType.EndOfFile}):
                break
            tempToken = self.getPeeked()

            if tempToken.type == TokenType.If:
                    node.addInstruction(self.parseIfStatement())
            elif tempToken.type == TokenType.While:
                    node.addInstruction(self.parseWhileStatement())
            elif tempToken.type == TokenType.Return:
                    node.addInstruction(self.parseReturnStatement())
            elif tempToken.type == TokenType.Var:
                    node.addInstruction(self.parseInitStatement())
            elif tempToken.type == TokenType.BracketOpen:
                    node.addInstruction(self.parseStatementBlock())
            elif tempToken.type == TokenType.Identifier:
                    node.addInstruction(self.parseAssignmentOrFunCall())
            elif tempToken.type == TokenType.Break:
                    node.addInstruction(self.parseLoopJump())
            elif tempToken.type == TokenType.Function:
                    node.addFunction(self.parseFunction())
            elif tempToken.type == TokenType.EndOfFile:
                if isFirst:
                    return node
                else:
                    self.error()
        if not isFirst:
            self.accept({ TokenType.BracketClose })
        return node
    
    def parseIfStatement(self):
        node = IfStatement()

        self.accept({ TokenType.If })
        self.accept({ TokenType.ParenthOpen })

        node.setCondition(self.parseCondition())

        self.accept({ TokenType.ParenthClose })

        node.setTrueBlock(self.parseStatementBlock())

        if self.peek({ TokenType.Else }):
            self.accept({ TokenType.Else })
            node.setFalseBlock(self.parseStatementBlock())
        return node
    
    def parseWhileStatement(self):
        node = WhileStatement()

        self.accept({ TokenType.While })
        self.accept({ TokenType.ParenthOpen })

        node.setCondition(self.parseCondition())

        self.accept({ TokenType.ParenthClose })

        node.setBlock(self.parseStatementBlock())
        return node
    
    def parseReturnStatement(self):
        node = ReturnStatement()

        self.accept({ TokenType.Return })
        node.setValue(self.parseAssignable())
        self.accept({ TokenType.Semicolon })

        return node
    
    def parseInitStatement(self):
        node = VarDeclaration()

        self.accept({ TokenType.Var  })
        nameToken = self.accept({ TokenType.Identifier })
        node.setName(nameToken.value)
        
        if self.peek({TokenType.Assignment}):
            self.accept({ TokenType.Assignment  })
            node.setValue(self.parseAssignable())
        
        self.accept({ TokenType.Semicolon })

        return node
    
    def parseAssignmentOrFunCall(self):
        tempToken  = self.accept({ TokenType.Identifier })
        node = self.parseFunCall(tempToken.value)
        if not node:
            assignmentNode = Assignment()
            assignmentNode.setVariable(self.parseVariable(tempToken))
            self.accept({ TokenType.Assignment })
            assignmentNode.setValue(self.parseAssignable())
            node = assignmentNode
        self.accept({ TokenType.Semicolon })   
        return node
    
    def parseLoopJump(self):       
        node = JumpLoop()
        token = self.accept({ TokenType.Continue, TokenType.Break });
        if not node:
            assignmentNode = Assignment()
            assignmentNode.setVariable(self.parseVariable(tempToken))
            self.accept({TokenType.Assignment})
            assignmentNode.setValue(self.parseAssignable())
            node = assignmentNode
        
        self.accept({ TokenType.Semicolon })
        
        return node
    
    def parseAssignable(self):
        if self.peek({ TokenType.Identifier }):
            tempToken = self.accept({ TokenType.Identifier })
            node = self.parseFunCall(tempToken.value)
            if not  node:
                node = self.parseExpression(tempToken)
        else:
            node = self.parseExpression()
        return node
    
    def parseFunCall(self,identifier):
        node = Call()
        
        if not self.peek({ TokenType.ParenthOpen }):
            return None
           
        node.setName(identifier)
        self.accept({ TokenType.ParenthOpen })
        
        if self.peek({ TokenType.ParenthClose }):
            self.accept({ TokenType.ParenthClose })
            return node
        while True:
            node.addArgument(self.parseAssignable())
            if self.peek({ TokenType.ParenthClose }):
                self.accept({ TokenType.ParenthClose })
                break
            if self.peek({ TokenType.Comma }):
                self.accept({ TokenType.Comma })
                continue
            self.peekFail()
        return node
    
    def parseExpression(self,firstToken = Token(TokenType.Undefined)):
        node = Expression()
        node.addOperand(self.parseMultiplicativeExpression(firstToken))
        while self.peek({ TokenType.Plus, TokenType.Minus }):
            tempToken = self.accept({ TokenType.Plus, TokenType.Minus })
            node.addOperator(tempToken.type)
            node.addOperand(self.parseMultiplicativeExpression())
        return node

    def parseMultiplicativeExpression(self,firstToken = Token(TokenType.Undefined)):
        node = Expression()
        node.addOperand(self.parsePrimaryExpression(firstToken))
        while self.peek({ TokenType.Multiply, TokenType.Divide }):
            tempToken = self.accept({ TokenType.Multiply, TokenType.Divide })
            node.addOperator(tempToken.type)
            node.addOperand(self.parsePrimaryExpression())
        return node

    def parsePrimaryExpression(self,firstToken = Token(TokenType.Undefined)):
        if firstToken.type != TokenType.Undefined:
            node = self.parseVariable(firstToken)
            return node
        if self.peek({ TokenType.ParenthOpen }):
            self.accept({ TokenType.ParenthOpen })
            node = self.parseExpression()
            self.accept({ TokenType.ParenthClose })
            return node
        if self.peek({ TokenType.Identifier  }):
            node = self.parseVariable()
            return node
        node = self.parseLiteral()
        return node

    def parseVariable(self,identifierToken = Token(TokenType.Undefined)):
        node = Variable()
        if identifierToken.type != TokenType.Identifier:
            tempToken = self.accept({TokenType.Identifier})
            node.setName(tempToken.value)
        else:
            node.setName(identifierToken.value)
        return node
        
    def parseLiteral(self):
        node = Literal()
        node.setData(self.parseNumberLiteral())
        return node

    def parseNumberLiteral(self):
        negative = False
        if self.peek({ TokenType.Minus }):
            self.accept({ TokenType.Minus })
            negative = True
        tempToken = self.accept({TokenType.NumberLiteral })
        value = tempToken.value
        if negative:
            value *= -1
        return value
    
    def parseCondition(self):
        node = Condition()
        node.addOperand(self.parseAndCondition())

        while self.peek({ TokenType.Or }):
            self.accept({ TokenType.Or })
            node.setOperator(TokenType.Or)
            node.addOperand(self.parseAndCondition())
        return node
    def parseAndCondition(self):
        node = Condition()
        node.addOperand(self.parseEqualityCondition())
        
        while self.peek({ TokenType.And }):
            self.accept({ TokenType.And })
            node.setOperator(TokenType.And)
            node.addOperand(self.parseEqualityCondition())
        return node
    
    def parseEqualityCondition(self):
        node = Condition()
        node.addOperand(self.parseRelationalCondition())
        
        if self.peek({ TokenType.Equality, TokenType.Inequality }):
            tempToken = self.accept({ TokenType.Equality, TokenType.Inequality })
            node.setOperator(tempToken.type)
            node.addOperand(self.parseRelationalCondition())
        return node
    
    def parseRelationalCondition(self):
        node = Condition()
        node.addOperand(self.parsePrimaryCondition())
        
        if self.peek({ TokenType.Less, TokenType.Greater, TokenType.LessOrEqual, TokenType.GreaterOrEqual }):
            tempToken = self.accept({ TokenType.Less, TokenType.Greater, TokenType.LessOrEqual, TokenType.GreaterOrEqual })
            node.setOperator(tempToken.type)
            node.addOperand(self.parsePrimaryCondition())
        return node
    
    def parsePrimaryCondition(self):
        node = Condition()
        if self.peek({ TokenType.Negation }):
            self.accept({ TokenType.Negation })
            node.setNegated()
        
        if self.peek({ TokenType.ParenthOpen}):
            self.accept({ TokenType.ParenthOpen })
            node.addOperand(self.parseCondition())
            self.accept({ TokenType.ParenthClose })
        else:
            if self.peek({ TokenType.Identifier }):
                node.addOperand(self.parseVariable())
            else:
                 node.addOperand(self.parseLiteral())
        if not node.isNegated():
            return node.getLeftSide()
        return node
    
    
    
    
    
    
    
    