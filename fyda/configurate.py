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
    :class:`configparser.ConfigParser` : configuration parsing class
    """
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
        print(('Section "{}" sucessfully removed.'
              ).format(section))
        _write_config(config)
    else:
        print('Section not removed! Check that it exists.')



def _config_exists(section, option=None):
    config = ProjectConfig()

    if option is None:
        return section in config.sections()

    return option in config.options(section)


def _config_add_or_change(section, key=None, value=None):
    config = ProjectConfig()

    if not _config_exists(section):
        config.add_section(section)
        _write_config(config)

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
    :meth:`add_data` : add data to config
    :meth:`add_directory` : add a directory to config
    :meth:`remove_directory` : remove a directory from config
    """
    config = ProjectConfig()
    for shortcut in shortcuts:
        filename = config['data'][shortcut]
        _, ext = os.path.splitext(filename)

        if ext in EXCEL_EXTENSIONS:
            config.remove_section(shortcut)

        _config_remove('data', shortcut)


def add_directory(**kwargs):
    """
    Add director(y/ies) to fyda configuration.

    Parameters
    ----------
    kwargs : str
        Keywords passed as shortcut=directory.

    See Also
    --------
    :meth:`remove_directory` : remove a directory from configuration
    :meth:`add_data` : add data to configuration
    :meth:`remove_data` : remove data from configuration

    Examples
    --------

        >>> fyda.summary('directories')
        [directories]

        >>> fyda.add_directory(place1='first place')
        >>> fyda.summary('directories')
        [directories]
        place1 = first place

        >>> fyda.add_directory(place2='second place', place3='third place')
        >>> fyda.summary('directories')
        [directories]
        place1 = first place
        place2 = second place
        place3 = third place
    """
    for shortcut, directory in kwargs.items():
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
    :meth:`add_directory` : add directory to configuration
    :meth:`add_data` : add data to configuration
    :meth:`remove_data`: remove data from configuration
    """
    _config_remove('directories', directory)


def set_data_root(directory):
    """
    Change the root folder for data storage.

    Parameters
    ----------
    directory : str
        Full filepath to the directory.


    Notes
    -----
        This data root will always be referenced with the shortcut
        ``input_folder``.


    See Also
    --------
    :meth:`add_data` : add data to configuration
    :meth:`add_directory` : add directory to configuration
    :meth:`remove_data` : remove data from configuration
    :meth:`remove_directory` : remove directory from configuration
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
    :meth:`add_data` : add data to configuration
    """
    if mode == 'add':
        _config_add_or_change(shortcut, key, value)
    elif mode == 'remove_option':
        _config_remove(shortcut, key)
    elif mode == 'remove':
        _config_delete_section(shortcut)


def add_option(shortcut, **kwargs):
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
    if not kwargs:
        add_section(shortcut)
    for keyword in kwargs:
        _configure_option(shortcut,
                          key=keyword,
                          value=kwargs[keyword],
                          mode='add')


def remove_option(shortcut, *args):
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
                          mode='remove_option')


def add_section(*section_names):
    """
    Add sections to config.

    Parameters
    ----------
    section_names : str
        Section titles to add.
    """
    for section in section_names:
        _config_add_or_change(section)


def remove_section(*section_names):
    """
    Remove a section from the config entirely.

    Parameters
    ----------
    section_name : str
        Name of the section to delete.

    """
    for section in section_names:
        _configure_option(section, mode='remove')


def sections():
    """
    Return the sections in the project config.

    Returns
    -------

    sections : list
        Names of section titles.
    """
    config = ProjectConfig()
    return config.sections()


def add_data(**kwargs):
    """
    Add a data file to the fyda configuration.

    Parameters
    ----------
    kwargs
        Keyword pairs to add, formatted as shortcut=filename.

    See Also
    --------
    :meth:`remove_data` : remove data from configuration
    :meth:`add_directory` : add directory to configuration
    :meth:`remove_directory` : remove directory from configuration
    """
    for shortcut, filename in kwargs.items():
        if _config_exists('data', shortcut) & (not ALLOW_OVERWRITE):
            raise OptionExistsError('data', shortcut)
        _config_add_or_change('data', shortcut, filename)
        _config_add_or_change('shortcut_map', filename, shortcut)

        _, extension = os.path.splitext(filename)
        if extension in EXCEL_EXTENSIONS:
            _config_add_or_change(shortcut, None, None)


def dir_path(dir_name):
    """
    Return full directory path from shortcut name.

    Parameters
    ----------
    dir_name : str
        Shortcut name to access directory path with.

    Returns
    -------
    directory : str
        Directory filepath.
    """
    config = ProjectConfig()
    # TODO error handling
    return os.path.expanduser(config['directories'][dir_name])


def data_path(data_name):
    """
    Return full file path from shortcut name.

    Parameters
    ----------
    data_name : str
        Shortcut name to access data path with.

    Returns
    -------
    filepath : str
        File path.
    """
    config = ProjectConfig()
    full_path = os.path.expanduser(
        os.path.join(
            dir_path('input_folder'),
            config['data'][data_name]
        )
    )
    return full_path
