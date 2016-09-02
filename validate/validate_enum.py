"""
.. module:: enum_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 enumeration specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import re

import validate_enum_member



# Regular expressions.
_RE_ENUM_NAME = '^[a-z_]+$'


def validate(name, obj):
    """Validates an enumeration.

    :param str name: Enumeration name.
    :param dict obj: Enumeration definition.

    """
    errors = []

    # Validate name.
    if not re.match(_RE_ENUM_NAME, name):
        errors.append("name is invalid - must be lower_case_underscore")

    # Validate description.
    if "description" not in obj:
        errors.append("description is required")
    elif not isinstance(obj['description'], str):
        errors.append("description must be a string")

    # Validate members.
    if "members" not in obj:
        errors.append("members is required")
    elif not isinstance(obj['members'], list) or \
         not len(obj['members']) or \
         [m for m in obj['members'] if not isinstance(m, tuple) or len(m) != 2]:
        errors.append("members must defined as a list of tuples: (name, description)")
    else:
        for m_obj in obj['members']:
        	errors += validate_enum_member.validate(m_obj)

    return ["ENUMERATION[{}] :: {}".format(name, e) for e in errors]
