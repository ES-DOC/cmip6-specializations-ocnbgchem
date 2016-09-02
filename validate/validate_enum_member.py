"""
.. module:: enum_member_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 enumeration member specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import re



# Regular expressions.
_RE_ENUM_MEMBER_NAME = '^[a-zA-Z0-9-_ ()/\*\.\:+]+$'


def validate(defn):
    """Validates an enum member.

    :param tuple defn: Enum member definition.

    """
    errors = []

    # Name is mandatory.
    name = defn[0]
    if name is None:
        errors.append("name is invalid")

    # Name is mandatory.
    if not re.match(_RE_ENUM_MEMBER_NAME, name):
        err = 'Invalid enum member: {} --> name contain invalid characters'
        err = err.format(name)
        errors.append(err)

    # Description is mandatory.
    description = defn[1]
    if description is None:
        pass
        # errors.append("member description is missing :: member-name={}".format(name))

    return errors
