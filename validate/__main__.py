"""
.. module:: __main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import datetime
import operator
import os

from context import ValidationContext
import utils_loader


# Define command line options.
_ARGS = argparse.ArgumentParser("Validates a set of CMIP6 specializations.")
_ARGS.add_argument(
    "--realm",
    help="Name of realm being validated.",
    dest="realm",
    type=str,
    default=os.path.dirname(os.path.dirname(__file__)).split("/")[-1][22:]
    )
_ARGS.add_argument(
    "--input",
    help="Path to a directory in which specializations reside.",
    dest="input_dir",
    type=str,
    default=os.path.dirname(os.path.dirname(__file__))
    )
_ARGS = _ARGS.parse_args()

# Report section break.
_REPORT_BREAK = "------------------------------------------------------------------------"

# Set specializations.
realm, grid, key_properties, processes = \
    utils_loader.get_specializations(_ARGS.input_dir, _ARGS.realm)

# Validate.
validator = ValidationContext(realm, grid, key_properties, processes)
validator.validate()

# Set errors.
in_error = validator.get_errors()
error_count = 0 if not in_error else len(reduce(operator.add, in_error.values()))

# Set report.
report = []
if not in_error:
    report.append(_REPORT_BREAK)
    report.append("The CMIP6 {} specializations are currently valid. Congratulations!".format(_ARGS.realm))
    report.append(_REPORT_BREAK)
else:
    report.append(_REPORT_BREAK)
    report.append("CMIP6 SPECIALIZATIONS VALIDATION REPORT")
    report.append(_REPORT_BREAK)
    report.append("Realm = {}".format(_ARGS.realm))
    report.append("Generated @ {}".format(datetime.datetime.now()))
    report.append("Error count = {}".format(error_count))
    report.append(_REPORT_BREAK)

    # Set report errors.
    for module, errors in sorted(in_error.items()):
        report.append("{}.py".format(module.__name__))
        for idx, err in enumerate(errors):
            report.append("Error #{}:\t{}.".format(idx + 1, err))
        report.append("")

# Write to stdout.
for l in report:
    print l
