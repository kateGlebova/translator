from json import load, dump


class Map:
    """
    Dict wrapper initialised from a json file with following structure:
    [ dict with initial values, dict with processed valued ]
    """
    dict = {}

    def __init__(self, filename, clear=False):
        """
        Initialise dict from the json file
        :param filename: name of the json file
        :param clear: True, the dict is filled only with initial values
                      False, the dict is filled with both initial and processed values
        """
        self.filename = filename
        self._init_dict(clear)

    # todo: add __getitem__

    def _init_dict(self, clear):
        """
        :param clear: True, the second dict of the array in file is removed
        """
        with open(self.filename, 'r') as f:
            table = load(f)

        self.dict = table[0]

        if clear:
            table.pop()
            with open(self.filename, 'w') as f:
                dump(table, f)
        else:
            self.dict = dict(self.dict, **table[1])

    def add(self, key, value):
        self.dict[key] = value

    def save(self):
        with open(self.filename, 'w') as f:
            dump(self.dict, f)
