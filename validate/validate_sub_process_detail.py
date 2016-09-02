"""
.. module:: sub_process_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 scientific sub-process specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import validate_property



def validate(process, key, defn):
    """Validates a scientific sub-process specialization.

    :param str key: Sub-process detail key.
    :param module defn: Sub-process detail definition.
    :param list enums: Set of allowed enumerations.

    """
    errors = []

    # Validate key.
    if len(key.split(":")) != 2:
        errors.append("key is invalid (format is not 'sub-process:name')")
    else:
        sub_process_key, key_ = key.split(":")
        if sub_process_key not in process.SUB_PROCESSES:
            errors.append("key is invalid (does not map to a sub-process)")
        elif key_ not in process.SUB_PROCESSES[sub_process_key]['details']:
            errors.append("key is invalid (does not map to a sub-process detail)")

    # Validate description.
    if "description" not in defn:
        errors.append("has no description")
    elif not isinstance(defn['description'], str):
        errors.append("description must be a string")

    # Validate properties.
    if "properties" not in defn:
        errors.append("has no properties")
    elif not isinstance(defn['properties'], list):
        errors.append("properties must be a list")
    elif [p for p in defn['properties'] if not isinstance(p, tuple) or len(p) != 4]:
        errors.append("properties must be 4 member tuples")
    else:
        for defn_ in defn['properties']:
            errors += validate_property.validate(defn_, process.ENUMERATIONS)

    return errors
