"""
.. module:: __main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import os

from generate_mm import Generator as MindmapGenerator
from generate_json import Generator as JsonGenerator
from generate_ids_level_1 import Generator as Level1IdentifierGenerator
from generate_ids_level_2 import Generator as Level2IdentifierGenerator
from generate_ids_level_3 import Generator as Level3IdentifierGenerator
from utils_loader import get_realm_specializations
from utils_factory import create_realm_specialization



# Map of generator types to generator.
_GENERATORS = {
    'mm': MindmapGenerator,
    'json': JsonGenerator,
    'ids-level-1': Level1IdentifierGenerator,
    'ids-level-2': Level2IdentifierGenerator,
    'ids-level-3': Level3IdentifierGenerator
}

# Map of generator types to encoding type.
_ENCODINGS = {
    'ids-level-1': 'csv',
    'ids-level-2': 'csv',
    'ids-level-3': 'csv'
}

# Map of generator types to file suffixes.
_FILE_SUFFIXES = {
    'ids-level-1': 'ids-level-1',
    'ids-level-2': 'ids-level-2',
    'ids-level-3': 'ids-level-3'
}

# Set directory from which module is being run.
_DIR = os.path.dirname(__file__)

# Set command line arguments.
_ARGS = argparse.ArgumentParser("Encodes CMIP6 realm specializations.")
_ARGS.add_argument(
    "--type",
    help="Type of generator to be executed.",
    dest="typeof",
    type=str,
    default="all"
    )
_ARGS.add_argument(
    "-o", "--output-dir",
    help="Path to a directory into which generated content will be written.",
    dest="output_dir",
    type=str,
    default=os.path.dirname(_DIR)
    )
_ARGS.add_argument(
    "--realm",
    help="Name of realm being processed.",
    dest="realm",
    type=str,
    default=os.path.dirname(_DIR).split("-")[-1]
    )
_ARGS.add_argument(
    "--input",
    help="Path to a directory in which realm specializations reside.",
    dest="input_dir",
    type=str,
    default=os.path.dirname(_DIR)
    )
_ARGS = _ARGS.parse_args()

# Validate inputs.
if _ARGS.typeof != 'all' and _ARGS.typeof not in _GENERATORS.keys():
    err = "Unknown generator type [{}].  Validate types = {}."
    err = err.format(_ARGS.typeof, " | ".join(sorted(_GENERATORS.keys())))
    raise ValueError(err)

# Set target generators to be executed.
if _ARGS.typeof == 'all':
    targets = _GENERATORS
else:
    targets = {
        _ARGS.typeof: _GENERATORS[_ARGS.typeof]
    }

logging_output = []
for generator_type, generator_cls in targets.iteritems():
    # Set output encoding.
    try:
        encoding = _ENCODINGS[generator_type]
    except KeyError:
        encoding = generator_type

    # Set output filename.
    try:
        fname = "{}-{}".format(_ARGS.realm, _FILE_SUFFIXES[generator_type])
    except KeyError:
        fname = _ARGS.realm
    finally:
        if encoding == 'py':
            fname = fname.replace("-", "_")

    # Set realm.
    realm = create_realm_specialization(
        get_realm_specializations(_ARGS.input_dir, _ARGS.realm)
        )

    # Run generator.
    generator = generator_cls(realm)
    generator.run()

    # Write generated output to file system.
    fpath = os.path.join(_ARGS.output_dir, "_{}.{}".format(fname, encoding))
    with open(fpath, 'w') as fstream:
        fstream.write(generator.get_output())

    logging_output.append((encoding, fpath))

# Inform user.
for encoding, fpath in sorted(logging_output):
    print "ES-DOC :: generated {} file written to --> {}".format(encoding, fpath)
