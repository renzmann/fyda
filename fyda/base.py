import os
import pickle
import pandas as pd
import numpy as np
import json
import warnings


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(__file__, '..', '..', 'data'))


# -----------------------------------------------------------------------------
# Module-level library
# -----------------------------------------------------------------------------
def _decode(reader, filename):

    try:  # First check if the reader is an open ``read`` method.
        return reader()
    except TypeError:
        pass

    try:  # Next possibility is that the reader just needs a string reference
        return reader(filename)
    except TypeError:
        pass

    try:  # Finally, check if we can open the string reference to read.
        with open(filename, 'r') as fileobj:
            return reader(fileobj)
    except UnicodeDecodeError:
        with open(filename, 'rb') as fileobj:
            return reader(fileobj)


def _pick_reader(filename, error='raise'):

    extension = os.path.splitext(filename)[-1]

    if extension in ['.xlsx']:
        return pd.read_excel
    if extension == '.csv':
        return pd.read_csv
    if extension in ['.pickle', '.pkl']:
        return pickle.load
    if extension in ['.npy', '.npz']:
        return np.load
    if extension == '.json':
        return json.load
    if extension in ['.sas7bdat', '.xport']:
        return pd.read_sas
    if extension == '.txt':
        def open_reader(x):
            with open(x, 'r') as fileobj:
                return fileobj.read()
        return open_reader

    if error == 'ignore':
        return

    raise TypeError("Extension '%s' not implemented yet." % extension)


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------
class DataBank:

    def __init__(self, root=ROOT):

        self._root = root
        self._data = {}
        self._reader_map = {}
        self._filetree = self.root_to_dict(self._root)

    # We access attributes this way because dict is mutable
    @property
    def tree(self):
        return self._filetree.copy()

    @property
    def shortcuts(self):
        return self._data.copy()

    @property
    def readers(self):
        return self._reader_map.copy()

    def deposit(self, filename, shortcut=None, reader=None, error='raise'):

        if shortcut is None:
            shortcut = filename
        if reader is None:
            reader = _pick_reader(filename)
        if shortcut in self._reader_map:
            warnings.warn('Non-unique file shortcut "%s" overwritten!'
                          % shortcut)

        self._reader_map.update({shortcut: reader})
        self._data.update({shortcut: filename})

    def withdraw(self, data_name, reader=None):

        # TODO missing name handling
        filename = self._data[data_name]

        if reader is None:
            try:
                reader = self._reader_map[data_name]
            except KeyError:
                reader = _pick_reader(os.path.splitext(filename)[-1])

        return _decode(reader, filename)

    def root_to_dict(self, root, auto_deposit=True):
        """Modified from `this`<https://btmiller.com/2015/03/17/represent-file
        -structure-as-yaml-with-python.html>_ example by Blake Miller. """

        # TODO prefix assignment for duplicate names.
        directory = {}

        for root_dir, dirnames, filenames in os.walk(root):
            dn = os.path.basename(root_dir)
            directory[dn] = {}

            for f in filenames:
                filepath = os.path.join(root, f)
                shortcut = os.path.splitext(f)[0]
                directory[dn].update({shortcut: f})

                if auto_deposit:
                    self.deposit(filepath, shortcut=shortcut)

            if dirnames:
                for d in dirnames:
                    directory[dn].update(
                        self.root_to_dict(os.path.join(root, d)))

            break  # We break here to stop the os.walk from doubling back

        return directory

    def refresh(self):

        self._filetree = self.root_to_dict(self._root)
