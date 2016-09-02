# -*- coding: utf-8 -*-

"""
.. module:: generate_ids_level_1.py
   :platform: Unix, Windows
   :synopsis: Generates level 1 identifiers.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from utils import get_label
from utils_model import Detail
from utils_model import DetailProperty
from utils_model import Enum
from utils_model import EnumChoice
from utils_model import Grid
from utils_model import GridDiscretisation
from utils_model import KeyProperties
from utils_model import KeyPropertiesConservation
from utils_model import KeyPropertiesExtent
from utils_model import KeyPropertiesResolution
from utils_model import KeyPropertiesTuning
from utils_model import Process
from utils_model import Realm
from utils_model import SubProcess
from utils_parser import Parser



# Map of specialization types to identifier types.
_ID_TYPES = {
    Detail: "detail",
    DetailProperty: "detail-property",
    Enum: "enum",
    EnumChoice: "enum-choice",
    Grid: "grid",
    GridDiscretisation: "grid-discretisation",
    KeyProperties: "key-properties",
    KeyPropertiesConservation: "key-properties-conservation",
    KeyPropertiesExtent: "key-properties-extent",
    KeyPropertiesResolution: "key-properties-resolution",
    KeyPropertiesTuning: "key-properties-tuning",
    Process: "process",
    Realm: "realm",
    SubProcess: "sub-process"
}


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
        self._ids.append((identifier, label, _ID_TYPES[type(owner)], identifier))

