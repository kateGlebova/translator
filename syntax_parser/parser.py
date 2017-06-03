from logging import getLogger, FileHandler, ERROR, Formatter
import sys

from os.path import dirname, join

from lexical_analysis.lexical_analysis import LexicalAnalysis
from lexical_analysis.table import Table
from syntax_parser.tree import Tree


class Parser:
    RULES = {
        'signal-program': [1, [('program',)]],
        'program': [2, [('401', 'procedure-identifier', 'parameters-list', '2', 'block', '2')]],
        'block': [3, [('declarations', '402', 'statements-list', '403')]],
        'statements-list': [4, [('empty',)]],
        'parameters-list': [5, [('4', 'declarations-list', '3'), ('empty',)]],
        'declarations-list': [6, [('declaration', 'declarations-list'), ('empty',)]],
        'declaration': [7, [('variable-identifier', '1', 'attribute', '2')]],
        'attribute': [8, [('1001',), ('1002',)]],
        'declarations': [9, [('constant-declarations',)]],
        'constant-declarations': [10, [('404', 'constant-declarations-list'), ('empty',)]],
        'constant-declarations-list': [11, [('constant-declaration', 'constant-declarations-list'), ('empty',)]],
        'constant-declaration': [12, [('constant-identifier', '0', 'constant', '2')]],
        'constant' : [13, [(constant, ) for constant in Table('tables/constants.json')]],
        'constant-identifier': [14, [('identifier', )]],
        'variable-identifier': [15, [('identifier', )]],
        'procedure-identifier': [16, [('identifier',)]],
        'identifier': [17, [(idn, ) for idn in Table('tables/identifiers.json')]]
    }

    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.current_lexeme_idx = 0
        self.current_lexeme = self._get_current_lexeme()
        if self.current_lexeme and self.current_lexeme[0] == '-1':
            print('Lexical error in a %s row' % self.current_lexeme[1])
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
        if not self._process_rule('signal-program', root, self.tree):
            print('You made a syntax error.')

    def _process_rule(self, element, node, tree):
        if not element in self.RULES:
            if isinstance(element, tuple):
                element = element[1]
            if element == self.current_lexeme[0] or element == 'empty':
                if not element == 'empty':
                    self._next_lexeme()
                return True
            return False

        rule = self.RULES[element]

        if len(rule[1]) == 1:
            correct = True
            for lexeme in rule[1][0]:
                new_node = self._add_lexeme_to_tree(tree, node, lexeme, rule[0])
                correct = correct and self._process_rule(lexeme, new_node, tree)
            return correct

        if len(rule[1]) > 1:
            right_option = False
            option = 0
            while option < len(rule[1]) and right_option == False:
                subtree = Tree()
                subtree_node = subtree.add_node(node.info)
                right_option = True
                for lexeme in rule[1][option]:
                    new_node = self._add_lexeme_to_tree(subtree, subtree_node, lexeme, rule[0])
                    right_option = right_option and self._process_rule(lexeme, new_node, subtree)
                option += 1

            if not right_option:
                return False

            node.children = subtree.root.children
            return True

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
        logger = getLogger('parser_listing')
        handler = FileHandler('/Users/ivan/Katya/opt/parser_errors.log')
        handler.setLevel(ERROR)
        handler.setFormatter(Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def _next_lexeme(self):
        self.current_lexeme_idx += 1
        self.current_lexeme = self._get_current_lexeme()
        while self.current_lexeme and self.current_lexeme[0] == '-1':
            print('Lexical error in a %s row' % self.current_lexeme[1])
            self.current_lexeme_idx += 1
            self.current_lexeme = self._get_current_lexeme()


if __name__ == "__main__":
    with LexicalAnalysis(join(dirname(__file__), '../lexical_analysis/tests/', 'test_correct')) as L:
        p = Parser(L.get_lexemes_string())
    p.parse_program()
    p.tree.display_tree()