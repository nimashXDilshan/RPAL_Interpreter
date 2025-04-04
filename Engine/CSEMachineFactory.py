# Engine/CSEMachineFactory.py

from Engine.CSEMachine import CSEMachine
from Symbols.E import E
from Symbols.B import B
from Symbols.Symbol import Symbol
from Symbols.Uop import Uop
from Symbols.Bop import Bop
from Symbols.Gamma import Gamma
from Symbols.Tau import Tau
from Symbols.Ystar import Ystar
from Symbols.Id import Id
from Symbols.Int import Int
from Symbols.Str import Str
from Symbols.Bool import Bool
from Symbols.Tup import Tup
from Symbols.Dummy import Dummy
from Symbols.Err import Err
from Symbols.Lambda import Lambda
from Symbols.Delta import Delta
from Symbols.Beta import Beta
from Standardizer.AST import AST
from Standardizer.Node import Node
from typing import List
from Symbols.Symbol import Symbol



class CSEMachineFactory:
    def __init__(self):
        self.e0 = E(0)
        self.i = 1
        self.j = 0
    
    def get_symbol(self, node: Node) -> Symbol:
        """Convert a node to the appropriate Symbol object based on its data"""
        data = node.get_data()
        
        # unary operators
        if data in ["not", "neg"]:
            return Uop(data)
        
        # binary operators
        elif data in ["+", "-", "*", "/", "**", "&", "or", "eq", "ne", "ls", "le", "gr", "ge", "aug"]:
            return Bop(data)
        
        # gamma
        elif data == "gamma":
            return Gamma()
        
        # tau
        elif data == "tau":
            return Tau(len(node.children))
        
        # ystar
        elif data == "<Y*>":
            return Ystar()
        
        # operands <ID:>, <INT:>, <STR:>, <nil>, <true>, <false>, <dummy>
        else:
            if data.startswith("<ID:"):
                return Id(data[4:-1])
            elif data.startswith("<INT:"):
                return Int(data[5:-1])
            elif data.startswith("<STR:"):
                return Str(data[6:-2])
            elif data.startswith("<nil"):
                return Tup()
            elif data.startswith("<true>"):
                return Bool("true")
            elif data.startswith("<false>"):
                return Bool("false")
            elif data.startswith("<dummy>"):
                return Dummy()
            else:
                print(f"Err node: {data}")
                return Err()
    
    def get_b(self, node: Node) -> B:
        """Create and populate a B object with symbols from pre-order traversal"""
        b = B()
        b.symbols = self.get_pre_order_traverse(node)
        return b
    
    def get_lambda(self, node: Node) -> Lambda:
        """Create a Lambda object from a lambda node"""
        lambda_obj = Lambda(self.i)
        self.i += 1
        lambda_obj.set_delta(self.get_delta(node.children[1]))
        
        if node.children[0].get_data() == ",":
            for identifier in node.children[0].children:
                lambda_obj.identifiers.append(Id(identifier.get_data()[4:-1]))
        else:
            lambda_obj.identifiers.append(Id(node.children[0].get_data()[4:-1]))
        
        return lambda_obj
    
    def get_pre_order_traverse(self, node: Node) -> List[Symbol]: # type: ignore
        """Traverse the AST in pre-order and convert nodes to symbols"""
        symbols = []
        
        if node.get_data() == "lambda":
            symbols.append(self.get_lambda(node))
        elif node.get_data() == "->":
            symbols.append(self.get_delta(node.children[1]))
            symbols.append(self.get_delta(node.children[2]))
            symbols.append(Beta())
            symbols.append(self.get_b(node.children[0]))
        else:
            symbols.append(self.get_symbol(node))
            for child in node.children:
                symbols.extend(self.get_pre_order_traverse(child))
        
        return symbols
    
    def get_delta(self, node: Node) -> Delta:
        """Create and populate a Delta object with symbols from pre-order traversal"""
        delta = Delta(self.j)
        self.j += 1
        delta.symbols = self.get_pre_order_traverse(node)
        return delta
    
    def get_control(self, ast: AST) -> List[Symbol]: # type: ignore
        """Create the control list for the CSE machine"""
        control = []
        control.append(self.e0)
        control.append(self.get_delta(ast.get_root()))
        return control
    
    def get_stack(self) -> List[Symbol]:  # type: ignore
        """Create the initial stack for the CSE machine"""
        stack = []
        stack.append(self.e0)
        return stack
    
    def get_environment(self) -> List[E]: # type: ignore
        """Create the initial environment for the CSE machine"""
        environment = []
        environment.append(self.e0)
        return environment
    
    def get_cse_machine(self, ast: AST) -> 'CSEMachine':
        """Create a CSEMachine with control, stack, and environment initialized"""
        return CSEMachine(self.get_control(ast), self.get_stack(), self.get_environment())