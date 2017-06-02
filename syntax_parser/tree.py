from syntax_parser.node import Node


class Tree:
    def __init__(self, root=None):
        self._root = root

    @property
    def root(self):
        return self._root

    def add_node(self, info, edge=None, parent=None):
        """
        Add node to the tree.
        :param info: str | node info
        :param edge: str | edge info
        :param parent: Node | parent node
        :return: Node | created node
        """
        if not parent and not self._root:
            self._root = Node(info)
            return self._root

        if not parent:
            raise Exception('No parent node specified.')

        if not isinstance(parent, Node):
            raise TypeError('Parent should be of Node type.')

        return parent.add_child(info, edge)

    def display_tree(self):
        self._display(0, self._root)

    def _display(self, tab_level, node, edge=None):
        if not node:
            return

        output = '\t' * tab_level + node.info
        if edge:
            output += '(%s)' % edge
        print(output)

        children = node.children
        for child in children:
            self._display(tab_level + 1, child[0], child[1])