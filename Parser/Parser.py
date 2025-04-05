#from enum import Enum
#from typing import List, Any
from Lexical_Analyzer.Token import Token
from Lexical_Analyzer.TokenType import TokenType
#from Exception.CustomException import CustomException
from Parser.Node import Node
from Parser.NodeType import NodeType


# Parser class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.AST = []
        self.stringAST = []
    
    def parse(self):
        self.tokens.append(Token(TokenType.END_OF_TOKENS, ""))
        self.E()
        if self.tokens[0].type == TokenType.END_OF_TOKENS:
            #print("Parsing Successful!")
            return self.AST
        else:
            print("Parsing Unsuccessful!")
            print("REMAINING UNPARSED TOKENS:")
            for token in self.tokens:
                print(f"<{token.type}, {token.value}>")
            return None
        
    def convert_AST_to_StringAST(self):
        #print("Converting AST to String.......")
        
        dots = ""
        stack = []
        
        while self.AST:
            if not stack:
                if self.AST[-1].noOfChildren == 0:
                    self.add_strings(dots, self.AST.pop())
                else:
                    node = self.AST.pop()
                    stack.append(node)
            else:
                if self.AST[-1].noOfChildren > 0:
                    node = self.AST.pop()
                    stack.append(node)
                    dots += "."
                else:
                    stack.append(self.AST.pop())
                    dots += "."
                    while stack[-1].noOfChildren == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]
                        node = stack.pop()
                        node.noOfChildren -= 1
                        stack.append(node)
        
        # Reverse the list
        self.stringAST.reverse()
        return self.stringAST
    
    def add_strings(self, dots, node):
        if node.type in [NodeType.IDENTIFIER, NodeType.INTEGER, NodeType.STRING, NodeType.TRUE_VALUE,
                         NodeType.FALSE_VALUE, NodeType.NIL, NodeType.DUMMY]:
            self.stringAST.append(dots + "<" + node.type.name.upper() + ":" + node.value + ">")
        elif node.type == NodeType.FCN_FORM:
            self.stringAST.append(dots + "function_form")
        else:
            self.stringAST.append(dots + node.value)
    
    
    # Expression parsing methods
    def E(self):
        # print("E()")
        
        n = 0
        token = self.tokens[0]
        if token.type == TokenType.KEYWORD and token.value in ["let", "fn"]:
            if token.value == "let":
                # print(self.tokens[0].value)
                self.tokens.pop(0)
                self.D()
                if self.tokens[0].value != "in":
                    print("Parse error at E : 'in' Expected")
                # print(self.tokens[0].value)
                self.tokens.pop(0)
                self.E()
                self.AST.append(Node(NodeType.LET, "let", 2))
            else:
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove fn
                while (self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "("):
                    self.Vb()
                    n += 1                
                if self.tokens[0].value != ".":
                    print("Parse error at E : '.' Expected")
                # print(self.tokens[0].value)
                self.tokens.pop(0)
                self.E()
                self.AST.append(Node(NodeType.LAMBDA, "lambda", n+1))
        else:
            self.Ew()
    
    def Ew(self):
        # print("Ew()")
        self.T()
        if self.tokens[0].value == "where":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove where
            self.Dr()
            self.AST.append(Node(NodeType.WHERE, "where", 2))
    
    def T(self):
        # print("T()")
        self.Ta()
        n = 1
        while self.tokens[0].value == ",":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove comma
            self.Ta()
            n += 1
        if n > 1:
            self.AST.append(Node(NodeType.TAU, "tau", n))
    
    def Ta(self):
        # print("Ta()")
        self.Tc()
        while self.tokens[0].value == "aug":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove aug
            self.Tc()
            self.AST.append(Node(NodeType.AUG, "aug", 2))
    
    def Tc(self):
        # print("Tc()")
        self.B()
        if self.tokens[0].value == "->":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove '->'
            self.Tc()
            if self.tokens[0].value != "|":
                print("Parse error at Tc: conditional '|' expected")
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove '|'
            self.Tc()
            self.AST.append(Node(NodeType.CONDITIONAL, "->", 3))
    
    def B(self):
        # print("B()")
        self.Bt()
        while self.tokens[0].value == "or":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove 'or'
            self.Bt()
            self.AST.append(Node(NodeType.OP_OR, "or", 2))
    
    def Bt(self):
        # print("Bt()")
        self.Bs()
        while self.tokens[0].value == "&":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove '&'
            self.Bs()
            self.AST.append(Node(NodeType.OP_AND, "&", 2))
    
    def Bs(self):
        # print("Bs()")
        if self.tokens[0].value == "not":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove 'not'
            self.Bp()
            self.AST.append(Node(NodeType.OP_NOT, "not", 1))
        else:
            self.Bp()
    
    def Bp(self):
        # print("Bp()")
        self.A()
        token = self.tokens[0]
        if token.value in [">", ">=", "<", "<=" , "gr", "ge", "ls", "le", "eq", "ne"]:
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            self.A()
            if token.value == ">":
                self.AST.append(Node(NodeType.OP_COMPARE, "gr", 2))
            elif token.value == ">=":
                self.AST.append(Node(NodeType.OP_COMPARE, "ge", 2))
            elif token.value == "<":
                self.AST.append(Node(NodeType.OP_COMPARE, "ls", 2))
            elif token.value == "<=":
                self.AST.append(Node(NodeType.OP_COMPARE, "le", 2))
            else:
                self.AST.append(Node(NodeType.OP_COMPARE, token.value, 2))
    
    def A(self):
        # print("A()")
        if self.tokens[0].value == "+":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove unary plus
            self.At()
        elif self.tokens[0].value == "-":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove unary minus
            self.At()
            self.AST.append(Node(NodeType.OP_NEG, "neg", 1))
        else:
            self.At()
        
        while self.tokens[0].value in ["+", "-"]:
            current_token = self.tokens[0]  # Save present token
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove plus or minus operators
            self.At()
            if current_token.value == "+":
                self.AST.append(Node(NodeType.OP_PLUS, "+", 2))
            else:
                self.AST.append(Node(NodeType.OP_MINUS, "-", 2))
    
    def At(self):
        # print("At()")
        self.Af()
        while self.tokens[0].value in ["*", "/"]:
            current_token = self.tokens[0]  # Save present token
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove multiply or divide operators
            self.Af()
            if current_token.value == "*":
                self.AST.append(Node(NodeType.OP_MUL, "*", 2))
            else:
                self.AST.append(Node(NodeType.OP_DIV, "/", 2))
    
    def Af(self):
        # print("Af()")
        self.Ap()
        if self.tokens[0].value == "**":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove power operator
            self.Af()
            self.AST.append(Node(NodeType.OP_POW, "**", 2))
    
    def Ap(self):
        # print("Ap()")
        self.R()
        while self.tokens[0].value == "@":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove @ operator
            
            if self.tokens[0].type != TokenType.IDENTIFIER:
                print("Parsing error at Ap: IDENTIFIER EXPECTED")
            self.AST.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove IDENTIFIER
            
            self.R()
            self.AST.append(Node(NodeType.AT, "@", 3))
    
    def R(self):
        # print("R()")
        self.Rn()
        while (self.tokens[0].type in [TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.STRING] or
               self.tokens[0].value in ["true", "false", "nil", "dummy"] or
               self.tokens[0].value == "("):
            
            self.Rn()
            self.AST.append(Node(NodeType.GAMMA, "gamma", 2))
            # print("gamma node added")
    
    def Rn(self):
        # print("Rn()")
        token = self.tokens[0]
        
        if token.type == TokenType.IDENTIFIER:
            self.AST.append(Node(NodeType.IDENTIFIER, token.value, 0))
            # print(token.value)
            self.tokens.pop(0)
        elif token.type == TokenType.INTEGER:
            self.AST.append(Node(NodeType.INTEGER, token.value, 0))
            # print(token.value)
            self.tokens.pop(0)
        elif token.type == TokenType.STRING:
            self.AST.append(Node(NodeType.STRING, token.value, 0))
            # print(token.value)
            self.tokens.pop(0)
        elif token.type == TokenType.KEYWORD:
            if token.value == "true":
                self.AST.append(Node(NodeType.TRUE_VALUE, token.value, 0))
                # print(token.value)
                self.tokens.pop(0)
            elif token.value == "false":
                self.AST.append(Node(NodeType.FALSE_VALUE, token.value, 0))
                # print(token.value)
                self.tokens.pop(0)
            elif token.value == "nil":
                self.AST.append(Node(NodeType.NIL, token.value, 0))
                # print(token.value)
                self.tokens.pop(0)
            elif token.value == "dummy":
                self.AST.append(Node(NodeType.DUMMY, token.value, 0))
                # print(token.value)
                self.tokens.pop(0)
            else:
                print("Parse Error at Rn: Unexpected KEYWORD")
        elif token.type == TokenType.PUNCTUATION:
            if token.value == "(":
                # print(token.value)
                self.tokens.pop(0)  # Remove '('
                
                self.E()
                
                if self.tokens[0].value != ")":
                    print("Parsing error at Rn: Expected a matching ')'")
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove ')'
            else:
                print("Parsing error at Rn: Unexpected PUNCTUATION")
        else:
            
            print("Parsing error at Rn: Expected a Rn, but got different")
    
    # Definition parsing methods
    def D(self):
        # print("D()")
        self.Da()
        if self.tokens[0].value == "within":
            # print(self.tokens[0].value)
            self.tokens.pop(0)  # Remove 'within'
            self.D()
            self.AST.append(Node(NodeType.WITHIN, "within", 2))
    
    def Da(self):
        # print("Da()")
        self.Dr()
        n = 1
        while self.tokens[0].value == "and":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            self.Dr()
            n += 1
        if n > 1:
            self.AST.append(Node(NodeType.OP_AND, "and", n))
    
    def Dr(self):
        # print("Dr()")
        is_rec = False
        if self.tokens[0].value == "rec":
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            is_rec = True
        self.Db()
        if is_rec:
            self.AST.append(Node(NodeType.REC, "rec", 1))
    
    def Db(self):
        # print("Db()")

        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(": # Db's production 3
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            self.D()
            if self.tokens[0].value != ")":
                print("Parsing error at Db #1")
            # print(self.tokens[0].value)
            self.tokens.pop(0)


        elif self.tokens[0].type == TokenType.IDENTIFIER: # Db's production 1 & 2
            if self.tokens[1].value == "(" or self.tokens[1].type == TokenType.IDENTIFIER:  # Expect a fcn_form
                self.AST.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove ID
                
                n = 1  # Identifier child
                while self.tokens[0].type == TokenType.IDENTIFIER or self.tokens[0].value == "(":
                    self.Vb()
                    n += 1

                if self.tokens[0].value != "=":
                    print("Parsing error at Db #2")
                # print(self.tokens[0].value)
                self.tokens.pop(0)
                self.E()
                
                self.AST.append(Node(NodeType.FCN_FORM, "fcn_form", n+1))
            elif self.tokens[1].value == "=":
                self.AST.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove identifier
                # print(self.tokens[0].value)
                self.tokens.pop(0)  # Remove equal
                self.E()
                self.AST.append(Node(NodeType.EQUAL, "=", 2))
            elif self.tokens[1].value == ",":
                self.Vl()
                if self.tokens[0].value != "=":
                    print("Parsing error at Db")
                # print(self.tokens[0].value)
                self.tokens.pop(0)
                self.E()
                
                self.AST.append(Node(NodeType.EQUAL, "=", 2))
    
    # Variable parsing methods
    def Vb(self):
        # print("Vb()")
        if self.tokens[0].type == TokenType.PUNCTUATION and self.tokens[0].value == "(":# Vb's 2 & 3 productions
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            is_vl = False
            
            if self.tokens[0].type == TokenType.IDENTIFIER:
                self.Vl()
                is_vl = True

            if self.tokens[0].value != ")":
                print("Parse error unmatch )")
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            if not is_vl:
                self.AST.append(Node(NodeType.EMPTY_PARAMS, "()", 0))

        elif self.tokens[0].type == TokenType.IDENTIFIER: # Vb's 1 productions
            self.AST.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            # print(self.tokens[0].value)
            self.tokens.pop(0)
    
    #comma seperated variable list in Vl

    def Vl(self):
        # print("Vl()")
        n = 0
        while True:
            if n > 0: # remove that comma token before parsing the next identifier.
                # print(self.tokens[0].value)
                self.tokens.pop(0)
            if self.tokens[0].type != TokenType.IDENTIFIER:
                print("Parse error: an ID was expected")
            self.AST.append(Node(NodeType.IDENTIFIER, self.tokens[0].value, 0))
            # print(self.tokens[0].value)
            self.tokens.pop(0)
            n += 1
            if self.tokens[0].value != ",":
                break
        if n >1:
            self.AST.append(Node(NodeType.COMMA, ",", n))