"""
.. module:: validate_topic.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a specialized CMIP6 scientific topic.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import constants
import re



# Regular expressions.
_RE_DETAIL_NAME = '^[a-z_]+$'
_RE_DETAILSET_NAME = '^[a-z_]+$'


def validate(topic, prop_sets):
    """Validates a set of CMIP6 scientific details.

    :param module topic: A specialization topic.
    :param module prop_sets: Topic property sets.

    """
    errors = []

    for name, defn in prop_sets.items():
        _validate_property_set(errors, topic.ENUMERATIONS.keys(), prop_sets, name, defn)

    return errors


def _validate_property_set(errors, enums, associated, name, defn):
    """Validates a single detail set specialization.

    """
    # Verify nesting level.
    if len(name.split(":")) > 2:
        errors.append("{} : property nesting level cannot be > 2".format(name))
        return

    # ... verify hierachical name is correct.
    is_top_level = name.startswith("toplevel")
    if not is_top_level:
        if ":" in name and not ":".join((name.split(":")[0:-1])) in associated:
            errors.append("{}: must be associated with a parent property set".format(name))
            return

    # description = mandatory string.
    if "description" not in defn:
        errors.append("{}: detail set must have a description".format(name))
    elif not isinstance(defn['description'], str):
        errors.append("{}: detail set description must be a string".format(name))

    # properties = collection.
    if "properties" in defn:
        if not isinstance(defn['properties'], list):
            errors.append("{}: properties must defined as a list".format(name))
        elif [p for p in defn['properties'] if not isinstance(p, tuple) or len(p) != 4]:
            errors.append("{}: all properties must be 4 member tuples".format(name))
        else:
            for prop in defn['properties']:
                errors += ["{}.{}".format(name, i) for i in _validate_property(prop, enums)]


def _validate_property(prop, enums):
    """Validates a single detail specialization.

    """
    errors = []

    # Unpack definition.
    name, type_, cardinality, description = prop

    # Validate name.
    if not isinstance(name, str):
        errors.append("name must be a string :: [{}]".format(name))
    elif len(name.strip()) == 0:
        errors.append("name must not be a zero length string")
    # TODO apply regex

    # Validate type.
    if not isinstance(type_, (str, unicode)):
        errors.append("type must be a string :: {}".format(type_))
    elif type_.startswith("ENUM:"):
        if type_[5:] not in enums:
            errors.append("type enum key is invalid :: {}".format(type_))
    elif type_ not in constants.TYPES:
        errors.append("type must be either simple or an enum :: {}".format(type_))

    # Validate cardinality.
    if cardinality not in constants.CARDINALITIES:
        errors.append("cardinality is invalid :: [{}]".format(cardinality))

    # Validate description.
    if not isinstance(description, str):
        errors.append("description must be a string :: [{}]".format(description))
    elif len(description.strip()) == 0:
        errors.append("description must not be a zero length string")
    # TODO apply regex

    return ["{} :: property {}".format(name, i) for i in errors]

