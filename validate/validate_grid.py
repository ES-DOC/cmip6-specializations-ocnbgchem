"""
.. module:: grid_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 scientific grid specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from validate_details import validate as validate_details
from validate_enum import validate as validate_enum
from validate_details_container import validate as validate_details_container
from utils import validate_spec
from utils import validate_std
from utils import set_default



# Set of fields.
_FIELDS = {
    'DETAILS': (dict, tuple),
    'ENUMERATIONS': (dict, ),
    'DISCRETISATION': (dict, ),
    'DISCRETISATION_DETAILS': (dict, )
    }


def _validate(mod, attr, key, obj):
    """Validates an associated details container.

    """
    details = getattr(mod, "{}_DETAILS".format(attr))
    errors = validate_details_container(key, obj, details)

    return ["{}['{}'] {}".format(attr, key, e) for e in errors]


def validate(ctx):
    """Validates a scientific grid specialization.

    :param ValidationContext ctx: Validation contextual information.

    """
    # Set helper vars.
    mod = ctx.grid

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
    for key, obj in mod.DISCRETISATION.items():
        ctx.errors[mod] += _validate(mod, "DISCRETISATION", key, obj)
