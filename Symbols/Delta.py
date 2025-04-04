from Symbols.Symbol import Symbol

class Delta(Symbol):
    def __init__(self, index):
        super().__init__("delta")
        self._index = index
        self.symbols = []

    def get_index(self):
        return self._index
     

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value
