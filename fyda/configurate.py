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


def _write_config(config):
    """Writes config to .ini file"""
    with open(CONF_PATH, 'w') as configfile:
        config.write(configfile)


class ProjectConfig(ConfigParser):
    """Configuration manager."""
    def __init__(self):
        super().__init__()

        if not os.path.exists(CONF_PATH):
            self.add_section('directories')
            self.add_section('data')
            _write_config(self)

        self.read(CONF_PATH)



def _config_remove(section, option):
    config = ProjectConfig()
    is_removed = config.remove_option(section, option)
    if is_removed:
        print(('Section "{}", option "{}" sucessfully removed.'
              ).format(section, option))
        _write_config(config)
    else:
        print('Option not removed! Check that it exists.')


def _config_delete_section(section):
    config = ProjectConfig()
    is_removed = config.remove_section(section)
    if is_removed:
        print(('Section "{}", sucessfully removed.'
              ).format(section))
        _write_config(config)
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

    if (key is None) or (value is None):
        return

    config[section][key] = value
    _write_config(config)


def get_shortcut(filename):
    """
    Return the shortcut for a given filename.

    Parameters
    ----------
    filename : str
        Relative to ``input`` from configuration

    Returns
    -------
    shortcut : str
        Shortcut name for file.
    """
    config = ProjectConfig()
    shortcut = config['shortcut_map'][filename]
    return shortcut


def remove_data(*shortcuts):
    """
    Remove a previously configured data reference.

    Parameters
    ----------
    shortcuts : str
        Short name identifier for data file.

    See Also
    --------
    :meth:`add_data`
    :meth:`add_directory`
    :meth:`remove_directory`
    """
    config = ProjectConfig()
    for shortcut in shortcuts:
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
    _config_add_or_change('directories', 'input_folder', directory)


def _configure_option(shortcut, key=None, value=None, mode='add'):
    """
    Add or remove keyword pairs from data configuration.

    Parameters
    ----------
    shortcut : str
        Short name identifier for data file.

    See also
    --------
    :meth:`add_data`
    """
    if mode == 'add':
        _config_add_or_change(shortcut, key, value)
    elif mode == 'remove_option':
        _config_remove(shortcut, key)
    elif mode == 'remove':
        _config_delete_section(shortcut)


def add_options(shortcut, **kwargs):
    """
    Add keyword-value pairs to configuration for data reading.

    Parameters
    ----------
    shortcut : str
        Short name identifier for data file.
    kwargs
        additional arguments passed to the appropriate data reader in
        :meth:`fyda.load_data`.
    """
    for keyword in kwargs:
        _configure_option(shortcut,
                          key=keyword,
                          value=kwargs[keyword],
                          mode='add')


def remove_options(shortcut, *args):
    """
    Remove options from data reading, referenced by keyword.

    Parameters
    ----------
    shortcut : str
        Short name identifier for data file.
    args
        Name(s) of keyword in option to remove.
    """
    for arg in args:
        _configure_option(shortcut,
                          key=arg,
                          mode='remove')


def add_data(**kwargs):
    """
    Add a data file to the fyda configuration.

    Parameters
    ----------
    kwargs
        Keyword pairs to add, formatted as shortcut=filename.

    See Also
    --------
    :meth:`remove_data`
    :meth:`add_directory`
    :meth:`remove_directory`
    """
    for shortcut, filename in kwargs.items():
        if _config_exists('data', shortcut) & (not ALLOW_OVERWRITE):
            raise OptionExistsError('data', shortcut)
        _config_add_or_change('data', shortcut, filename)
        _config_add_or_change('shortcut_map', filename, shortcut)

        _, extension = os.path.splitext(filename)
        if extension in EXCEL_EXTENSIONS:
            _config_add_or_change(shortcut, None, None)
