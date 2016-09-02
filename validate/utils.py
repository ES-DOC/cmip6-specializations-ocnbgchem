"""
.. module:: utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validation utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import imp
import os

import constants



def get_cim_id(module):
    """Reurns the expected cim id of a module.

    """
    parts = [module.__name__.split("_")[0], "_".join(module.__name__.split("_")[1:])]
    parts = [i for i in parts if i]

    return "cmip6.{}".format(".".join(parts))


def validate_std(ctx):
    """Validates a modules standard attributes.

    """
    # Validate AUTHORS.
    if not hasattr(ctx.module, 'AUTHORS'):
        ctx.error("AUTHORS property is missing")
    elif not isinstance(ctx.module.AUTHORS, str):
        ctx.error("AUTHORS property must be a string")

    # Validate AUTHORS.
    if not hasattr(ctx.module, 'CONTACT'):
        ctx.error("CONTACT property is missing")
    elif not isinstance(ctx.module.CONTACT, str):
        ctx.error("CONTACT property must be a string")

    # Validate DESCRIPTION.
    if not hasattr(ctx.module, 'DESCRIPTION'):
        ctx.error("DESCRIPTION property is missing")
    elif not isinstance(ctx.module.DESCRIPTION, str):
        ctx.error("DESCRIPTION property must be a string")

    # Validate QC_STATUS.
    if not hasattr(ctx.module, 'QC_STATUS'):
        ctx.error("QC_STATUS property is missing")
    elif ctx.module.QC_STATUS not in constants.QC_STATES:
        ctx.error("QC_STATUS is invalid. Valid set = {}".format(list(constants.QC_STATES)))


def validate_spec(ctx, attr, types=(dict, )):
    """Validates a specialization collection.

    """
    if not hasattr(ctx.module, attr):
        ctx.error("{} is missing".format(attr))
    elif not isinstance(getattr(ctx.module, attr), collections.OrderedDict):
        ctx.error("{} must be an OrderedDict".format(attr))
    else:
        for key, defn in getattr(ctx.module, attr).items():
            if not isinstance(defn, types):
                err = "{}[{}]: must be a {}".format(attr, key, " or ".join([i.__name__ for i in types]))
                ctx.error(err)

def get_specializations(input_dir, realm):
    """Returns specialization modules organized by type.

    :param str input_dir: Directory within which modules reside.
    :param str realm: Name of realm being processed.

    """
    def is_target(filename):
        """Returns flag indicating whether a module is a specialization target or not.

        """
        return not filename.startswith('_') and \
               filename.endswith('.py') and \
               filename.startswith(realm)

    # Load specialization modules.
    modules = sorted([i for i in os.listdir(input_dir) if is_target(i)])
    modules = [os.path.join(input_dir, m) for m in modules]
    modules = [(m.split("/")[-1].split(".")[0], m) for m in modules]
    modules = [imp.load_source(name, fpath) for name, fpath in modules]

    # Organize specialization modules.
    realm = grid = key_properties = None
    processes = []
    for module in modules:
        if realm is None:
            realm = module
        elif module.__name__.endswith('_grid'):
            grid = module
        elif module.__name__.endswith('_key_properties'):
            key_properties = module
        else:
            processes.append(module)

    return realm, grid, key_properties, processes


def set_default(target, attr, value):
    """Sets a default value upon an object.

    """
    try:
        getattr(target, attr)
    except AttributeError:
        setattr(target, attr, value)
