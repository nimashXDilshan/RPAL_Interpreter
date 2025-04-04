from Symbols.Symbol import Symbol
from Symbols.Id import Id
from Symbols.Lambda import Lambda

class Eta(Symbol):
    def __init__(self):
        super().__init__("eta")
        self.index = None
        self.environment = None
        self.identifier = None  # Should be an instance of Id
        self.lambda_ = None     # Should be an instance of Lambda

    def set_index(self, i):
        self.index = i

    def get_index(self):
        return self.index

    def set_environment(self, e):
        self.environment = e

    def get_environment(self):
        return self.environment

    def set_identifier(self, identifier: Id):
        self.identifier = identifier

    def set_lambda(self, lambda_: Lambda):
        self.lambda_ = lambda_

    def get_lambda(self):
        return self.lambda_
