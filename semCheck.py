import ir
import AST
class SemCheck:
    def check(self,syntaxTree):
        self.syntaxTree = syntaxTree
        self.definedFunctions = dict()
        self.scanFunctionDefinitions()
        return self.traverseTree()
    def scanFunctionDefinitions(self):
        for functionNode in self.syntaxTree.functions:
            if functionNode.name in self.definedFunctions:
                raise Exception('Duplicated definition of function')
            self.definedFunctions[functionNode.name] = ir.Function()
            self.definedFunctions[functionNode.name].name =  functionNode.name
                                           
    def traverseTree(self):
        functions = []
        for function in self.syntaxTree.functions:
            functions.append(self.checkFunction(function))
        return functions

    def checkFunction(self,functionDef):
        function  = self.definedFunctions[functionDef.name]
        function.instructions.append(self.checkBlock(function.scopeProto,functionDef.blockNode))
        return function
    def checkBlock(self,scopeProto,blockNode):
        block = ir.Block()
        block.scopeProto.upperScope = scopeProto
        for instruction in blockNode.instructions:
            if instruction.getType() == AST.NodeType.VarDeclaration:
                self.checkVarDeclaration(block.scopeProto, instruction.name)
            elif instruction.getType() == AST.NodeType.Assignment:
                block.instructions.append(self.checkAssignment(block.scopeProto,instruction.variable,instrucion.value))
            elif instruction.getType() == AST.NodeType.ReturnStatement:
                block.instructions.append(self.checkReturnStatement(block.scopeProto,instruction.assignableNode))
            elif instruction.getType() == AST.NodeType.Call:
                block.instructions.append(self.checkFunctionCall(block.scopeProto,instruction))
            elif instruction.getType() == AST.NodeType.StatementBlock:
                block.instructions.append(self.checkBlock(block.scopeProto,instruction))
            elif instruction.getType() == AST.NodeType.IfStatement:
                block.instructions.append(self.checkIfStatement(block.scopeProto,instruction))
            elif instruction.getType() == AST.NodeType.WhileStatement:
                block.instructions.append(self.checkWhileStatement(block.scopeProto,instruction))
            elif instruction.getType() == AST.NodeType.LoopJump:
                node = ir.LoopJump()
                node.isBreak = instruction.isBreak
                block.instructions.append(node)    
        return block
    def checkVarDeclaration(self,scopeProto,name):
        if not scopeProto.addVariable(name):
            raise Exception("Redeclaration of variable: ")
    def checkAssignment(self,scopeProto,variable,assignable):
        node = ir.Assignment()
        if not scopeProto.hasVariable(variable):
            raise Exception("Assignment to undefined variable: ")
        node.variable.name = variable
        node.value = self.checkAssignable(scopeProto, assignable)
        scopeProto.setVariableDefined(variable)
        return node
    
    def checkAssignable(self,scopeProto,assignable):
        if assignable.getType() ==  AST.NodeType.Call:
            return self.checkFunctionCall(scopeProto,assignable)
        elif assignable.getType() ==  AST.NodeType.Expression:
            return self.checkExpression(scopeProto, assignable)
        return None
    
    def checkFunctionCall(self,scopeProto,call):
        if call.name not in self.definedFunctions:
            raise Exception("Call to undefined function")
            return None
        functionDef = self.definedFunctions[call.name]
        if len(functionDef.scopeProto.variables) != len(call.arguments):
            raise Exception("invalid args")
            return None
        obj = ir.Call()
        obj.name = call.name
        for argument in call.arguments:
            obj.arguments.append(self.checkAssignable(scopeProto, argument))
        return obj
    
    def checkExpression(self,scopeProto,expression):
        obj = ir.Expression()
        obj.operations = expression.operations
        for operand in expression.operands:
            if operand.getType() == AST.NodeType.Expression:
                 obj.operands.append(self.checkExpression(scopeProto, operand))
            elif operand.getType() == AST.NodeType.Variable:
                 obj.operands.append(self.checkVariable(scopeProto, operand))
            else:
                raise Exception("invalid expression operand", operand.getType())
        return obj
    
    def checkVariable(self,scopeProto,variable):
        obj = ir.Variable()
        if not scopeProto.hasVariable(variable.name):
            raise Exception("Usage of undefined variable")
            return None
        if not scopeProto.isVariableDefined(variable.name):
            raise Exception("Usage of empty  variable")
            return None
        obj.name = variable.name
        obj.value = self.checkAssignable(scopeProto, obj.value)
        return obj
    
    def checkReturnStatement(self,scopeProto,assignable):
        obj = ir.Return()
        obj.value = self.checkAssignable(scopeProto, assignable)
        return obj
    
    def checkIfStatement(self,scopeProto,stmt):
        obj = ir.IfStatement()
        obj.condition = self.checkCondition(scopeProto,stmt.conditionNode)
        obj.trueBlock = self.checkBlock(scopeProto, stmt.trueBlockNode)
        if stmt.falseBlockNode:
            obj.falseBlock = self.checkBlock(scopeProto, stmt.falseBlockNode)
        return obj
    
    def WhileStatement(self,scopeProto,stmt):
        obj = ir.WhileStatement()
        obj.condition = self.checkCondition(scopeProto,stmt.conditionNode)
        obj.block  = self.checkBlock(scopeProto, stmt.blockNode)
        return obj
    
    def checkCondition(self,scopeProto,condition):
        obj = ir.Condition()
        obj.operation  = condition.operation
        obj.negated = condition.negated
        for operand in condition.operands:
            if operand.getType() == AST.NodeType.Condition:
                 obj.operands.append(self.checkCondition(scopeProto, operand))
            elif operand.getType() == AST.NodeType.Variable:
                 obj.operands.append(self.checkVariable(scopeProto, operand))
            else:
                raise Exception("Invalid condition operand")
        return obj
                            
                            
        
    
        
        
        
            
                
        