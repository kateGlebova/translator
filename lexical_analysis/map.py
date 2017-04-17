from json import load, dump


class Map:
    """
    Dict wrapper initialised from a json file with following structure:
    [ dict with initial values, dict with processed valued ]
    """
    dictionary = {}

    def __init__(self, filename, clear=False):
        """
        Initialise dict from the json file.
        :param filename: name of the json file
        :param clear: True, the dict is filled only with initial values
                      False, the dict is filled with both initial and processed values
        """
        self.filename = filename
        self._init_dict(clear)

    def __getitem__(self, key):
        return self.dictionary[key]

    def _init_dict(self, clear):
        """
        :param clear: True, the second dict of the array in file is removed
        """
        with open(self.filename, 'r') as f:
            table = load(f)

        self.dictionary = table[0]

        if clear or len(table) < 2:
            table.pop()
            with open(self.filename, 'w') as f:
                dump(table, f)
        else:
            self.dictionary = dict(self.dictionary, **table[1])

    def add(self, key, value):
        self.dictionary[key] = value

    def save(self):
        with open(self.filename, 'w') as f:
            dump(self.dictionary, f)
