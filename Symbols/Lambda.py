from Symbols.Symbol import Symbol
from Symbols.Id import Id
from Symbols.Delta import Delta

class Lambda(Symbol):
    def __init__(self, i):
        super().__init__("lambda")
        self.set_index(i)
        self.identifiers = []  # List of Id objects
        self.delta = None
    
    def set_index(self, i):
        self.index = i
    
    def get_index(self):
        return self.index
    
    def set_environment(self, n):
        self.environment = n
    
    def get_environment(self):
        return self.environment
    
    def set_delta(self, delta):
        self.delta = delta
    
    def get_delta(self):
        return self.delta
