# e.py

from Symbols.Symbol import Symbol
from typing import Optional

class Id:
    def __init__(self, data: str):
        self.data = data

    def get_data(self) -> str:
        return self.data

    def __eq__(self, other):
        return isinstance(other, Id) and self.data == other.data

    def __hash__(self):
        return hash(self.data)

class E(Symbol):
    def __init__(self, index: int):
        super().__init__("e")
        self.index = index
        self.parent: Optional[E] = None
        self.is_removed = False
        self.values: dict[Id, Symbol] = {}

    def set_index(self, i: int):
        self.index = i

    def get_index(self) -> int:
        return self.index

    def set_parent(self, e: 'E'):
        self.parent = e

    def get_parent(self) -> Optional['E']:
        return self.parent

    def set_is_removed(self, is_removed: bool):
        self.is_removed = is_removed

    def get_is_removed(self) -> bool:
        return self.is_removed

    def lookup(self, id: Id) -> Symbol:
        if id in self.values:
            return self.values[id]
        elif self.parent is not None:
            return self.parent.lookup(id)
        else:
            return Symbol(id.get_data())
