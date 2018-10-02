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
    return _open_conf()


def _edit_config(section, key, value):
    config = ProjectConfig()
    config[section][key] = value
    with open(CONF_PATH, 'w') as configfile:
        config.write(configfile)


def add_data(shortcut, filename):
    _edit_config('data', shortcut, filename)


def add_directory(shortcut, directory):
    _edit_config('directories', shortcut, directory)


def set_data_root(directory):
    _edit_config('directories', 'input', directory)
