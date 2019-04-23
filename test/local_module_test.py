"""Test suite for fyda base functions."""
import os
import fyda


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
RCPATH = os.path.join(CURRENT_DIR, '.fydarc')


def fydarc_checks():
    """Basic checks for dealing with the .fydarc file."""

    # If a fydarc exists, remove it.
    if os.path.exists(RCPATH):
        os.remove(RCPATH)
    assert ~os.path.exists(RCPATH)

    # Initialize a new fydarc
    fyda.options.CONFIG_LOCATION = RCPATH
    db = fyda.DataBank()
    assert os.path.exists(RCPATH)

    # TODO test where root is set (default, set with ProjectConfig, etc.)
    # TODO check whats inside DataBank against static file

    # TODO rebasing not working correctly. Look through:
    #   1. _forbid tree values
    #   2. encoding and rebasing process.
    for val in db.shortcuts:
        print(val, db.shortcuts[val])

    for val in db._forbid:
        print(val, db._forbid[val])

    # TODO create data folder with all possible combinations


def main():
    fydarc_checks()


if __name__ == '__main__':
    main()
