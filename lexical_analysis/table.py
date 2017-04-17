from json import load, dump

import sys


class Table:
    """
    Dict wrapper initialised from a json file with following structure:
    [ dict with initial values, dict with processed valued ]
    """

    def __init__(self, filename, clear=False):
        """
        Initialise dict from the json file.
        :param filename: name of the json file
        :param clear: True, the dict is filled only with initial values
                      False, the dict is filled with both initial and processed values
        """
        self.filename = filename
        self.table = self._init_dict(clear)
        self.last_code = self._init_last_code()

    def __getitem__(self, key):
        try:
            return self.table[0][key]
        except KeyError:
            return self.table[1][key]

    def __contains__(self, item):
        return item in self.table[0] or item in self.table[1]

    def _init_dict(self, clear):
        """
        :param clear: True, the second dict of the array in file is removed
        """
        table = []

        try:
            with open(self.filename, 'r') as f:
                file_table = load(f)
        except FileNotFoundError:
            print('No such table "%s"' % self.filename)
            sys.exit(1)

        table.append(file_table[0])

        if clear or len(file_table) < 2:
            with open(self.filename, 'w') as f:
                dump(table, f)
            table.append({})
        else:
            table.append(file_table[1])

        return table

    def _init_last_code(self):
        try:
            last_code = max(max(self.table[0].values()), max(self.table[1].values()))
        except ValueError:
            with open('tables/ranges.json') as ranges:
                last_code = load(ranges).get(self.filename, 2000)
        finally:
            return int(last_code) + 1

    def get_code(self, entry):
        if entry in self:
            return self[entry]
        else:
            self.table[1][entry] = self.last_code
            self.last_code += 1

    def save(self):
        with open(self.filename, 'w') as f:
            dump(self.table, f)
