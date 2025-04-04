from Symbols.Rand import Rand

class Id(Rand):
    def __init__(self, data):
        super().__init__(data)

    def get_data(self):
        return super().get_data()
