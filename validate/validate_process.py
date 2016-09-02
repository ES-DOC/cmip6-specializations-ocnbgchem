"""
.. module:: process_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 scientific process specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from validate_details import validate as validate_details
from validate_enum import validate as validate_enum
from validate_sub_process import validate as validate_sub_process
from validate_sub_process_detail import validate as validate_sub_process_detail
from utils import set_default
from utils import validate_spec
from utils import validate_std



# Map of fields to acceptable file value types.
_FIELDS = {
    'DETAILS': (dict, tuple),
    'ENUMERATIONS': (dict, ),
    'SUB_PROCESSES': (dict, ),
    'SUB_PROCESS_DETAILS': (dict, ),
}


def _validate_sub_process(mod, key, obj):
    """Validates an associated sub-prcess.

    """
    def _get_invalid_detail_keys():
        """Gets invalid sub-process detail keys.

        """
        keys = [(k, "{}:{}".format(key, k)) for k in obj['details']]

        return [k[0] for k in keys if not k[1] in mod.SUB_PROCESS_DETAILS]


    errors = validate_sub_process(key, obj)
    if not errors:
        for key_ in _get_invalid_detail_keys():
            err = "has an invalid detail key: {}".format(key_)
            errors.append(err)

    return ["SUB_PROCESSES['{}'] {}".format(key, e) for e in errors]


def validate(ctx):
    """Validates a scientific process specialization.

    :param ValidationContext ctx: Validation contextual information.

    """
    # Set helper vars.
    mod = ctx.process

    # Set defaults for optional fields.
    for field in _FIELDS.keys():
        set_default(mod, field, collections.OrderedDict())

    # Level-1 validation.
    validate_std(ctx)
    for field, types in _FIELDS.items():
        validate_spec(ctx, field, types)

    # Escape if level-1 errors.
    if ctx.errors[mod]:
        return

    # Level-2 validation.
    for key, obj in mod.DETAILS.items():
        ctx.errors[mod] += validate_details(key, obj, mod.ENUMERATIONS)
    for key, obj in mod.ENUMERATIONS.items():
        ctx.errors[mod] += validate_enum(key, obj)
    for key, obj in mod.SUB_PROCESSES.items():
        ctx.errors[mod] += _validate_sub_process(mod, key, obj)
    for key, obj in mod.SUB_PROCESS_DETAILS.items():
        ctx.errors[mod] += ["SUB_PROCESS_DETAILS['{}'] :: {}".format(key, e) for e in
                            validate_sub_process_detail(mod, key, obj)]
