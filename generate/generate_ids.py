# -*- coding: utf-8 -*-

"""
.. module:: generate_ids_level_1.py
   :platform: Unix, Windows
   :synopsis: Generates level 1 identifiers.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from utils import get_label
from utils_parser import Parser



class Generator(Parser):
    """Specialization to mindmap generator.

    """
    def __init__(self, realm):
        """Instance constructor.

        """
        super(Generator, self).__init__(realm)

        self._ids = [("cmip6-id", "cmip6-label", "cmip6-type", "")]


    def get_output(self):
        """Returns generated output as a text blob.

        """
        return "\n".join(self._get_output())


    def _get_output(self):
        """Returns formatted identifier collection.

        """
        return ["{}, {}, {}".format(i, j, k)
                for i, j, k, _ in self._ids]
        return ["{}, {}, {}".format(i, j, k)
                for i, j, k, _ in sorted(self._ids, key=lambda i: i[-1])]


    def emit_null_row(self, owner):
        """Emits a null row.

        """
        if len(self._ids[-1][0]):
            self._ids.append(("", "", "", owner.id))


    def set_id(self, owner, identifier=None):
        """Appends an identifier to managed collection.

        """
        try:
            identifier = identifier or owner.id
        except AttributeError:
            pass
        finally:
            if not identifier:
                print "Invalid identifier: ", type(owner), owner.name, identifier
                return

        # Derive label.
        label = " > ".join([get_label(i) for i in identifier.split(".")[1:]])

        # Append to managed collection.
        self._ids.append((identifier, label, owner.cfg_section, identifier))

