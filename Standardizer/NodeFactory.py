from Standardizer.Node import Node

class NodeFactory:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_node(data, depth, parent=None, children=None, is_standardized=False):
        if parent is None and children is None and is_standardized is False:
            # First method implementation
            node = Node()
            node.set_data(data)
            node.set_depth(depth)
            node.children = []
            return node
        else:
            # Second method implementation
            node = Node()
            node.set_data(data)
            node.set_depth(depth)
            node.set_parent(parent)
            node.children = children
            node.is_standardized = is_standardized
            return node