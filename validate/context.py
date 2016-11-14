# -*- coding: utf-8 -*-

"""
.. module:: context.py
   :platform: Unix, Windows
   :synopsis: Contextual information passed to a validator.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections

from validate_topic import validate as validate_topic
from validate_realm import validate as validate_realm



class ValidationContext(object):
    """Encapsulates validation processing information.

    """
    def __init__(self, realm, grid, key_properties, processes):
        """Instance constructor.

        """
        self.module = None
        self.errors = collections.defaultdict(list)
        self.warnings = collections.defaultdict(list)
        self.realm = realm
        self.realm_key = realm.__name__
        self.grid = grid
        self.key_properties = key_properties
        self.processes = processes


    @property
    def modules(self):
        """Gets set of specialization modules.

        """
        result = [self.realm, self.grid, self.key_properties] + self.processes

        return [m for m in result if m]


    def error(self, msg):
        """Adds an error to the managed collection.

        """
        self.errors[self.module].append(msg)


    def warn(self, msg):
        """Adds a warning to the managed collection.

        """
        self.warnings[self.module].append(msg)


    def validate(self):
        """Validates the specialization set.

        """
        validate_realm(self, self.realm)
        if self.grid:
            validate_topic(self, self.grid)
        if self.key_properties:
            validate_topic(self, self.key_properties)
        for process in self.processes:
            validate_topic(self, process)


    def get_errors(self):
        """Returns set of validation errors.

        """
        return {k: v for k, v in self.errors.items() if v}


    def get_warnings(self):
        """Returns set of validation warning.

        """
        return {k: v for k, v in self.warnings.items() if v}
