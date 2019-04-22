"""Base module for fyda."""
import importlib
import json
import os
import pickle
import warnings
from configparser import ConfigParser
from io import BytesIO

import boto3
import numpy as np
import pandas as pd

from . import options
from .errorhandling import NoShortcutError


# TODO
# Prefix assignment for duplicate names. Get rid of nasty warning.
# ?? Option values for behavior with duplicates. (Overwrite/keep/rename)
# Sanity checks for file assignment in .fydarc. Possibly get flexible there.
# Future idea: some way to search through files/shortcuts; like fuzzy search


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
def _get_conf():  # Allows the user to change configuration path dynamically

    importlib.reload(options)

    if not options.CONFIG_LOCATION:
        return options.locate_config()

    return options.CONFIG_LOCATION


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

        if (not os.path.exists(_get_conf())) and make_config:
            self.add_section('directories')
            self.add_section('data')
            _write_config(self)

        self.read(_get_conf())


class DataBank:
    """
    Interact with the system's data automatically.

    Parameters
    ----------
    root : str
        Path to root data folder. If none is provided, uses the default from
        ``.fydarc`` given by the ``conf_path`` parameter.

    Attributes
    ----------
    shortcuts : dict
        A mapping of shortcut values to their respective file objects.
    tree : dict
        The file tree representation of the ``root`` folder. Each folder can be
        accessed as successive ``dict`` keys, e.g.
        tree['level`']['level2'][...].
    readers : dict
        Maps between shortcuts and the required data reader for that file.

    Methods
    -------
    :meth:`DataBank.deposit`
    :meth:`DataBank.withdraw`
    :meth:`DataBank.root_to_dict`
    :meth:`DataBank.refresh`
    """

    def __init__(self, root=None):

        if root is None:
            pc = ProjectConfig()
            self._root = os.path.abspath(pc['directories']['root'])
        else:
            self._root = root
        self._data = {}
        self._reader_map = {}
        self._filetree = self.root_to_dict(self._root)

    # We access attributes this way because dict is mutable
    # TODO: any way to warn people when they try to change these?
    @property
    def tree(self):
        return self._filetree.copy()

    @property
    def shortcuts(self):
        return self._data.copy()

    @property
    def readers(self):
        return self._reader_map.copy()

    def _determine_path(self, input_string):
        """Determine the actual file location, based on input string."""

        pc = ProjectConfig()

        # .fydarc takes priority
        if input_string in pc['data'].keys():
            return os.path.join(self._root, pc['data'][input_string])

        try:  # Second check shortcuts
            filename = self.shortcuts[input_string]
        except KeyError:

            if os.path.splitext(input_string)[1] == '':
                raise NoShortcutError(input_string)

            filename = os.path.join(self._root, input_string)

        try:  # Then see if it is a path relative to data root
            with open(filename):
                pass
        except (FileNotFoundError, PermissionError):
            # Otherwise, just take original string
            filename = input_string

        return filename

    def deposit(self, filename, shortcut=None, reader=None, error='raise'):
        """
        Store a shortcut and reader reference for the given file name.

        Parameters
        ----------
        filename : str
            Name of the file to store.
        shortcut : str
            Shortcut to deposit.
        reader : callable, (optional)
            If provided, maps shortcut to this callable whenever the data is
            called to open. If none is provided, a reader will be automatically
            assigned.
        error : str
            If set to 'ignore', ignores any errors when picking a file reader.
        """

        # TODO ``determine_shortcut`` logic that double checks all names and
        #   adapts to duplicates.
        if shortcut is None:
            shortcut = filename
        # TODO if shortcut is not None and shortcut already exists, determine
        #   what to do.
        if reader is None:
            reader = _pick_reader(filename, error=error)
        if (shortcut in self._reader_map) & options.SHOW_WARNINGS:
            warnings.warn('Non-unique file shortcut "%s" overwritten!'
                          % shortcut)

        # TODO move update logic?
        self._reader_map.update({shortcut: reader})
        self._data.update({shortcut: filename})

    def withdraw(self, data_name, reader=None):
        """
        Automatically load data, given shortcut to file.

        Parameters
        ----------
        data_name : str
            Shortcut or filename.
        reader : callable, (optional)
            A function that takes either a string or object with a "read"
            method.

        Returns
        -------
        data
            Data as read by ``reader``.
        """

        filename = self._determine_path(data_name)

        if reader is None:
            try:
                reader = self.readers[data_name]
            except KeyError:
                reader = _pick_reader(filename)

        return _decode(reader, filename)

    def root_to_dict(self, root, auto_deposit=True):
        """
        Recursively convert root folder to native Python dictionary.

        Parameters
        ----------
        root : str or path-like
            Path to root folder.
        auto_deposit : bool
            If True, automatically call :meth:`DataBank.deposit` on any files
            found through the recursion to the ``shortcuts`` dict.

        Notes
        -----
        Modified from `this`<https://btmiller.com/2015/03/17/represent-file
        -structure-as-yaml-with-python.html>_ example by Blake Miller.

        """

        directory = {}

        for root_dir, dirnames, filenames in os.walk(root):
            dn = os.path.basename(root_dir)
            directory[dn] = {}

            for f in filenames:
                filepath = os.path.join(root, f)
                # TODO this logic should move to deposit function
                shortcut = os.path.splitext(f)[0]
                directory[dn].update({shortcut: f})

                if auto_deposit:
                    # TODO pass ``None`` for shortcut here. Let deposit figure
                    self.deposit(filepath, shortcut=shortcut)

            if dirnames:
                for d in dirnames:
                    directory[dn].update(
                        self.root_to_dict(os.path.join(root, d)))

            break  # We break here to stop the os.walk from doubling back

        return directory

    def refresh(self):
        """Rerun :meth:`DataBank.root_to_dict` to refresh file tree and deposit
        any new data."""

        self._filetree = self.root_to_dict(self._root)


# -----------------------------------------------------------------------------
# Module-level library
# -----------------------------------------------------------------------------
def _check_bucket(bucket_name):
    """Sanity check on S3 bucket configuration."""

    if bucket_name is None:
        try:
            pc = ProjectConfig()
            bucket_name = pc['directories']['s3_bucket']
        except KeyError:
            msg = ("Can't determine s3 bucket name. Either pass the "
                   "bucket_name explicitly, or add an s3_bucket "
                   "configuration value under ['directories'] in your .fydarc")
            raise TypeError(msg)

    return bucket_name


def _decode(reader, filename):
    """Successively try different methods to open ``filename`` with
    ``reader``."""

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
    """Reader selection based on ``filename`` extension."""

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
def data_path(shortcut, root=None):
    """
    Return the absolute path to the file referenced by ``shortcut``.

    Parameters
    ----------
    shortcut : str
        Shortcut reference for the file.
    root : str
        Root directory to use with :class:`DataBank`.

    Returns
    -------
    path : str
        Absolute path to file.

    """

    db = DataBank(root)

    if shortcut in db.shortcuts:
        return db.shortcuts[shortcut]
    else:
        try:
            pc = ProjectConfig()
            return os.path.join(pc['directories']['root'],
                                pc['data'][shortcut])
        except KeyError:
            raise NoShortcutError(shortcut)


def load(file_name):
    """
    Load data intelligently.

    Parameters
    ----------
    file_name : str or path-like
        Files to load. These can be shortcuts or file paths.
    """

    db = DataBank()
    return db.withdraw(file_name)


def load_s3(file_name, bucket_name=None, reader=None, **kwargs):
    """
    Read a file from S3.

    Parameters
    ----------
    file_name : str
        Absolute name of the file object as represented in S3 bucket.
    bucket_name : str, (optional)
        Bucket to load object from. If none used, uses bucket specification in
        ``.fydarc``.
    reader : callable, (optional)
        Function capable of reading the file. If none is passed, one will be
        automatically assigned based on the file extension.
    kwargs
        Additional keyword arguments to pass to file reader.

    Returns
    -------
    data
        As read by reader object
    """

    bucket_name = _check_bucket(bucket_name)

    if reader is None:
        reader = _pick_reader(file_name)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    with BytesIO() as data:
        bucket.download_fileobj(file_name, data)
        data.seek(0)  # move back to the beginning after writing
        obj = reader(data, **kwargs)

    return obj
