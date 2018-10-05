"""Container for fyda-specific exception handling."""
class ConfigurationError(Exception):
    """Raised when user tries to use data that has not been configured."""
    def __init__(self, unconfigured):
        msg = ('The option "{}" has not been configured for use with fyda. '
               'See the documentation for how to configure new data and '
               'options.'
              ).format(unconfigured)

        super().__init__(msg)


class ExcelConfigError(Exception):
    """Raised when an excel file is read but there is no keyword config."""
    def __init__(self, unconfigured):
        msg = (('Excel file "{}" not '
                'configured! See documentation on how to '
                'configure excel file for fyda.'
               ).format(unconfigured))
        super().__init__(msg)


class OptionExistsError(Exception):
    """Raised when user tries to set a configuration that already exists."""
    def __init__(self, section, option):
        msg = ('An option called "{}" already exists. '
               'To overwrite this option, first delete it '
               'using fyda.remove_{}. Or, to change this '
               'behavior permanently, set '
               'fyda.configurate.ALLOW_OVERWRITE = True.'
              ).format(option, section)
        super().__init__(msg)


class ReaderError(Exception):
    """Raised when the data reader cannot parse the filetype."""
    def __init__(self):
        msg = ('Data reader could not parse the filetype. Check the '
               'file extension to ensure it is correct in the configuration '
               'and that it is a supported extension.')
        super().__init__(msg)
