"""
Configuration management module.
"""
import os
from configparser import ConfigParser
from .errorhandling import OptionExistsError

CONF_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'config.ini'
    )
)

ALLOW_OVERWRITE = False
EXCEL_EXTENSIONS = ['.xlsx']

class ProjectConfig(ConfigParser):
    """Configuration manager."""
    def __init__(self):
        super().__init__()
        self.read(CONF_PATH)


def _config_remove(section, option):
    config = ProjectConfig()
    is_removed = config.remove_option(section, option)
    if is_removed:
        print(('Section "{}", option "{}" sucessfully removed.'
              ).format(section, option))
    else:
        print('Option not removed! Check that it exists.')


def _config_delete_section(section):
    config = ProjectConfig()
    is_removed = config.remove_section(section)
    if is_removed:
        print(('Section "{}", sucessfully removed.'
              ).format(section))
    else:
        print('Section not removed! Check that it exists.')



def _config_exists(section, option=None):
    config = ProjectConfig()

    if option is None:
        return section in config.sections()

    return option in config.options(section)


def _config_add_or_change(section, key, value):
    config = ProjectConfig()

    if not _config_exists(section):
        config.add_section(section)

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

    See Also
    --------
    :meth:`remove_data`
    :meth:`add_directory`
    :meth:`remove_directory`
    """
    if _config_exists('data', shortcut) & (not ALLOW_OVERWRITE):
        raise OptionExistsError('data', shortcut)
    _config_add_or_change('data', shortcut, filename)

    _, extension = os.path.splitext(filename)
    if extension in EXCEL_EXTENSIONS:
        configure_excel(shortcut)



def remove_data(shortcut):
    """
    Remove a previously configured data reference.

    Parameters
    ----------
    shortcut : str
        Short name identifier for data file.

    See Also
    --------
    :meth:`add_data`
    :meth:`add_directory`
    :meth:`remove_directory`
    """
    config = ProjectConfig()
    filename = config['data'][shortcut]
    _, ext = os.path.splitext(filename)

    if ext in EXCEL_EXTENSIONS:
        config.remove_section(shortcut)

    _config_remove('data', shortcut)



def add_directory(shortcut, directory):
    """
    Add a directory to the fyda configuration.

    Parameters
    ----------
    shortcut : str
        Short name to call directory with.
    directory : str
        Full filepath to the directory.

    See Also
    --------
    :meth:`remove_directory`
    :meth:`add_data`
    :meth:`remove_data`
    """
    if _config_exists('directories', shortcut) & (not ALLOW_OVERWRITE):
        raise OptionExistsError('directory', shortcut)
    _config_add_or_change('directories', shortcut, directory)


def remove_directory(directory):
    """
    Remove a previously configured directory reference.

    Parameters
    ----------
    directory : str
        Short name identifier for directory

    See Also
    --------
    :meth:`add_directory`
    :meth:`add_data`
    :meth:`remove_data`
    """
    _config_remove('directories', directory)


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

    See Also
    --------
    :meth:`add_data`
    :meth:`add_directory`
    :meth:`remove_data`
    :meth:`remove_directory`
    """
    _config_add_or_change('directories', 'input', directory)


def configure_excel(shortcut, key=None, value=None, mode='add'):
    """
    Add or remove keyword pairs from excel configuration.

    Parameters
    ----------
    shortcut : str
        Short name identifier for excel file.

    See also
    --------
    :meth:`add_data`
    """
    if mode == 'add':
        _config_add_or_change(shortcut, key, value)
    elif mode == 'remove':
        _config_delete_section(shortcut)
