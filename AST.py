from enum import Enum, auto
class NoValue(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)
class NodeType(NoValue):
    Program             = auto() 
    FunDefinition       = auto()
    Statement           = auto()
    Assignment          = auto()
    Call                = auto()
    Condition           = auto()
    Expression          = auto()
    IfStatement         = auto()
    LoopJump            = auto()
    ReturnStatement     = auto()
    StatementBlock      = auto()
    VarDeclaration      = auto()
    Variable            = auto()
    WhileStatement      = auto()
    Literal             = auto()
    
class Node():
    pass

class Program(Node):
    def __init__(self):
        self.functions = []
    def addFunction(self,function):
        self.functions.append(function)
    def getType(self):
        return NodeType.Program
    
class FunDefinition(Node):  
    def setName(self,name):
        self.name = name;
    def setParameters(self,parameters):
        self.parameters = parameters
    def setBlock(self,blockNode):
        self.blockNode = blockNode
    def getType(self):
        return NodeType.FunDefinition

class StatementBlock(Node):
    def __init__(self):
        self.instructions = []
    def addInstruction(self,node):
          self.instructions.append(node)
    def getType(self):
        return NodeType.Statement

class WhileStatement(Node):
    def setCondition(self,conditionNode):
        self.conditionNode = conditionNode
    def setBlock(self,blockNode):
        self.blockNode = blockNode
    def getType(self):
        return NodeType.WhileStatement

class IfStatement(Node):
    def setCondition(self,conditionNode):
        self.conditionNode = conditionNode
    def setTrueBlock(self,trueBlockNode):
        self.trueBlockNode = trueBlockNode
    def setFalseBlock(self,falseBlockNode):
        self.falseBlockNode = falseBlockNode
    def getType(self):
        return NodeType.IfStatement    

class ReturnStatement(Node):
    def setValue(self,assignableNode):
        self.assignableNode = assignableNode
    def getType(self):
        return NodeType.ReturnStatement    
    
class Call(Node):
    def __init__(self):
        self.arguments = []
    def setName(self,name):
        self.name = name
    def addArgument(self,assignableNode):
        self.arguments.append(assignableNode) 
    def getType(self):
        return NodeType.Call   
    
class Expression(Node):
    def __init__(self):
        self.operations = []
        self.operands = []
    def addOperand(self,node):
        self.operands.append(node) 
    def addOperator(self,operation):
        self.operations.append(operation)
    def getType(self):
        return NodeType.Expression

class Variable(Node):
    def setName(self,name):
        self.name = name 
    def setArg(self,arg):
        self.arg = arg
    def getType(self):
        return NodeType.Variable 

class Assignment(Node):
    def setVariable(self,variable):
        self.variable = variable 
    def setValue(self,value):
        self.value = value
    def getType(self):
        return NodeType.Assignment

class Literal(Node):
    def setData(self,data):
        self.data = data
    def getType(self):
        return NodeType.Literal
    
class Condition(Node):
    def __init__(self):
        self.operation = TokenType.Undefined
        self.operands = []
        self.negated = False
    def setName(self,name):
        self.name = name
    def addOperand(self,operand):
        self.operands.append(operand)
    def setOperator(self,operation):
            self.operation = operation
    def setNegated(self,negated):
            self.negated = True
    def isNegated():
        return self.negated
    def getLeftSide():
        return self.operands[0]
    def getType(self): 
        return NodeType.Condition
    
class VarDeclaration(Node):
    def __init__(self):
        self.name = None
        self.assignableNode = None
    def setName(self,name):
        self.name = name
    def setValue(self,assignableNode):
        self.assignableNode  = assignableNode
    def getType(self): 
        return NodeType.VarDeclaration
