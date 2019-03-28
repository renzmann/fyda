"""Library for error handling."""


# -----------------------------------------------------------------------------
# Custom Error Classes
# -----------------------------------------------------------------------------
class NoShortcutError(Exception):
    """Raised when a shortcut is used but not found."""
    def __init__(self, shortcut):
        msg = ('It appears you are trying to use the value "{}" as a shortcut,'
               ' but this value cannot be found in the shortcut tree. Check '
               'the file name you are trying to access and/or that the '
               'shortcut is configured in your .fydarc').format(shortcut)
        super().__init__(msg)
