class Node:
    def __init__(self, info):
        self._info = info
        #self.children is a list of tuples with the following structure (node, edge)
        self._children = []

    @property
    def info(self):
        return self._info

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def add_child(self, info, edge=None):
        child = Node(info)
        self._children.append((child, edge))
        return child

    def __str__(self):
        return self._info