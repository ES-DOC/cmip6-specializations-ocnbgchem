"""
.. module:: utils.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: CMIP6 specialization validation utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import imp
import os



def validate_field(ctx, module, name, typeof):
    """Validates a field defined within a root specialization.

    """
    if not hasattr(module, name):
        ctx.error("{} is missing".format(name))
    elif not isinstance(getattr(module, name), typeof):
        ctx.error("{} type is invalid (must be a {})".format(name, typeof))
    else:
        return True


def get_modules(input_dir, typeof):
    """Returns specialization modules.

    :param str input_dir: Directory within which modules reside.
    :param str typeof: Type of specialization being processed.

    """
    # Load specialization modules.
    modules = _get_modules(input_dir, typeof)
    if not modules:
        raise KeyError("Specializations not found")

    # Set specializations.
    root = _get_module(modules, typeof)
    try:
        root.GRID
    except AttributeError:
        grid = None
    else:
        grid = _get_module(modules, root.GRID)
    key_properties = _get_module(modules, root.KEY_PROPERTIES)
    processes = [_get_module(modules, p) for p in root.PROCESSES]

    return root, grid, key_properties, processes


def _get_modules(input_dir, specialization_type):
    """Returns a set of specialization modules.

    """
    modules = sorted([i for i in os.listdir(input_dir) if _is_target(i, specialization_type)])
    modules = [os.path.join(input_dir, m) for m in modules]
    modules = [(m.split("/")[-1].split(".")[0], m) for m in modules]

    return [imp.load_source(name, fpath) for name, fpath in modules]


def _get_module(modules, name):
    """Returns a specialization module.

    """
    for module in modules:
        if module.__name__ == name:
            return module


def _is_target(filename, specialization_type):
    """Returns flag indicating whether a module is a specialization target or not.

    """
    return not filename.startswith('_') and \
           filename.endswith('.py') and \
           filename.startswith(specialization_type)


class ValidationContext(object):
    """Validation context information.

    """
    def __init__(self, specializations):
        """Instance constructor.

        """
        self.module = None
        self.errors = collections.defaultdict(list)
        self.warnings = collections.defaultdict(list)

        root, grid, key_properties, processes = specializations
        self.root = root
        self.grid = grid
        self.key_properties = key_properties
        self.processes = processes


    @property
    def modules(self):
        """Gets set of specialization modules.

        """
        result = [self.root, self.grid, self.key_properties] + self.processes

        return [m for m in result if m is not None]


    def has_module(self, key):
        """Returns flag indicating whether a module key can be mapped.

        """
        return key in [i.__name__ for i in self.modules]


    def error(self, msg):
        """Adds an error to the managed collection.

        """
        self.errors[self.module].append(msg)


    def warn(self, msg):
        """Adds a warning to the managed collection.

        """
        self.warnings[self.module].append(msg)


    def get_errors(self):
        """Returns set of validation errors.

        """
        return {k: v for k, v in self.errors.items() if v}


    def get_warnings(self):
        """Returns set of validation warning.

        """
        return {k: v for k, v in self.warnings.items() if v}
