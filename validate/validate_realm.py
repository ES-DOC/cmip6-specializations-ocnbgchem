"""
.. module:: realm_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 scientific realm specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from utils import validate_std



def validate(ctx):
    """Validates a scientific realm specialization.

    :param ValidationContext ctx: Validation contextual information.

    """
    # Set helper vars.
    mod = ctx.realm

    # Validate standard attributes.
    validate_std(ctx)

    # Validate CONTRIBUTORS.
    if not hasattr(ctx.module, 'CONTRIBUTORS'):
        ctx.error("CONTRIBUTORS property is missing")
    elif not isinstance(ctx.module.CONTRIBUTORS, str):
        ctx.error("CONTRIBUTORS property must be a string")

    # Validate CHANGE_HISTORY.
    if not hasattr(ctx.module, 'CHANGE_HISTORY'):
        ctx.error("CHANGE_HISTORY property is missing")
    elif not isinstance(ctx.module.CHANGE_HISTORY, list):
        ctx.error("CHANGE_HISTORY property must be a list")
    elif [i for i in ctx.module.CHANGE_HISTORY if not isinstance(i, tuple) or len(i) != 4]:
        ctx.error("CHANGE_HISTORY entries must be 4 member tuples: (version, date, comment, who)")


    # Validate REALM.
    if not hasattr(mod, "REALM"):
        ctx.error("REALM is missing")
    elif not mod.REALM == ctx.realm_key:
        ctx.error("REALM must be = {}".format(ctx.realm_key))

    # Validate GRID.
    if not hasattr(mod, "GRID"):
        ctx.error("GRID is missing")
    elif not mod.GRID == "{}_grid".format(ctx.realm_key):
        ctx.error("GRID must be = {}".format("{}_grid".format(ctx.realm_key)))

    # Validate KEY_PROPERTIES.
    if not hasattr(mod, "KEY_PROPERTIES"):
        ctx.error("KEY_PROPERTIES property is missing")
    elif not mod.KEY_PROPERTIES == "{}_key_properties".format(ctx.realm_key):
        ctx.error("KEY_PROPERTIES must be = {}".format("{}_key_properties".format(ctx.realm_key)))

    # Validate PROCESSES.
    if not hasattr(mod, "PROCESSES"):
        ctx.error("PROCESSES property is missing")
    elif not isinstance(mod.PROCESSES, list):
        ctx.error("PROCESSES must be a list of process keys")
    else:
        process_keys = [p.__name__ for p in ctx.processes]
        for process_key in mod.PROCESSES:
            if process_key not in process_keys:
                err = "invalid process key: {}".format(process_key)
                ctx.error(err)
