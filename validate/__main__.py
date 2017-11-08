"""
.. module:: __main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import datetime
import glob
import operator
import os

import utils
import validate_root
import validate_short_table
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

# Name of associated project.
_PROJECT = __file__.split('/')[-3].split('-')[0]

# Report section break.
_REPORT_BREAK = "------------------------------------------------------------------------"


def _validate_definitions():
    """Validates py definitions.

    """
    # Set specialization modules.
    modules = utils.get_modules(_ARGS.input_dir, _ARGS.typeof)

    # Set validation context.
    ctx = utils.DefinitionsValidationContext(modules)

    # Validate.
    validate_root.validate(ctx)
    for module in [i for i in ctx.modules if i != ctx.root]:
        validate_topic.validate(ctx, module)

    # Set errors.
    errors = ctx.get_errors()

    # Set report.
    report = []
    if not errors:
        report.append(_REPORT_BREAK)
        report.append("{} {} specializations are valid.".format(_PROJECT.upper(), _ARGS.typeof))
        report.append(_REPORT_BREAK)
    else:
        error_count = len(reduce(operator.add, errors.values()))
        report.append(_REPORT_BREAK)
        report.append("CMIP6 SPECIALIZATIONS VALIDATION REPORT")
        report.append(_REPORT_BREAK)
        report.append("Specialization Type = {}".format(_ARGS.typeof))
        report.append("Generated @ {}".format(datetime.datetime.now()))
        report.append("Error count = {}".format(error_count))
        report.append(_REPORT_BREAK)

        # Set report errors.
        for module, errors in sorted(errors.items()):
            report.append("{}.py".format(module.__name__))
            for idx, err in enumerate(errors):
                report.append("Error #{}:\t{}.".format(idx + 1, err))
            report.append("")

    # Write to stdout.
    for l in report:
        print "ES-DOC :: {}".format(l)

    return len(errors) == 0


def _validate_short_tables():
    """Validates short tables definitions.

    """
    # Set files to be validated.
    dpath = os.path.join(_ARGS.input_dir, 'short_tables')
    if not os.path.exists(dpath):
        return


    # Validate files.
    errors = {i: validate_short_table.validate(i) \
              for i in glob.glob("{}/*.json".format(dpath))}

    # Report errors.
    report = []
    for fpath, ferrors in errors.items():
        fname = fpath.split('/')[-1]
        if ferrors:
            report.append(_REPORT_BREAK)
            report.append("Invalid {} {} short-table: {}".format(_PROJECT.upper(), _ARGS.typeof, fname))
            for error in ferrors:
                report.append("\t{}".format(error))
            report.append(_REPORT_BREAK)

    if not report:
        report.append(_REPORT_BREAK)
        report.append("{} {} short-tables are valid.".format(_PROJECT.upper(), _ARGS.typeof))
        report.append(_REPORT_BREAK)

    # Write to stdout.
    for l in report:
        print "ES-DOC :: {}".format(l)


if _validate_definitions():
    _validate_short_tables()
