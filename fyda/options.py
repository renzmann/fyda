import os
import os.path as op


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
# Select config file based on heirarchy of selection
#    1. CWD
#    2. Project level
#    3. Install location
#    4. User home
#    5. (System level)
def locate_config(config_name='.fydarc', sysvar='FYDA_HOME'):

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


conf_path = locate_config()
