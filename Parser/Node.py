class Node:
    def __init__(self, node_type, value, noOfChildren):
        self.type = node_type
        self.value = value
        self.noOfChildren = noOfChildren  # root node depth is 0
