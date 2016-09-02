"""
.. module:: details_container_validator.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a CMIP6 discretisation specialization.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
def validate(key, defn, details_collection):
    """Validates a set of details pertaining to a details specialization container.

    :param str key: Specialization detail key.
    :param dict defn: Specialization detail definition.
    :param list defn: Associated specialization detail collection.

    """
    errors = []

    # Validate description.
    if "description" not in defn:
        errors.append("has no description")
    elif not isinstance(defn["description"], str):
        errors.append("description must be a string")

    # Validate details.
    if "details" not in defn:
        errors.append("has no details")
    elif not isinstance(defn["details"], list):
        errors.append("details must be a list")
    elif [i for i in defn["details"] if not isinstance(i, str)]:
        errors.append("details contains invalid key(s)")

    if not errors:
        for key in [k for k in defn['details'] if not k in details_collection]:
            err = "has an invalid detail key: {}".format(key)
            errors.append(err)

    return errors
