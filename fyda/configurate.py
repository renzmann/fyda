"""
Configuration management module.
"""
import os
from configparser import ConfigParser

CONF_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'config.ini'
    )
)

def _open_conf():
    cp = ConfigParser()
    cp.read(CONF_PATH)
    return cp


def ProjectConfig():
    """
    Configuration manager.
    """
    return _open_conf()


def _edit_config(section, key, value):
    config = ProjectConfig()
    config[section][key] = value
    with open(CONF_PATH, 'w') as configfile:
        config.write(configfile)


def add_data(shortcut, filename):
    """
    Add a data file to the fyda configuration.

    Parameters
    ----------
    shortcut : str
        Short name to call data file with

    filename : str
        full file name relative to ``input_path`` in the directories
        section of configuration
    """
    _edit_config('data', shortcut, filename)


def add_directory(shortcut, directory):
    """
    Add a directory to the fyda configuration.

    Parameters
    ----------
    shortcut : str
        Short name to call directory with.
    directory : str
        Full filepath to the directory. 
    """
    _edit_config('directories', shortcut, directory)


def set_data_root(directory):
    """
    Change the root folder for data storage.

    Parameters
    ----------
    directory : str
        Full filepath to the directory.

    .. note::
       This data root will always be referenced with the shortcut
       ``input_folder``.

    """
    _edit_config('directories', 'input', directory)
