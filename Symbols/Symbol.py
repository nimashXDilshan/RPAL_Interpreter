# symbol.py

class Symbol:
    def __init__(self, data: str):
        self.data = data

    def set_data(self, data: str):
        self.data = data

    def get_data(self) -> str:
        return self.data
