from tokenType import TokenType
class ScopeProto():
    def __init__(self):
        self.variables = dict()
        self.upperScope = None
        self.varOrder = []
    def addVariable(self,name):
        if self.hasVariable(name):
            return False
        self.variables[name] = False
        self.varOrder.append(name)
        return True
    def getVariable(self,name):
        if name in self.variables:
            return self.variables[name]
        if self.upperScope:
            return self.upperScope.getVariable(name)
        return None
    def setVariableDefined(self,name):
        if name not in self.variables:
            self.variables[name] = True
    def hasVariable(self,name):
        return name in self.variables
    def isVariableDefined(self,name):
        if name in self.variables:
            return self.variables[name]
        return False
    def instantiate(self,upperScope):
        instance = ScopeInst()
        instance.upperScope = upperScope
        instance.varOrder = self.varOrder
        for name,val in self.variables.items():
            instance.variables[name] = val
        return instance
class ScopeInst():
    def __init__(self):
        self.variables = dict()
        self.upperScope = None
    def getVariable(self,name):
        if name in self.variables:
            return self.variables[name]
        if self.upperScope:
            return self.upperScope.getVariable(name)
        return None
    def setVariable(self,name,literal):
        if name in self.variables:
            self.variables[name] = literal
            return
        if self.upperScope:
            self.upperScope.setVariable(name)
            return
        raise Exception('Undefined variable')

class Instruction:
    def canDoReturn():
        return False        
        
class Block(Instruction):
    def __init__(self):
        super().__init__()
        self.instructions = []
        self.scopeProto = ScopeProto()    
    def execute(self,scope,functions):
        thisScope = self.scopeProto.instantiate(scope)
        for instruction in self.instructions:
            functionNode.name
            result = instruction.execute(thisScope, functions)
            if result and (result.loopJump or instruction.canDoReturn): 
                return result
        return None
    def canDoReturn():
        return True   
        
class Function(Block):
    def __init__(self):
        super().__init__()
        self.variables = dict()
        self.name = None
    def execute(self,scope,functions):
          raise Exception("Cannot execute function without parameters, fatal error")    
            
    def execute(self,scope,functions,arguments):
        thisScope = self.scopeProto.instantiate(scope)
        argIdx = 0
        for arg in arguments.items():
            copy = Literal()
            copy.data = argument.data
            thisScope.variables[thisScope.varOrder[argIdx]] = copy
            argIdx += 1
        for instruction in self.instructions:
            print(functions)
            result = instruction.execute(thisScope, functions)
            if result and result.loopJump :
                raise Exception('Break outside of loop')
            if result and instruction.canDoReturn():
                return result
        return None
class ConditionOperand:
    def isTruthy(self):
        return False
class Literal(ConditionOperand):
    def __init__(self):
        self.castedToBool  = False
        self.loopJump  = False
        self.isBreak  = False
        self.data = None
    def execute(self,scope,functions):
        copy = Literal()
        copy.data = self.data
        return copy
    def isTruthy():
        return self.data != 0

class Variable(ConditionOperand):
    def __init__(self):
        self.name = None
        self.value  = None
    def execute(self,scope,functions):
        ref = scope.getVariable(name)
        copy = Literal()
        copy.data = ref.data
        return copy
    def isTruthy():
        return self.data != 0

class LoopJump():
    def __init__(self):
        self.isBreak = None
        self.value  = None
    def execute(self,scope,functions):
        result  = Literal()
        result.loopJump  = True
        result.isBreak   = self.isBreak
        return result
class Assignment():
    def __init__(self):
        self.variable  = Variable()
        self.value  = None
    def execute(self,scope,functions):
        scope.setVariable(self.variable.name,value.execute(scope, functions))
        return None    
                    
class Call():
    def __init__(self):
        self.arguments  = []
        self.name  = None
    def execute(self,scope,functions):
        concreteArguments = []
        for arg in self.arguments:
            concreteArguments.append(arg.execute(scope, functions))
        return functions[self.name].execute(None, functions, concreteArguments)
        return None   

class Return(Instruction):
    def __init__(self):
        self.value  = None
    def execute(self,scope,functions):
        print(self.value)
        return self.value.execute(scope, functions)
    def canDoReturn(self):
        return true
    
class Expression():
    def __init__(self):
        self.operations  = []
        self.operands  = []
    def execute(self,scope,functions):
        if len(self.operations) == 0:
            return self.operands[0].execute(scope, functions)
        result = self.operands[0].execute(scope, functions)
        i = 0
        for operation in self.operations:
            it = self.operands[i]
            if op == TokenType.Plus:
                result += it.execute(scope, functions)
            elif op == TokenType.Minus:
                 result -= it.execute(scope, functions)
            elif op == TokenType.Multiply:
                  result *= it.execute(scope, functions)
            elif op == TokenType.Divide:
                result /= it.execute(scope, functions)
            else:
                raise Exception("Invalid expression operator")
        return result
    def canDoReturn(self):
        return true
    
                          
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
