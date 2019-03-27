import os
import os.path as op


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SHOW_WARNINGS = True
CONFIG_LOCATION = None


# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
def locate_config(config_name='.fydarc', sysvar='FYDA_HOME'):
    """
    Locate the configuration file following a prioritized hierarchy.

    Parameters
    ----------
    config_name : str
        Name of the config file to look for.
    sysvar : str
        System-level variable that fyda will use when looking for a
        configuration file.

    Returns
    -------
    path : str
        Path to the configuration file. If the file is not found in any of the
        locations specified in the hierarchy, then the location to where fyda
        is installed is returned.

    Notes
    -----
    The hierarchy for file location prioritization is:

    1. CWD
    2. Project level
    3. Install location
    4. User home
    5. (System level)
    """

    # If a config is in the current working directory, prioritize it
    cwd = op.abspath(config_name)

    # If fyda is included at the top level of module
    project = op.abspath(
        op.join(op.dirname(__file__), '..', '..', config_name))

    # If fyda is used to manage a whole project
    install = op.abspath(op.join(op.dirname(__file__), '..', config_name))

    # If fyda is used for user management
    user = op.expanduser(op.join('~', config_name))

    try:
        system = op.join(os.environ[sysvar], config_name)
    except KeyError:
        system = ''

    for path in (cwd, project, install, user, system):
        if op.exists(path):
            return path

    return project

