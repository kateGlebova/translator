from logging import getLogger, FileHandler, ERROR, Formatter
import sys

from os.path import dirname, join

from lexical_analysis.lexical_analysis import LexicalAnalysis
from lexical_analysis.table import Table
from syntax_parser.tree import Tree


class Parser:
    RULES = {
        'signal-program': [1, [('program',)]],
        'program': [2, [(('PROCEDURE', '401'), 'procedure-identifier', 'parameters-list', (';', '2'), 'block', (';', '2'))]],
        'block': [3, [('declarations', ('BEGIN', '402'), 'statements-list', ('END', '403'))]],
        'statements-list': [4, [('statement', 'statements-list'), ('empty',)]],
        'parameters-list': [5, [(('(', '4'), 'declarations-list', (')', '3')), ('empty',)]],
        'declarations-list': [6, [('declaration', 'declarations-list'), ('empty',)]],
        'declaration': [7, [('variable-identifier', (':', '1'), 'attribute', (';', '2'))]],
        'attribute': [8, [(('INTEGER', '1001'),), (('FLOAT', '1002'),)]],
        'declarations': [9, [('constant-declarations',)]],
        'constant-declarations': [10, [('404', 'constant-declarations-list'), ('empty',)]],
        'constant-declarations-list': [11, [('constant-declaration', 'constant-declarations-list'), ('empty',)]],
        'constant-declaration': [12, [('constant-identifier', ('=', '0'), 'constant', (';', '2'))]],
        'constant' : [13, [(constant, ) for constant in Table('tables/constants.json')]],
        'constant-identifier': [14, [('identifier', )]],
        'variable-identifier': [15, [('identifier', )]],
        'procedure-identifier': [16, [('identifier',)]],
        'identifier': [17, [(idn, ) for idn in Table('tables/identifiers.json')]],
        'statement': [18, [('variable-identifier', ('=', '0'), 'variable-identifier', 'operation', 'variable-identifier', (';', '2'))]],
        'operation': [19, [('operation-symbol', )]],
        'operation-symbol': [20, [(('+', '5'), ), (('*', '6'), ), (('/', '7'), )]]
    }

    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.current_lexeme_idx = 0
        self.current_lexeme = self._get_current_lexeme()
        if self.current_lexeme and self.current_lexeme[0] == '-1':
            self.listing.error('Lexical error in a %s row, %s column' % (self.current_lexeme[1], self.current_lexeme[2]))
            self._next_lexeme()
        self.tree = Tree()
        self.listing = self._init_logger()

    def _get_current_lexeme(self):
        try:
            return self.lexemes[self.current_lexeme_idx]
        except IndexError:
            return None

    def parse_program(self):
        root = self.tree.add_node('signal-program')
        result, row, column = self._process_rule('signal-program', root, self.tree)
        if not result:
            self.listing.error('You made a syntax error in %s row, %s column.' % (row, column))
        else:
            self.tree.display_tree()

    def _process_rule(self, element, node, tree):
        if not element in self.RULES:
            if isinstance(element, tuple):
                element = element[1]
            row, column = self.current_lexeme[1:]
            if element == self.current_lexeme[0] or element == 'empty':
                if not element == 'empty':
                    self._next_lexeme()
                return True, row, column
            return False, row, column

        rule = self.RULES[element]

        if len(rule[1]) == 1:
            correct = True
            for lexeme in rule[1][0]:
                new_node = self._add_lexeme_to_tree(tree, node, lexeme, rule[0])
                recursive_correct, row, column = self._process_rule(lexeme, new_node, tree)
                correct = correct and recursive_correct
            return correct, row, column

        if len(rule[1]) > 1:
            right_option = False
            option = 0
            while option < len(rule[1]) and right_option == False:
                subtree = Tree()
                subtree_node = subtree.add_node(node.info)
                right_option = True
                for lexeme in rule[1][option]:
                    new_node = self._add_lexeme_to_tree(subtree, subtree_node, lexeme, rule[0])
                    recursive_right_option, row, column = self._process_rule(lexeme, new_node, subtree)
                    right_option = right_option and recursive_right_option
                    if not right_option:
                        break
                option += 1

            if not right_option:
                return False, row, column

            node.children = subtree.root.children
            return True, row, column

    @staticmethod
    def _add_lexeme_to_tree(tree, node, lexeme, rule_number):
        """
        Add node to the tree or if the node is a lexeme from the table add both the lexeme and the lexeme code to the tree.
        """
        if isinstance(lexeme, tuple):
            new_node = tree.add_node(lexeme[1], rule_number, node)
            new_node = tree.add_node(lexeme[0], parent=new_node)
        else:
            new_node = tree.add_node(lexeme, rule_number, node)
        return new_node

    @staticmethod
    def _init_logger():
        logger_path = join(dirname(__file__), '../listing.log')
        with open(logger_path, 'w') as f:
            pass
        logger = getLogger('parser_listing')
        handler = FileHandler(logger_path)
        handler.setLevel(ERROR)
        handler.setFormatter(Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def _next_lexeme(self):
        self.current_lexeme_idx += 1
        self.current_lexeme = self._get_current_lexeme()
        while self.current_lexeme and self.current_lexeme[0] == '-1':
            self.listing.error('Lexical error in a %s row, %s column' % (self.current_lexeme[1], self.current_lexeme[2]))
            self.current_lexeme_idx += 1
            self.current_lexeme = self._get_current_lexeme()


if __name__ == "__main__":
    with LexicalAnalysis(join(dirname(__file__), '../lexical_analysis/tests/', 'test_correct')) as L:
        p = Parser(L.get_lexemes_string())
    p.parse_program()