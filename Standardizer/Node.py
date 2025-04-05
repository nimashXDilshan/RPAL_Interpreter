


class Node:
    # Node class for the Standardizer
    
    def __init__(self):
        self.data = None
        self.depth = None
        self.parent = None
        self.children = []
        self.is_standardized = False
    
    def set_data(self, data):
        self.data = data
    
    def get_data(self):
        return self.data
    
    def get_degree(self):
        return len(self.children)
    
    def get_children(self):
        return self.children
    
    def set_depth(self, depth):
        self.depth = depth
    
    def get_depth(self):
        return self.depth
    
    def set_parent(self, parent):
        self.parent = parent
    
    def get_parent(self):
        return self.parent
    
    def standardize(self):
        from Standardizer.NodeFactory import NodeFactory
        
        if not self.is_standardized:
            for child in self.children:
                child.standardize()
            
            if self.get_data() == "let":
                # standardizing let
                temp1 = self.children[0].children[1]
                temp1.set_parent(self)
                temp1.set_depth(self.depth + 1)
                temp2 = self.children[1]
                temp2.set_parent(self.children[0])
                temp2.set_depth(self.depth + 2)
                self.children[1] = temp1
                self.children[0].set_data("lambda")
                self.children[0].children[1] = temp2
                self.set_data("gamma")
                
            elif self.get_data() == "where":
                # standardizing where
                temp = self.children[0]
                self.children[0] = self.children[1]
                self.children[1] = temp
                self.set_data("let")
                self.standardize()
                
            elif self.get_data() == "function_form":
                # standardizing function_form
                Ex = self.children[-1]
                current_lambda = NodeFactory.get_node("lambda", self.depth + 1, self, [], True)
                self.children.insert(1, current_lambda)
                
                while self.children[2] != Ex:
                    V = self.children[2]
                    self.children.pop(2)
                    V.set_depth(current_lambda.depth + 1)
                    V.set_parent(current_lambda)
                    current_lambda.children.append(V)
                    
                    if len(self.children) > 3:
                        current_lambda = NodeFactory.get_node("lambda", current_lambda.depth + 1, current_lambda, [], True)
                        current_lambda.get_parent().children.append(current_lambda)
                
                current_lambda.children.append(Ex)
                self.children.pop(2)
                self.set_data("=")
                
            elif self.get_data() == "lambda":
                # standardizing lambda (multi parameter functions)
                if len(self.children) > 2:
                    Ey = self.children[-1]
                    current_lambdax = NodeFactory.get_node("lambda", self.depth + 1, self, [], True)
                    self.children.insert(1, current_lambdax)
                    
                    while self.children[2] != Ey:
                        V = self.children[2]
                        self.children.pop(2)
                        V.set_depth(current_lambdax.depth + 1)
                        V.set_parent(current_lambdax)
                        current_lambdax.children.append(V)
                        
                        if len(self.children) > 3:
                            current_lambdax = NodeFactory.get_node("lambda", current_lambdax.depth + 1, current_lambdax, [], True)
                            current_lambdax.get_parent().children.append(current_lambdax)
                    
                    current_lambdax.children.append(Ey)
                    self.children.pop(2)
                    
            elif self.get_data() == "within":
                # standardizing within
                X1 = self.children[0].children[0]
                X2 = self.children[1].children[0]
                E1 = self.children[0].children[1]
                E2 = self.children[1].children[1]
                
                gamma = NodeFactory.get_node("gamma", self.depth + 1, self, [], True)
                lambda_node = NodeFactory.get_node("lambda", self.depth + 2, gamma, [], True)
                
                X1.set_depth(X1.depth + 1)
                X1.set_parent(lambda_node)
                
                X2.set_depth(X1.depth - 1)
                X2.set_parent(self)
                
                E1.set_depth(E1.depth)
                E1.set_parent(gamma)
                
                E2.set_depth(E2.depth + 1)
                E2.set_parent(lambda_node)
                
                lambda_node.children.append(X1)
                lambda_node.children.append(E2)
                gamma.children.append(lambda_node)
                gamma.children.append(E1)
                
                self.children.clear()
                self.children.append(X2)
                self.children.append(gamma)
                self.set_data("=")
                
            elif self.get_data() == "@":
                # standardizing @
                gamma1 = NodeFactory.get_node("gamma", self.depth + 1, self, [], True)
                e1 = self.children[0]
                e1.set_depth(e1.get_depth() + 1)
                e1.set_parent(gamma1)
                
                n = self.children[1]
                n.set_depth(n.get_depth() + 1)
                n.set_parent(gamma1)
                
                gamma1.children.append(n)
                gamma1.children.append(e1)
                
                self.children.pop(0)
                self.children.pop(0)
                self.children.insert(0, gamma1)
                self.set_data("gamma")
                
            elif self.get_data() == "and":
                # standardizing and (simultaneous definitions)
                comma = NodeFactory.get_node(",", self.depth + 1, self, [], True)
                tau = NodeFactory.get_node("tau", self.depth + 1, self, [], True)
                
                for equal in self.children:
                    equal.children[0].set_parent(comma)
                    equal.children[1].set_parent(tau)
                    comma.children.append(equal.children[0])
                    tau.children.append(equal.children[1])
                
                self.children.clear()
                self.children.append(comma)
                self.children.append(tau)
                self.set_data("=")
                
            elif self.get_data() == "rec":
                # standardizing rec
                X = self.children[0].children[0]
                E = self.children[0].children[1]
                
                F = NodeFactory.get_node(X.get_data(), self.depth + 1, self, X.children, True)
                G = NodeFactory.get_node("gamma", self.depth + 1, self, [], True)
                Y = NodeFactory.get_node("<Y*>", self.depth + 2, G, [], True)
                L = NodeFactory.get_node("lambda", self.depth + 2, G, [], True)
                
                X.set_depth(L.depth + 1)
                X.set_parent(L)
                
                E.set_depth(L.depth + 1)
                E.set_parent(L)
                
                L.children.append(X)
                L.children.append(E)
                G.children.append(Y)
                G.children.append(L)
                
                self.children.clear()
                self.children.append(F)
                self.children.append(G)
                self.set_data("=")
                
            # unary & binary operators, tuples, conditionals and commas are not standardized due cse rules 6-13
            
        self.is_standardized = True