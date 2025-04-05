from Symbols.Symbol import Symbol

class Lambda(Symbol):
    def __init__(self, index):
        super().__init__("lambda")
        self.index=index
        self.environment =None
        self.identifiers = []  # List of Id objects
        self.delta = None

    
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
