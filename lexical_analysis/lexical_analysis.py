from os.path import join, dirname

from table import Table


# "0" dg
# "1" -
# "2" lt
# "3" dm
# "4" (
# "5" ws
# "6" other

class LexicalAnalysis:

    def __init__(self, filename):
        self.filename = filename
        self.buffer = ''
        self.constants = Table('tables/constants.json', clear=True)
        self.delimiters = Table('tables/delimiters.json')
        self.identifiers = Table('tables/identifiers.json', clear=True)
        self.key_words = Table('tables/key_words.json')
        self.symbols = Table('tables/symbols.json')
        self.processing_functions = {
            "0": self._process_constant,
            "1": self._process_negative_constant,
            "2": self._process_identifier,
            "3": self._process_delimiter,
            "4": self._process_parant,
            "5": self._process_whitespace,
            "6": self._process_invalid
        }
        self.lexemes_string = []
        self.current_row = 1
        self.current_column = 0

        with open(self.filename) as f:
            self.process_program(f)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.constants.save()
        self.identifiers.save()

    def get_character(self, f):
        character = f.read(1)
        self.current_column += 1
        if character:
            return {'char': character, 'attribute': self.symbols[str(ord(character))]}
        return None

    def process_program(self, f):
        character = self.get_character(f)
        while character:
            if character['char'] == '\n':
                self.current_row += 1
                self.current_column = 0

            lexeme_code, character = self.processing_functions[character['attribute']](f, character)

            if lexeme_code:
                self.lexemes_string.append((lexeme_code[0], self.current_row, lexeme_code[1]))

    def get_lexemes_string(self):
        return self.lexemes_string

    def _generate_code(self, table, lexeme):
        code = table.get_code(lexeme)
        lexeme_column = self.current_column - len(self.buffer)
        self.buffer = ''
        return str(code), lexeme_column

    def _process_constant(self, f, char):
        self.buffer += char['char']
        character = self.get_character(f)
        while character and character['attribute'] == "0":
            self.buffer += character['char']
            character = self.get_character(f)
        return self._generate_code(self.constants, self.buffer), character

    def _process_negative_constant(self, f, char):
        self.buffer += char['char']
        character = self.get_character(f)
        if character['attribute'] == "0":
            return self._process_constant(f, character)
        return self._process_invalid(f, character)

    def _process_identifier(self, f, char):
        self.buffer += char['char']
        character = self.get_character(f)
        while character and character['attribute'] in ("0", "2"):
            self.buffer += character['char']
            character = self.get_character(f)

        if self.buffer in self.key_words:
            return self._generate_code(self.key_words, self.buffer), character
        return self._generate_code(self.identifiers, self.buffer), character

    def _process_delimiter(self, f, char):
        self.buffer += char['char']
        return self._generate_code(self.delimiters, self.buffer), self.get_character(f)

    def _process_parant(self, f, char):
        character = self.get_character(f)
        if character['char'] != '*':
            self.buffer += '('
            return self._generate_code(self.delimiters, self.buffer), character
        return self._process_comment_text(f)

    def _process_comment_text(self, f):
        character = self.get_character(f)
        while character and character['char'] != '*':
            character = self.get_character(f)
        if not character:
            return self._process_invalid(f, character)
        return self._process_comment_end(f)

    def _process_comment_end(self, f):
        character = self.get_character(f)
        while character and character['char'] == '*':
            character = self.get_character(f)
        if not character:
            self._process_invalid(f, character)
        if character['char'] == ')':
            return None, self.get_character(f)
        return self._process_comment_text(f)

    def _process_whitespace(self, f, char):
        character = self.get_character(f)
        while character and character['attribute'] == "5":
            character = self.get_character(f)
        return None, character

    def _process_invalid(self, f, char):
        lexeme_column = self.current_column - len(self.buffer)

        if char:
            character = self.get_character(f)
            while character and character['attribute'] not in ("3", "4", "5"):
                character = self.get_character(f)
            return ("-1", lexeme_column), character

        return ("-1", lexeme_column), ''
