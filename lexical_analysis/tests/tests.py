import pytest
from os.path import dirname, join

from lexical_analysis.lexical_analysis import LexicalAnalysis


class TestLexicalAnalysis():
    test_cases_dir = dirname(__file__)

    def test_correct(self):
        answer = ('401', '1003', '4', '1004', '1', '1001', '2', '1005', '1', '1002', '3', '2',
                  '404', '1006', '0', '501', '2', '1007', '0', '502', '2', '402', '403', '2')
        with LexicalAnalysis(join(self.test_cases_dir, 'test_correct')) as L:
            assert L.get_lexemes_string() == answer

    def test_comment(self):
        answer = ('401', '1003', '2', '404', '1004', '0', '501', '2', '402', '403', '2')
        with LexicalAnalysis(join(self.test_cases_dir, 'test_comment')) as L:
            assert L.get_lexemes_string() == answer

    def test_wrong(self):
        answer = ('401', '-1', '1003', '2', '-1')
        with LexicalAnalysis(join(self.test_cases_dir, 'test_wrong')) as L:
            assert L.get_lexemes_string() == answer

if __name__ == '__main__':
    with LexicalAnalysis(join(dirname(__file__), 'test_correct')) as L:
        print(L.get_lexemes_string())
        print('Constants table')
        print(L.constants.table)
        print('Identifiers table')
        print(L.identifiers.table)
