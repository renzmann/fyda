"""
Basic data handling library.
"""
import os
import warnings
import numpy as np
import pandas as pd
from .errorhandling import ConfigurationError
from .errorhandling import ReaderError
from .configurate import ProjectConfig
from .configurate import EXCEL_EXTENSIONS
from .configurate import _config_exists
from .configurate import get_shortcut


SHOW_WARNINGS = True


def _data_reader(filepath):
    filename, extension = os.path.splitext(filepath)

    if extension == '':
        config = ProjectConfig()
        _, extension = os.path.splitext(config['data'][filename])
    if extension in EXCEL_EXTENSIONS:
        return pd.read_excel
    if extension == '.csv':
        return pd.read_csv
    if extension in ['.pickle', '.pkl']:
        return pd.read_pickle
    if extension == '.json':
        return pd.read_json
    if extension in ['.sas7bdat', '.xport']:
        return pd.read_sas
    if extension in ['.npy', '.npz']:
        return np.load

    raise ReaderError()


def _pave_inputs(input_path, *args):
    for arg in args:
        config = ProjectConfig()
        name, _ = os.path.splitext(arg)

        if name in config['data'].keys():
            filename = config['data'][name]
            arg_file = os.path.join(input_path, filename)
        elif arg in config['data'].values():
            arg_file = os.path.join(input_path, arg)
        else:
            raise ConfigurationError(arg)
        yield arg_file


def load_data(*data_filenames, **kwargs):
    """
    Load specified data.

    Parameters
    ----------
    data_filenames : optional
        By default this will be the list of names given in configuration under the
        ``data`` keyword.

    kwargs : optional
        Additional arguments passed to the data reader.

    Returns
    -------
    data : tuple or DataFrame
        Data as DataFrames in order specified by configuration file. If there
        is only only file, return that DataFrame. Otherwise, return a tuple of
        DataFrames


    .. note::

       **Supported file extensions**

          - Excel: .xlsx
          - Flat files: .csv
          - Pandas pickle: .pickle, .pkl
          - JSON: .json
          - SAS: .sas7bdat, .xport


    Examples
    --------
    fyda is flexible with how it handles ``load_data`` calls. If no
    arguments are passed, it will by default return everything specified
    under ``data`` in ``config.ini``. The data listed there should be found
    in the ``input`` folder also given in ``config.ini``.

    >>> import fyda
    >>> fyda.summary('data')
    [data]
    iris=iris.csv
    >>> data = fyda.load_data()
    >>> data.head()
       sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  class_name
    0                5.1               3.5                1.4               0.2      setosa
    1                4.9               3.0                1.4               0.2      setosa
    2                4.7               3.2                1.3               0.2      setosa
    3                4.6               3.1                1.5               0.2      setosa
    4                5.0               3.6                1.4               0.2      setosa


    You can also specify the dataset by name.

    >>> data = fyda.load_data('iris.csv')

    Or, if you assigned a shortcut name, you can use that too.

    >>> data = fyda.load_data('iris')

    You can also pass additional keyword arguments to the data reader.

    >>> fyda.load_data('iris', nrows=2)
       sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  class_name
    0                5.1               3.5                1.4               0.2      setosa
    1                4.9               3.0                1.4               0.2      setosa

    """

    config = ProjectConfig()
    if not data_filenames:
        data_filenames = config['data'].values()

    directories = config['directories']
    input_path = os.path.join(os.path.expanduser(directories['input_folder']))
    all_inputs = list(_pave_inputs(input_path, *data_filenames))
    data_list = []

    for enum in enumerate(all_inputs):
        count = enum[0]                  # Elements of data_filenames may or
        file_path = enum[1]              # may not have file extensions, so we
        filename = data_filenames[count] # have the _data_reader call take care
        reader = _data_reader(filename)  # of parsing through them.

        if _config_exists(filename):
            kwargs.update(dict(config[filename]))
        else:
            try:
                shortcut = get_shortcut(filename)
                kwargs.update(dict(config[shortcut]))
            except KeyError:
                if SHOW_WARNINGS:
                    msg = ('Could not find keyword configurations for "{0}".'
                           ' To suppress this warning, use'
                           ' fyda.add_option(\'{0}\')'
                           ' to add a blank configuration'
                           ' section for this data file; or set'
                           ' fyda.util.SHOW_WARNINGS = False to suppress all'
                           ' warnings.'
                          ).format(filename)
                    warnings.warn(msg)

        table = reader(file_path, **kwargs)
        data_list.append(table)

    if len(data_list) == 1:
        return data_list[0]

    return tuple(data_list)


def summary(*sections):
    """
    Print a summary of the configuration for given option.

    Parameters
    ----------
    sections : str, optional
        Sections to print information for. If none given, prints entire
        summary.
    """
    config = ProjectConfig()
    if not sections:
        sections = config.sections()
    for section in set(sections) - set(['shortcut_map']):
        print('[{}]'.format(section))
        for key, value in config[section].items():
            print('{} = {}'.format(key, value))
        print('\n')
