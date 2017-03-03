"""
.. module:: validate_property.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a specialized CMIP6 scientific property.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

# Set of valid property cardinalities.
_CARDINALITIES = {'0.1', '1.1', '0.N', '1.N'}

# Set of valid property types.
_TYPES = {'bool', 'float', 'int', 'str'}

# Proeprty name regular expression.
_RE_NAME = '^[a-z_]+$'


def validate(prop, enums):
    """Validates a property specialization.

    :param tuple prop: Property being validated.
    :param tuple prop: Property being validated.

    :returns: Property validation errors.
    :rtype: list

    """
    name, typeof, cardinality, description = prop
    errors = []
    _validate_name(errors, name)
    _validate_type(errors, typeof, enums)
    _validate_cardinality(errors, cardinality)
    _validate_description(errors, description)

    return ["{} :: property {}".format(name, i) for i in errors]


def _validate_name(errors, name):
    """Validates a property's name.

    """
    if not isinstance(name, str):
        errors.append("name must be a string :: [{}]".format(name))
    elif len(name.strip()) == 0:
        errors.append("name must not be a zero length string")
    # TODO apply regex


def _validate_type(errors, typeof, enums):
    """Validates a property's type.

    """
    if not isinstance(typeof, (str, unicode)):
        errors.append("type must be a string :: {}".format(typeof))
    elif typeof.startswith("ENUM:"):
        if typeof[5:] not in enums:
            errors.append("type enum key is invalid :: {}".format(typeof))
    elif typeof not in _TYPES:
        errors.append("type must be either simple or an enum :: {}".format(typeof))


def _validate_cardinality(errors, cardinality):
    """Validates a property's cardinality.

    """
    if cardinality not in _CARDINALITIES:
        errors.append("cardinality is invalid :: [{}]".format(cardinality))


def _validate_description(errors, description):
    """Validates a property's description.

    """
    if not isinstance(description, str):
        errors.append("description must be a string :: [{}]".format(description))
    elif len(description.strip()) == 0:
        errors.append("description must not be a zero length string")
