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
            "1": self.process_constant,
            "2": self.process_identifier,
            "3": self.process_delimiter,
            "4": self.process_comment,
            "5": self.process_whitespace,
            "6": self.process_invalid
        }

        with open(self.filename) as f:
            self.process_program(f)

    def get_character(self, f):
        character = f.read(1)
        if character:
            return {'char': character, 'attribute': self.symbols[str(ord(character))] }
        return None

    def process_program(self, f):
        character = self.get_character(f)

    def process_constant(self, f):
        pass

    def process_identifier(self, f):
        pass

    def process_delimiter(self, f):
        pass

    def process_comment(self, f):
        pass

    def process_whitespace(self, f):
        pass

    def process_invalid(self, f):
        pass