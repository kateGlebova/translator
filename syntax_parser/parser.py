from logging import getLogger, FileHandler, ERROR, Formatter
import sys

from os.path import dirname, join

from lexical_analysis.lexical_analysis import LexicalAnalysis
from lexical_analysis.table import Table
from syntax_parser.tree import Tree


class Parser:
    constants = Table('tables/constants.json')
    delimiters = Table('tables/delimiters.json')
    identifiers = Table('tables/identifiers.json')
    key_words = Table('tables/key_words.json')

    RULES = {
        'signal-program': [1, [('program',)]],
        'program': [2, [('PROCEDURE', 'procedure-identifier', 'parameters-list', ';', 'block', ';')]],
        'block': [3, [('declarations', 'BEGIN', 'statements-list', 'END')]],
        'statements-list': [4, [('empty',)]],
        'parameters-list': [5, [('(', 'declarations-list', ')'), ('empty',)]],
        'declarations-list': [6, [('declaration', 'declarations-list'), ('empty',)]],
        'declaration': [7, [('variable-identifier', ':', 'attribute', ';')]],
        'attribute': [8, [('INTEGER', ), ('FLOAT',)]],
        'declarations': [9, [('constant-declarations',)]],
        'constant-declarations': [10, [('CONST', 'constant-declarations-list'), ('empty',)]],
        'constant-declarations-list': [11, [('constant-declaration', 'constant-declarations-list'), ('empty',)]],
        'constant-declaration': [12, [('constant-identifier', '=', 'constant', ';')]],
        'constant': [13, [(constant, ) for constant in constants]],
        'constant-identifier': [14, [('identifier', )]],
        'variable-identifier': [15, [('identifier', )]],
        'procedure-identifier': [16, [('identifier',)]],
        'identifier': [17, [(idn, ) for idn in identifiers]],
    }

    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.current_lexeme_idx = 0
        self.current_lexeme = self._get_current_lexeme()
        if self.current_lexeme and self.current_lexeme[0] == '-1':
            self.error_listing.error('Lexical error in a %s row, %s column' % (self.current_lexeme[1], self.current_lexeme[2]))
            self._next_lexeme()
        self.tree = Tree()
        self.error_listing = self._init_logger()

    def _get_element_code(self, element):
        if element in self.identifiers:
            return self.identifiers[element]
        if element in self.constants:
            return self.constants[element]
        if element in self.key_words:
            return self.key_words[element]
        if element in self.delimiters:
            return self.delimiters[element]
        return element

    def _get_current_lexeme(self):
        try:
            return self.lexemes[self.current_lexeme_idx]
        except IndexError:
            return None

    def parse_program(self):
        root = self.tree.add_node('signal-program')
        result, row, column = self._process_rule('signal-program', root, self.tree)
        if not result:
            self.error_listing.error('You made a syntax error in %s row, %s column.' % (row, column))
            sys.exit(1)
        else:
            self.tree.display_tree()

    def _process_rule(self, element, node, tree):
        if not element in self.RULES:
            element = self._get_element_code(element)
            row, column = self.current_lexeme[1:]
            if element == self.current_lexeme[0] or element == 'empty':
                if not element == 'empty':
                    self._add_lexeme_to_tree(tree, node, element, None)
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
                if not correct:
                    break
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
        logger_path = join(dirname(__file__), '../errors.log')
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
            self.error_listing.error('Lexical error in a %s row, %s column' % (self.current_lexeme[1], self.current_lexeme[2]))
            self.current_lexeme_idx += 1
            self.current_lexeme = self._get_current_lexeme()


if __name__ == "__main__":
    with LexicalAnalysis(join(dirname(__file__), '../lexical_analysis/tests/', 'test_correct')) as L:
        p = Parser(L.get_lexemes_string())
    p.parse_program()