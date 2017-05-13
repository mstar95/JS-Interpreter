from tokenType import TokenType
class ScopeProto():
    def __init__(self):
        self.variables = dict()
        self.upperScope = None
        self.varOrder = []
        self.functions = dict()
    def addFunction(self,name,function):
        self.functions[name] = function
         
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
        variable = self.getVariable(name)
        if not variable == None:
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
        instance.functions = self.functions
        for name,val in self.variables.items():
            instance.variables[name] = val
        return instance
class ScopeInst():
    def __init__(self):
        self.variables = dict()
        self.upperScope = None
        self.functions = dict()
    def getVariable(self,name):
        if name in self.variables:
            return self.variables[name]
        if self.upperScope:
            return self.upperScope.getVariable(name)
        return None
    def getFunction(self,name):
        if name in self.functions:
            return self.functions[name]
        if self.upperScope:
            return self.upperScope.getFunction(name)
        return None
    def setVariable(self,name,literal):
        if name in self.variables:
            self.variables[name] = literal
            return
        if self.upperScope:
            self.upperScope.setVariable(name,literal)
            return
        raise Exception('Undefined variable')

class Instruction:
    def canDoReturn(self):
        return False        
        
class Block(Instruction):
    def __init__(self):
        super().__init__()
        self.instructions = []
        self.scopeProto = ScopeProto()    
    def execute(self,scope,functions):
        selfScope = self.scopeProto.instantiate(scope)
        print(":D",self.instructions)
        for instruction in self.instructions:
            print("kek")
            result = instruction.execute(selfScope, functions)
            if result and (result.loopJump or instruction.canDoReturn()): 
                print(result.loopJump,instruction.canDoReturn,result.loopJump or instruction.canDoReturn)
                return result
        return None
    def canDoReturn(self):
        return True   
        
class Function(Block):
    
    def __init__(self):
        super().__init__()
        self.variables = dict()
        self.name = None
    def execute(self,scope,functions):
          raise Exception("Cannot execute function without parameters, fatal error")    
            
    def execute(self,scope,functions,arguments):
        selfScope = self.scopeProto.instantiate(scope)
        argIdx = 0
        for arg in arguments:
            copy = Literal()
            copy.data = argument.data
            selfScope.variables[selfScope.varOrder[argIdx]] = copy
            argIdx += 1
        for instruction in self.instructions:
            result = instruction.execute(selfScope, functions)
            if result and result.loopJump :
                raise Exception('Break outside of loop')
            if result and instruction.canDoReturn():
                return result
        return None
class ConditionOperand:
    def isTruthy(self):
        return False
class Condition(ConditionOperand):
    def __init__(self):
        self.negated = False
        self.operation = TokenType.Undefined
        self.operands = []
    def execute(self,scope,functions):
        if self.operation == TokenType.Undefined:
            if not self.negated:
                return self.operands[0].execute(scope, functions)
            else:
                result = Literal()
                result.castedToBool = True
                data = self.operands[0].execute(scope, functions).isTruthy()
                if data:
                    result.data = 0.0
                else:
                    result.data = 1.0
                return result
        elif self.operation == TokenType.Or:
            result = Literal()
            result.castedToBool = True
            for operand in self.operands:
                if operand.execute(scope, functions).isTruthy():
                    result.data = 1.0
                    return result
            result.data = 0.0 
            return result
        elif self.operation == TokenType.And:
            result = Literal()
            result.castedToBool = True
            for operand in self.operands:
                if not operand.execute(scope, functions).isTruthy():
                    result.data = 0.0
                    return result
            result.data = 1.0 
            return result
        elif self.operation == TokenType.Equality:
            result = Literal()
            result.castedToBool = True
            left = self.operands[0].execute(scope, functions)
            right = self.operands[1].execute(scope, functions)
            if left.castedToBool and right.castedToBool:
                result.data = 1.0 if left.isTruthy() == right.isTruth() else 0.0
            elif not left.castedToBool and not right.castedToBool:
                result.data = 1.0 if left.data == right.data else 0.0 
            else:
                raise Error("compare queality")
            return result
        elif self.operation == TokenType.Inequality:
            result = Literal()
            result.castedToBool = True
            left = self.operands[0].execute(scope, functions)
            right = self.operands[1].execute(scope, functions)
            if left.castedToBool and right.castedToBool:
                result.data = 1.0 if left.isTruthy() != right.isTruth() else 0.0
            elif not left.castedToBool and not right.castedToBool:
                result.data = 1.0 if left.data != right.data else 0.0 
            else:
                raise Error("compare inqueality")
            return result
        elif self.operation == TokenType.Less:
            result = Literal()
            result.castedToBool = True
            left = self.operands[0].execute(scope, functions)
            right = self.operands[1].execute(scope, functions)
            if not left.castedToBool and not right.castedToBool:
                result.data = 1.0 if left.data < right.data else 0.0
            else:
                raise Exception("compare less")
                return None
            return result
        elif self.operation == TokenType.LessOrEqual:
            result = Literal()
            result.castedToBool = True
            left = self.operands[0].execute(scope, functions)
            right = self.operands[1].execute(scope, functions)
            if not left.castedToBool and not right.castedToBool:
                result.data = 1.0 if left.data <= right.data else 0.0 
            else:
                raise Exception("compare lessEqual")
                return None
            return result
        elif self.operation == TokenType.Greater:
            result = Literal()
            result.castedToBool = True
            left = self.operands[0].execute(scope, functions)
            right = self.operands[1].execute(scope, functions)
            if not left.castedToBool and not right.castedToBool:
                result.data = 1.0 if left.data > right.data else 0.0
            else:
                raise Exception("compare greater")
                return None
            return result
        elif self.operation == TokenType.GreaterOrEqual:
            result = Literal()
            result.castedToBool = True
            left = self.operands[0].execute(scope, functions)
            right = self.operands[1].execute(scope, functions)
            if not left.castedToBool and not right.castedToBool:
                result.data = 1.0 if left.data >= right.data else 0.0
            else:
                raise Exception("compare greater")
                return None
            return result
        else:
            raise Exception("Invalid condition operator")
            return None
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
    def isTruthy(self):
        return self.data != 0

class Variable(ConditionOperand):
    def __init__(self):
        self.name = None
        self.value  = None
    def execute(self,scope,functions):
        ref = scope.getVariable(self.name)
        copy = Literal()
        copy.data = ref.data
        return copy
    def isTruthy(self):
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
        scope.setVariable(self.variable.name,self.value.execute(scope, functions))
        return None    
                    
class Call(Instruction):
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
        print("CHUJ")
        return self.value.execute(scope, functions)
    def canDoReturn(self):
        return True
    
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
            i+=1
            it = self.operands[i]
            if operation == TokenType.Plus:
                result.data += it.execute(scope, functions).data
            elif operation == TokenType.Minus:
                 result.data -= it.execute(scope, functions).data
            elif operation == TokenType.Multiply:
                  result.data *= it.execute(scope, functions).data
            elif operation == TokenType.Divide:
                result.data /= it.execute(scope, functions).data
            else:
                raise Exception("Invalid expression operator")
        return result
    def canDoReturn(self):
        return True
    
class IfStatement():
    def __init__(self):
        self.condition  = None
        self.trueBlock  = None
        self.falseBlock = None
    def execute(self,scope,functions):
        if self.condition.execute(scope, functions).isTruthy():
            return self.trueBlock.execute(scope,functions)
        else:
            return self.falseBlock.execute(scope,functions)
        return None
    def canDoReturn(self):
        return True
    
              