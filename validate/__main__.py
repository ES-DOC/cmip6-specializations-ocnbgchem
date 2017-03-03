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

import utils
import validate_root
import validate_topic


# Define command line options.
_ARGS = argparse.ArgumentParser("Validates a set of CMIP6 specializations.")
_ARGS.add_argument(
    "--typeof",
    help="Type of specializations being validated.",
    dest="typeof",
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

# Map of specialization types to filename overrides.
_FILENAME_OVERRIDES = {
    "toplevel": "model",
    "ocean-bgc": "oceanbgc"
}

# Set specialization filename prefix.
try:
    _FILENAME = _FILENAME_OVERRIDES[_ARGS.typeof]
except KeyError:
    _FILENAME = _ARGS.typeof

# Set specialization modules.
modules = utils.get_modules(_ARGS.input_dir, _FILENAME)

# Set validation context.
ctx = utils.ValidationContext(modules)

# Validate.
validate_root.validate(ctx)
for module in [i for i in ctx.modules if i != ctx.root]:
    validate_topic.validate(ctx, module)

# Set errors.
in_error = ctx.get_errors()

# Set report.
report = []
if not in_error:
    report.append(_REPORT_BREAK)
    report.append("The CMIP6 {} specializations are currently valid. Congratulations!".format(_ARGS.typeof))
    report.append(_REPORT_BREAK)
else:
    error_count = len(reduce(operator.add, in_error.values()))
    report.append(_REPORT_BREAK)
    report.append("CMIP6 SPECIALIZATIONS VALIDATION REPORT")
    report.append(_REPORT_BREAK)
    report.append("Specialization Type = {}".format(_ARGS.typeof))
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
