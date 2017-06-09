from os.path import join, dirname

import sys

from lexical_analysis.lexical_analysis import LexicalAnalysis
from syntax_parser.parser import Parser


class Generator:
    def __init__(self, tree, errors_listing):
        self.tree = tree
        self.error_listing = errors_listing
        self.procedure_identifier = str(self.tree.root.children[0][0].children[1][0].children[0][0].children[0][0])
        self.parameters = []
        self.constants = []

    def _check_parameters(self, declarations_list):
        if str(declarations_list.children[0][0]) == 'empty':
            return

        parameter = str(declarations_list.children[0][0].children[0][0].children[0][0].children[0][0])
        if parameter == self.procedure_identifier or parameter in self.parameters:
            self.error_listing.error('Identifier {} is already defined'.format(parameter))
            sys.exit(1)

        self.parameters.append(parameter)
        self._check_parameters(declarations_list.children[1][0])

    def _assembler_constants(self):
        declarations_list = self.tree.root.children[0][0].children[4][0].children[0][0].children[0][0].children[1][0]
        return self._const_declarations_to_asm(declarations_list)

    def _const_declarations_to_asm(self, declarations_list):
        if str(declarations_list.children[0][0]) == 'empty':
            return ''
        constant = declarations_list.children[0][0]
        identifier = str(constant.children[0][0].children[0][0].children[0][0])

        if identifier == self.procedure_identifier or identifier in self.parameters:
            self.error_listing.error('Identifier {} is already defined'.format(identifier))
            sys.exit(1)
        if identifier in self.constants:
            self.error_listing.error('You cannot redefine constant {}'.format(identifier))
            sys.exit(1)

        self.constants.append(identifier)
        assembler_constant = '{identifier} equ {value}\n'.format(identifier=identifier,
                                                                 value=constant.children[2][0].children[0][0])
        return assembler_constant + self._const_declarations_to_asm(declarations_list.children[1][0])

    def generate_code(self):
        self._check_parameters(self.tree.root.children[0][0].children[2][0].children[1][0])
        with open(join(dirname(__file__), 'asm_template.txt')) as template:
            return template.read().format(self._assembler_constants())

if __name__ == '__main__':
    with LexicalAnalysis(join(dirname(__file__), '../lexical_analysis/tests/', 'test_correct')) as L:
        p = Parser(L.get_lexemes_string())
    p.parse_program()
    with open(join(dirname(__file__), '../listing.log'), 'w') as listing:
        listing.write(Generator(p.tree, p.error_listing).generate_code())
