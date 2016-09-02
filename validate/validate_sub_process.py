"""
.. module:: sub_process_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 scientific sub-process specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
def validate(key, defn):
    """Validates a scientific sub-process specialization.

    :param str key: Sub-process key.
    :param dict defn: Sub-process definition.

    """
    errors = []

    # Validate description.
    if "description" not in defn:
        errors.append("description is missing")
    elif not isinstance(defn["description"], str):
        errors.append("description must be a string")

    # Validate details.
    if "details" not in defn:
        errors.append("details are missing")
    elif not isinstance(defn["details"], list):
        errors.append("details must be a list")
    elif [i for i in defn["details"] if not isinstance(i, str)]:
        errors.append("details contains invalid key(s)")

    return errors
