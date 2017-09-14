"""
.. module:: validate_short_tables.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates short tables.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import json
import os


def validate(fpath):
    """Validates a short table.

    :param str fpath: File path of short table.

    :returns: List of errors.
    :rtype: list

    """
    try:
        _validate_fpath(fpath)
    except AssertionError as err:
        return [err]

    try:
        obj = _validate_json(fpath)
    except AssertionError as err:
        return [err]

    return _validate_dict(obj)


def _validate_fpath(fpath):
    """Validates file path exists.

    """
    assert os.path.isfile(fpath), "Unknown file"


def _validate_json(fpath):
    """Validates JSON can be decoded.

    """
    try:
        with open(fpath, 'r') as fstream:
            return json.loads(fstream.read())
    except:
        raise AssertionError("Malformed JSON")


def _validate_dict(obj):
    """Validates JSON content.

    """
    errors = []

    # Validate AUTHORS.
    if "AUTHORS" not in obj:
        errors.append("AUTHORS is required")
    elif not isinstance(obj['AUTHORS'], list):
        errors.append("AUTHORS must be a list")

    # Validate CHANGE_HISTORY.
    if "CHANGE_HISTORY" not in obj:
        errors.append("CHANGE_HISTORY is required")
    elif not isinstance(obj['CHANGE_HISTORY'], list):
        errors.append("CHANGE_HISTORY must be a list")
    else:
        for defn in obj['CHANGE_HISTORY']:
            if not isinstance(defn, list) or not len(defn) == 4:
                errors.append("Change histories must be defined as 4 member lists")
                break

    # Validate CONTACT.
    if "CONTACT" not in obj:
        errors.append("CONTACT is required")
    elif not isinstance(obj['CONTACT'], (str, basestring)):
        errors.append("CONTACT must be a string")

    # Validate CONTRIBUTORS.
    if "CONTRIBUTORS" not in obj:
        errors.append("CONTRIBUTORS is required")
    elif not isinstance(obj['CONTRIBUTORS'], list):
        errors.append("CONTRIBUTORS must be a list")

    # Validate LABEL.
    if "LABEL" not in obj:
        errors.append("LABEL is required")
    elif not isinstance(obj['LABEL'], (str, basestring)):
        errors.append("LABEL must be a string")

    # Validate PROPERTIES.
    if "PROPERTIES" not in obj:
        errors.append("PROPERTIES is required")
    elif not isinstance(obj['PROPERTIES'], list):
        errors.append("PROPERTIES must be a list")
    else:
        for defn in obj['PROPERTIES']:
            if not isinstance(defn, list) or not len(defn) == 2:
                errors.append("All properties must be 2 member lists")
                break
            else:
                if not isinstance(defn[0], (str, basestring)):
                    errors.append("Property names must be strings")
                    break
                if not isinstance(defn[1], int) or defn[1] <= 0:
                    errors.append("Property priorities must be integers > 0")
                    break

    # Validate LABEL.
    if "QC_STATUS" not in obj:
        errors.append("QC_STATUS is required")
    elif not isinstance(obj['QC_STATUS'], (str, basestring)):
        errors.append("QC_STATUS must be a string")

    return errors
