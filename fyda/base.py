from io import BytesIO
import os
import boto3
import pickle
import pandas as pd
import numpy as np
import json
import warnings
from configparser import ConfigParser
from . import options


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
def _get_conf():  # Allows the user to change configuration path dynamically
    return options.conf_path


# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------
class ProjectConfig(ConfigParser):
    """
    Configuration manager.

    Notes
    -----
        This class is a wrapper around :class:`configparser.ConfigParser` with
        the added benefit of automatically reading the configuration file on
        instantiation. If the configuration file doesn't exist when
        :class:`ConfigParser` is called, it is created in the environment
        automatically.

    See also
    --------
    :py:class:`configparser.ConfigParser` : configuration parsing class
    """
    def __init__(self, make_config=True):
        super().__init__()

        if (not os.path.exists(_get_conf())) and (make_config):
            self.add_section('directories')
            self.add_section('data')
            _write_config(self)

        self.read(_get_conf())


class DataBank:

    def __init__(self, conf_path=_get_conf(), root=None):

        if root is None:
            pc = ProjectConfig()
            self._root = pc['directories']['root']
        else:
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
            reader = _pick_reader(filename, error='ignore')
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


# -----------------------------------------------------------------------------
# Module-level library
# -----------------------------------------------------------------------------
def _check_bucket(bucket_name):

    if bucket_name is None:
        try:
            pc = ProjectConfig()
            bucket_name = pc['directories']['s3_bucket']
        except KeyError:
            msg = ("Can't determine s3 bucket name. Either pass the "
                   "bucket_name explicitly, or add the s3_bucket "
                   "configuration value to your .fydarc")
            raise TypeError(msg)

    return bucket_name


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

    raise NotImplementedError("Extension '%s' not implemented yet."
                              % extension)


def _write_config(config):
    """Writes config to .ini file"""
    with open(_get_conf(), 'w') as configfile:
        config.write(configfile)


# -----------------------------------------------------------------------------
# Public library
# -----------------------------------------------------------------------------
def load_s3_obj(file_name, bucket_name=None, **kwargs):

    bucket_name = _check_bucket(bucket_name)
    reader = _pick_reader(file_name)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    with BytesIO() as data:
        bucket.download_fileobj(file_name, data)
        data.seek(0)    # move back to the beginning after writing
        obj = reader(data, **kwargs)

    return obj
