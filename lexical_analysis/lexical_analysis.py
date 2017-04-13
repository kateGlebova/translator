from lexical_analysis.map import Map


# "0" dg
# "1" -
# "2" lt
# "3" dm
# "4" (
# "5" ws
# "6" other

class LexicalAnalysis:
    ciphered_lexemes = []

    def __init__(self, filename):
        self.filename = filename
        self.buffer = ''
        self.constants_table = Map('tables/constants.json')
        self.delimiters_table = Map('tables/delimiters.json')
        self.identifiers = Map('tables/identifiers.json')
        self.key_words = Map('tables/key_words.json')
        self.symbols = Map('tables/symbols.json')
        self.processing_functions = {
            "0": self.process_constant,
            "1": self.process_negative_constant,
            "2": self.process_identifier,
            "3": self.process_delimiter,
            "4": self.process_parant,
            "5": self.process_whitespace,
            "6": self.process_invalid
        }

        with open(self.filename) as f:
            self.process_program(f)

    def get_character(self, f):
        character = f.read(1)
        if character:
            return {'char': character, 'attribute': self.symbols[str(ord(character))]}
        return None

    def process_program(self, f):
        character = self.get_character(f)
        #how to generate and save lexeme code


    def process_constant(self, f, char):
        self.buffer += char
        character = self.get_character(f)
        while character and character['attribute'] == "0":
            self.buffer += character['char']
            character = self.get_character(f)
        return character

    def process_negative_constant(self, f, char):
        self.buffer += char
        character = self.get_character(f)
        if character['attribute'] == "0":
            return self.process_constant(f, character)
        self.process_invalid()

    def process_identifier(self, f, char):
        self.buffer += char
        character = self.get_character(f)
        while character and character['attribute'] in ("0", "2"):
            self.buffer += character['char']
            character = self.get_character(f)
        return character

    def process_delimiter(self, f, char):
        self.buffer += char
        return self.get_character(f)

    def process_parant(self, f, char):
        character = self.get_character(f)
        if character['char'] != '*':
            self.buffer += '('
            return character
        return self.process_comment_text(f)

    def process_comment_text(self, f):
        character = self.get_character(f)
        while character and character['char'] != '*':
            character = self.get_character(f)
        if not character:
            self.process_invalid()
        return self.process_comment_end(f)

    def process_comment_end(self, f):
        character = self.get_character(f)
        while character and character['char'] == '*':
            character = self.get_character(f)
        if not character:
            self.process_invalid()
        if character['char'] == ')':
            return self.get_character(f)
        return self.process_comment_text(f)

    def process_whitespace(self, f):
        character = self.get_character(f)
        while character and character['attribute'] == "5":
            character = self.get_character(f)
        return character

    def process_invalid(self):
        # todo: create exceptions
        raise Exception('Invalid character.')
