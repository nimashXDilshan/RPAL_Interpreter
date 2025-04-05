
# CSE Machine implementation
from Symbols.Rator import Rator
from Symbols.Eta import Eta
from Symbols.E import E
from Symbols.B import B
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

class CSEMachine:
    def __init__(self, control, stack, environment):
        self.set_control(control)
        self.set_stack(stack)
        self.set_environment(environment)
    
    def set_control(self, control):
        self.control = control
    
    def set_stack(self, stack):
        self.stack = stack
    
    def set_environment(self, environment):
        self.environment = environment
    
    def execute(self):
        current_environment = self.environment[0]
        j = 1
        
        while self.control:
            # Uncomment for debugging
            # self.print_control()
            # self.print_stack()
            # self.print_environment()
            
            # pop last element of the control
            #current_symbol = self.control[-1]
            current_symbol=self.control.pop()
            
            # rule no. 1
            if isinstance(current_symbol, Id):
                self.stack.insert(0, current_environment.lookup(current_symbol))
            
            # rule no. 2
            elif isinstance(current_symbol, Lambda):
                current_symbol.set_environment(current_environment.get_index())
                self.stack.insert(0, current_symbol)
            
            # rule no. 3, 4, 10, 11, 12 & 13
            elif isinstance(current_symbol, Gamma):
                next_symbol = self.stack.pop(0)
                
                # lambda (rule no. 4 & 11)
                if isinstance(next_symbol, Lambda):
                    lambda_obj = next_symbol
                    e = E(j)
                    j += 1
                    
                    if len(lambda_obj.identifiers) == 1:
                        temp = self.stack.pop(0)
                        e.values[lambda_obj.identifiers[0]] = temp
                    else:
                        tup = self.stack.pop(0)
                        for i, id in enumerate(lambda_obj.identifiers):
                            e.values[id] = tup.symbols[i]
                    for env in self.environment:
                        if env.get_index() == lambda_obj.get_environment():
                            e.set_parent(env)
                    current_environment = e
                    self.control.append(e)
                    self.control.append(lambda_obj.get_delta())
                    self.stack.insert(0, e)
                    self.environment.append(e)
                
                # tup (rule no. 10)
                elif isinstance(next_symbol, Tup):
                    tup = next_symbol
                    i = int(self.stack.pop(0).get_data())
                    self.stack.insert(0, tup.symbols[i-1])
                
                # ystar (rule no. 12)
                elif isinstance(next_symbol, Ystar):
                    lambda_obj = self.stack.pop(0)
                    eta = Eta()
                    eta.set_index(lambda_obj.get_index())
                    eta.set_environment(lambda_obj.get_environment())
                    eta.set_identifier(lambda_obj.identifiers[0])
                    eta.set_lambda(lambda_obj)
                    self.stack.insert(0, eta)
                
                # eta (rule no. 13)
                elif isinstance(next_symbol, Eta):
                    eta = next_symbol
                    lambda_obj = eta.get_lambda()
                    self.control.append(Gamma())
                    self.control.append(Gamma())
                    self.stack.insert(0, eta)
                    self.stack.insert(0, lambda_obj)
                
                # builtin functions
                else:
                    if next_symbol.get_data() == "Print":
                        # do nothing
                        pass
                    elif next_symbol.get_data() == "Stem":
                    
                        s=self.stack.pop(0)
                        s.set_data(s.get_data()[0])
                        self.stack.insert(0, s)
                    elif next_symbol.get_data() == "Stern":
                        
                        s=self.stack.pop(0)
                        s.set_data(s.get_data()[1:])
                        self.stack.insert(0, s)
                    elif next_symbol.get_data() == "Conc":
                        
                        s1=self.stack.pop(0)
                        s2=self.stack.pop(0)
                        s1.set_data(s1.get_data() + s2.get_data())
                        self.stack.insert(0, s1)
                    elif next_symbol.get_data() == "Order":
                        
                        tup=self.stack.pop(0)
                        n = Int(str(len(tup.symbols)))
                        self.stack.insert(0, n)
                    elif next_symbol.get_data() == "Null":
                        # implement
                        pass
                    elif next_symbol.get_data() == "Itos":
                        # implement
                        pass
                    elif next_symbol.get_data() == "Isstring":
                        # implement Isstring function
                        if isinstance(self.stack[0], Str):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Isstring":
                        if isinstance(self.stack[0], Str):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Istuple":
                        if isinstance(self.stack[0], Tup):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Isdummy":
                        if isinstance(self.stack[0], Dummy):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Istruthvalue":
                        if isinstance(self.stack[0], Bool):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
                    elif next_symbol.get_data() == "Isfunction":
                        if isinstance(self.stack[0], Lambda):
                            self.stack.insert(0, Bool("true"))
                        else:
                            self.stack.insert(0, Bool("false"))
                        self.stack.pop(1)
            
            # rule no. 5
            elif isinstance(current_symbol, E):
                self.stack.pop(1)
                
                self.environment[current_symbol.get_index()].set_is_removed(True)
                y = len(self.environment)
                while y > 0:
                    if not self.environment[y-1].get_is_removed():
                        current_environment = self.environment[y-1]
                        break
                    else:
                        y -= 1
            
            # rule no. 6 & 7
            elif isinstance(current_symbol, Rator):
                if isinstance(current_symbol, Uop):
                    rator = current_symbol
                    rand = self.stack.pop(0)
                    self.stack.insert(0, self.apply_unary_operation(rator, rand))
                
                if isinstance(current_symbol, Bop):
                    rator = current_symbol
                    rand1 = self.stack[0]
                    rand2 = self.stack[1]
                    rand1 = self.stack.pop(0)
                    rand2 = self.stack.pop(0)
                    self.stack.insert(0, self.apply_binary_operation(rator, rand1, rand2))
            
            # rule no. 8
            elif isinstance(current_symbol, Beta):
                if self.stack[0].get_data() == "true":
                    self.control.pop()
                else:
                    self.control.pop(-2)
                self.stack.pop(0)
            
            # rule no. 9
            elif isinstance(current_symbol, Tau):
                tau = current_symbol
                tup = Tup()
                for _ in range(tau.get_n()):
                    tup.symbols.append(self.stack[0])
                    self.stack.pop(0)
                self.stack.insert(0, tup)
            
            elif isinstance(current_symbol, Delta):
                self.control.extend(current_symbol.symbols)
            
            elif isinstance(current_symbol, B):
                self.control.extend(current_symbol.symbols)
            
            else:
                self.stack.insert(0, current_symbol)


    def write_stack_to_file(self, file_path):
        with open(file_path, 'a') as file:
            for symbol in self.stack:
                file.write(symbol.get_data())
                if isinstance(symbol, (Lambda, Delta, E, Eta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")

    def write_control_to_file(self, file_path):
        with open(file_path, 'a') as file:
            for symbol in self.control:
                file.write(symbol.get_data())
                if isinstance(symbol, (Lambda, Delta, E, Eta)):
                    file.write(str(symbol.get_index()))
                file.write(",")
            file.write("\n")
    
    def clear_file(file_path):
        open(file_path, 'w').close()
                
    def print_environment(self):
        for symbol in self.environment:
            print(f"e{symbol.get_index()} --> ", end="")
            if symbol.get_index() != 0:
                print(f"e{symbol.get_parent().get_index()}")
            else:
                print()

    def covert_string_to_bool(self, data):
        if data == "true":
            return True
        elif data == "false":
            return False            
    
    def apply_unary_operation(self, rator, rand):
        if rator.get_data() == "neg":
            val = int(rand.get_data())
            return Int(str(-1 * val))
        elif rator.get_data() == "not":
            val = self.covert_string_to_bool(rand.get_data())
            return Bool(str(not val).lower())
        else:
            return Err()
    
    def apply_binary_operation(self, rator, rand1, rand2):
        # Apply binary operation
        if rator.get_data() == "+":
            val1 = int(rand1.get_data())
            val2 = int(rand2.get_data())
            return Int(str(val1 + val2))
        elif rator.data == "-":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 - val2))
        elif rator.data == "*":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 * val2))
        elif rator.data == "/":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(int(val1 / val2)))
        elif rator.data == "**":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Int(str(val1 ** val2))
        elif rator.data == "&":
            val1 = self.covert_string_to_bool(rand1.data)
            val2 = self.covert_string_to_bool(rand2.data)
            return Bool(str(val1 and val2).lower())
        elif rator.data == "or":
            val1 = self.covert_string_to_bool(rand1.data)
            val2 = self.covert_string_to_bool(rand2.data)
            return Bool(str(val1 or val2).lower())
        elif rator.data == "eq":
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 == val2).lower())
        elif rator.data == "ne":
            val1 = rand1.data
            val2 = rand2.data
            return Bool(str(val1 != val2).lower())
        elif rator.data == "ls":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 < val2).lower())
        elif rator.data == "le":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool((val1 <= val2))
        elif rator.data == "gr":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 > val2).lower())
        elif rator.data == "ge":
            val1 = int(rand1.data)
            val2 = int(rand2.data)
            return Bool(str(val1 >= val2).lower())
        elif rator.data == "aug":
            if isinstance(rand2, Tup):
                rand1.symbols.extend(rand2.symbols)
            else:
                rand1.symbols.append(rand2)
            return rand1
        else:
            return Err()

    def get_tuple_value(self, tup):
        temp = "("
        for symbol in tup.symbols:
            if isinstance(symbol, Tup):
                temp += self.get_tuple_value(symbol) + ", "
            else:
                temp += symbol.get_data() + ", "
        temp = temp[:-2] + ")"  # Remove last comma and space, add closing parenthesis
        return temp
    
    def get_answer(self):
        self.execute()
        if isinstance(self.stack[0], Tup):
            return self.get_tuple_value(self.stack[0])
        return self.stack[0].get_data()