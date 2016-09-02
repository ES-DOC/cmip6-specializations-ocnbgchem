"""
.. module:: key_properties_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 scientific key properties specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from validate_details import validate as validate_details
from validate_details_container import validate as validate_details_container
from validate_enum import validate as validate_enum
from utils import set_default
from utils import validate_spec
from utils import validate_std


# Set of fields.
_FIELDS = {
    'DETAILS': (dict, tuple),
    'ENUMERATIONS': (dict, ),
    'EXTENT': (dict, ),
    'EXTENT_DETAILS': (dict, tuple),
    'EXTRA_CONSERVATION_PROPERTIES': (dict, ),
    'EXTRA_CONSERVATION_PROPERTIES_DETAILS': (dict, tuple),
    'RESOLUTION': (dict, ),
    'RESOLUTION_DETAILS': (dict, tuple),
    'TUNING_APPLIED': (dict, ),
    'TUNING_APPLIED_DETAILS': (dict, tuple)
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
    mod = ctx.key_properties

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
    for field in {
        'EXTENT',
        'EXTRA_CONSERVATION_PROPERTIES',
        'RESOLUTION',
        'TUNING_APPLIED'
        }:
        for key, obj in getattr(mod, field).items():
            ctx.errors[mod] += _validate(mod, field, key, obj)
