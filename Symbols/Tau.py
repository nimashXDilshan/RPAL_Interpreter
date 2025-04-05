from Symbols.Symbol import Symbol

#
class Tau(Symbol):
    def __init__(self, n):
        super().__init__("tau")
        self.set_n(n)

    def set_n(self, n):
        self.n = n

    def get_n(self):
        return self.n
