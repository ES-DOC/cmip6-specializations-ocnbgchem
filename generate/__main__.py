"""
.. module:: __main__.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import argparse
import os

from generate_js import Generator as JavascriptGenerator
from generate_json import Generator as JSONGenerator
from generate_mm import Generator as MindmapGenerator
from generate_ids_level_1 import Generator as Level1IdentifierGenerator
from generate_ids_level_2 import Generator as Level2IdentifierGenerator
from generate_ids_level_3 import Generator as Level3IdentifierGenerator
from utils_factory import get_specialization
from utils_factory import get_short_tables
from utils_loader import get_modules
from utils_loader import get_short_tables_definitions



# Name of associated project.
_PROJECT = __file__.split('/')[-3].split('specializations')[0][0:-1]

# Map of generator types to generator.
_GENERATORS = {
    'js': JavascriptGenerator,
    'json': JSONGenerator,
    'mm': MindmapGenerator,
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

# Map of generator types to file prefixes.
_FILE_PREFIXES = {
    'js': '_',
    'json': '_',
    'mm': '_',
    'ids-level-1': '_',
    'ids-level-2': '_',
    'ids-level-3': '_'
}

# Map of generator types to file suffixes.
_FILE_SUFFIXES = {
    'ids-level-1': '-ids-level-1',
    'ids-level-2': '-ids-level-2',
    'ids-level-3': '-ids-level-3'
}

# Map of generator types to directories.
_DIRECTORIES = {
    'js': '',
    'json': '',
    'mm': '',
    'ids-level-1': '',
    'ids-level-2': '',
    'ids-level-3': ''
}

# Set directory from which module is being run.
_DIR = os.path.dirname(__file__)

# Set command line arguments.
_ARGS = argparse.ArgumentParser("Encodes a CMIP6 specialization.")
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
    "--scope",
    help="Name of specialization scope being processed.",
    dest="scope",
    type=str,
    default=os.path.dirname(os.path.dirname(__file__)).split("/")[-1][22:]
    )
_ARGS.add_argument(
    "--input",
    help="Path to a directory in which specializations reside.",
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

# Set specialization filename prefix.
_FILENAME = _ARGS.scope

# Set target generators to be executed.
if _ARGS.typeof == 'all':
    targets = _GENERATORS
else:
    targets = {
        _ARGS.typeof: _GENERATORS[_ARGS.typeof]
    }

# Set specialization modules.
specialization = get_specialization(get_modules(_ARGS.input_dir, _FILENAME))

# Set specialization short tables.
short_tables = get_short_tables(get_short_tables_definitions(_ARGS.input_dir, _FILENAME))

logging_output = []
for generator_type, generator_cls in targets.iteritems():
    # Run generator
    generator = generator_cls(_PROJECT, specialization, short_tables)
    generator.run()

    # Set output file name.
    fname = "{}{}{}.{}".format(
        _FILE_PREFIXES.get(generator_type, ''),
        _FILENAME,
        _FILE_SUFFIXES.get(generator_type, ''),
        _ENCODINGS.get(generator_type, generator_type)
        )
    if fname.endswith('.py'):
        fname = fname.replace("-", "_")

    # Set output file path.
    fpath = _ARGS.output_dir
    dpath = _DIRECTORIES.get(generator_type, '')
    for part in dpath.split('/'):
        fpath = os.path.join(fpath, part)
    fpath = os.path.join(fpath, fname)

    # Write generated output to file system.
    with open(fpath, 'w') as fstream:
        fstream.write(generator.get_output())

    logging_output.append((fname.split('.')[-1], fpath))


# Inform user.
for encoding, fpath in sorted(logging_output):
    print "ES-DOC :: generated {} file written to --> {}".format(encoding, fpath)
