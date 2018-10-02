"""
Basic data handling library.
"""
import os
import pandas as pd

from .errorhandling import ConfigurationError
from .configurate import ProjectConfig
from configparser import ConfigParser


def _attribute_remover(att_type, data):
    data_ = data.copy()
    rm_atts = open_conf()[att_type]
    data_ = data_.drop(rm_atts, axis='columns')
    return data_


def _data_reader(filepath):
    filename, extension = os.path.splitext(filepath)

    if extension == '.xlsx':
        return pd.read_excel
    if extension == '.csv':
        return pd.read_csv
    if extension in ['.pickle', '.pkl']:
        return pd.read_pickle
    if extension == '.json':
        return pd.read_json
    if extension in ['.sas7bdat', '.xport']:
        return pd.read_sas

    raise ConfigurationError('Data reader not configured for file "%s"' % filename)


def _pave_inputs(input_path, *args):
    for arg in args:
        config = ProjectConfig()
        name, ext = os.path.splitext(arg)
        
        if name in config['data'].keys():
            filename = config['data'][name]
            arg_file = os.path.join(input_path, filename)
        elif arg in config['data'].values():
            arg_file = os.path.join(input_path, arg)
        else:
            raise ConfigurationError('data "{}" has not been '.format(arg),
                                     'added to the interface. ',
                                     'See documentation for how to add data ',
                                     'to fyda.')
        yield arg_file


def load_data(*data_filenames):
    """
    Load specified data.

    Parameters
    ----------
    args : optional, default None
        By default this will be the list of names given in conf.ini under the
        ``data_types`` keyword.

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
    >>> data.head()
       sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  class_name
    0                5.1               3.5                1.4               0.2      setosa
    1                4.9               3.0                1.4               0.2      setosa
    2                4.7               3.2                1.3               0.2      setosa
    3                4.6               3.1                1.5               0.2      setosa
    4                5.0               3.6                1.4               0.2      setosa


    Or, if you assigned a shortcut name, you can use that too.

    >>> data = fyda.load_data('iris')
    >>> data.head()
       sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  class_name
    0                5.1               3.5                1.4               0.2      setosa
    1                4.9               3.0                1.4               0.2      setosa
    2                4.7               3.2                1.3               0.2      setosa
    3                4.6               3.1                1.5               0.2      setosa
    4                5.0               3.6                1.4               0.2      setosa

    """

    config = ProjectConfig()
    if not data_filenames:
        data_filenames = config['data'].values()

    directories = config['directories']
    input_path = os.path.join(os.path.expanduser(directories['input_folder']))
    all_inputs = list(_pave_inputs(input_path, *data_filenames))
    data_list = []

    for enum in enumerate(all_inputs):
        count = enum[0]
        file_path = enum[1]
        filename = data_filenames[count]
        reader = _data_reader(filename)

        if reader is pd.read_excel:
            if filename in config.sections():
                shortcut = filename
            elif filename in config['data'].values():
                shortcut, _ = os.path.splitext(filename)
            else:
                raise ValueError('Excel file "{}" not '.format(filename),
                                 'configured! See documentation on how to ',
                                 'configure excel file for fyda.')
            xl_kwargs = dict(config.items(shortcut))
            table = reader(file_path, **xl_kwargs)
        else:
            table = reader(file_path)

        data_list.append(table)

    if len(data_list) == 1:
        return data_list[0]

    return tuple(data_list)
