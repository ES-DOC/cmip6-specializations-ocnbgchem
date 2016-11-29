"""
.. module:: utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validation utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

import constants



def get_cim_id(module):
    """Reurns the expected cim id of a module.

    """
    parts = [module.__name__.split("_")[0], "_".join(module.__name__.split("_")[1:])]
    parts = [i for i in parts if i]

    return "cmip6.{}".format(".".join(parts))


def validate_std(ctx, module, sections=[]):
    """Validates a module's standard attributes.

    """
    # Set current specializations module being processed.
    ctx.module = module

    # Validate expected fields.
    for field in {'AUTHORS', 'CONTACT', 'DESCRIPTION', 'QC_STATUS'}:
        if not hasattr(module, field):
            ctx.error("{} property is missing".format(field))
        elif not isinstance(getattr(module, field), (str, unicode)):
            ctx.error("{} property must be a string".format(field))
        # TODO: use regex

    # Validate expected section.
    for section in sections:
        if not hasattr(module, section):
            ctx.error("{} is missing".format(section))
        elif not isinstance(getattr(module, section), collections.OrderedDict):
            ctx.error("{} must be an OrderedDict".format(section))
        else:
            for key, obj in getattr(module, section).items():
                if not isinstance(key, (str, unicode)):
                    err = "{}: all keys must be strings".format(section)
                elif len(key.strip()) == 0:
                    err = "{}: all keys must be strings".format(section)
                elif not isinstance(obj, dict):
                    err = "{}[{}]: must be a dictionary".format(section, key)
                    ctx.error(err)


def set_default(target, attr, value):
    """Sets a default value upon an object.

    """
    try:
        getattr(target, attr)
    except AttributeError:
        setattr(target, attr, value)
