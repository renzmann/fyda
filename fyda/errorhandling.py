class OptionExistsError(Exception):
    """Raised when user tries to set a configuration that already exists."""
    def __init__(self, section, option):
        msg = ('An option called "{}" already exists. '
               'To overwrite this option, first delete it '
               'using fyda.remove_{}. Or, to change this '
               'behavior permanently, set fyda.util.ALLOW_OVERWRITE = True.'
              ).format(option, section)

        super().__init__(msg)


class ConfigurationError(Exception):
    """Raised when user tries to use data that has not been configured."""
    def __init__(self, unconfigured):
        msg = ('The option "{}" has not been configured for use with fyda. '
               'See the documentation for how to configure new data and '
               'options.'
              ).format(unconfigured)

        super().__init__(msg)
