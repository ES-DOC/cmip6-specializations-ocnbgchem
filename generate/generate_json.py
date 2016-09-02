# -*- coding: utf-8 -*-

"""
.. module:: generator.py
   :platform: Unix, Windows
   :synopsis: Rewrites a cmip6 realm specialization to json.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import json


from utils import get_label
from utils_model import Grid
from utils_model import GridDiscretisation
from utils_model import KeyProperties
from utils_model import Process
from utils_model import Realm
from utils_parser import Parser



# Map of output types to keys.
_JSON_KEYS = {
    Grid: "grid",
    KeyProperties: "keyProperties",
    Process: "process"
}

# Type that are to be emitted as JSON.
_JSON_TYPES = tuple(_JSON_KEYS.keys())



class Generator(Parser):
    """Specialization to mindmap generator.

    """
    def __init__(self, realm):
        """Instance constructor.

        """
        super(Generator, self).__init__(realm)

        self._maps = collections.OrderedDict()


    def get_output(self):
        """Returns generated output as a text blob.

        """
        # Set realm map.
        obj = self._maps[self.realm]

        # Append process, grid, key properties maps.
        for mod, mod_obj in self._maps.items():
            if isinstance(mod, _JSON_TYPES):
                if isinstance(mod, Process):
                    obj['processes'].append(mod_obj)
                else:
                    obj[_JSON_KEYS[type(mod)]] = mod_obj

        return json.dumps(obj, indent=4)


    def on_realm_parse(self, realm):
        """On realm parse event handler.

        """
        obj = self._map_module(realm)
        obj['processes'] = []

        self._maps[realm] = obj


    def on_grid_parse(self, realm, grid):
        """On grid parse event handler.

        """
        obj = self._map_module(grid)

        self._maps[grid] = obj


    def on_grid_discretisation_parse(self, realm, grid, discretisation):
        """On grid discretisation parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = "Discretisation"
        obj['description'] = discretisation.description
        obj['id'] = discretisation.id

        self._maps[discretisation] = obj
        self._maps[grid]['discretisation'] = obj


    def on_key_properties_parse(self, realm, key_properties):
        """On key_properties parse event handler.

        """
        obj = self._map_module(key_properties)

        self._maps[key_properties] = obj


    def on_key_properties_conservation_parse(self, realm, grid, conservation):
        """On key-properties conservation parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = "Conservation"
        obj['description'] = conservation.description

        self._maps[conservation] = obj
        self._maps[grid]['conservation'] = obj


    def on_process_parse(self, realm, process):
        """On process parse event handler.

        """
        obj = self._map_module(process)
        obj['subProcesses'] = []

        self._maps[process] = obj


    def on_subprocess_parse(self, process, subprocess):
        """On sub-process parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(subprocess.name)
        obj['description'] = subprocess.description
        obj['id'] = subprocess.id
        self._maps[process]['subProcesses'].append(obj)

        self._maps[subprocess] = obj


    def on_detail_parse(self, owner, detail):
        """On process detail parse event handler.

        """
        if owner not in self._maps:
            return

        obj = collections.OrderedDict()
        obj['label'] = get_label(detail.name)
        obj['description'] = detail.description
        if detail.id is None:
            detail.id = "{}.{}".format(owner.id, detail.name)
        obj['id'] = detail.id
        obj['properties'] = []

        owner = self._maps[owner]
        owner['details'] = owner.get('details', [])
        owner['details'].append(obj)

        self._maps[detail] = obj


    def on_detail_property_parse(self, detail, prop):
        """On detail property parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(prop.name)
        obj['description'] = prop.description
        obj['id'] = prop.id
        obj['uiOrdinal'] = len(self._maps[detail]['properties']) + 1
        obj['cardinality'] = prop.cardinality
        obj['type'] = "enum" if prop.typeof.find("ENUM") >= 0 else prop.typeof
        if prop.enum:
            obj['enum'] = {
                'label': prop.enum.name,
                'id': prop.enum.id,
                'description': prop.enum.description,
                'isOpen': True,
                'choices': []
            }

        self._maps[detail]['properties'].append(obj)
        self._maps[prop] = obj


    def on_detail_property_choice_parse(self, detail, prop, choice):
        """On process detail property choice parse event handler.

        """
        if choice.is_other:
            return

        obj = collections.OrderedDict()
        obj['label'] = choice.value
        obj['description'] = choice.description

        self._maps[prop]['enum']['choices'].append(obj)


    def _map_module(self, mod):
        """Maps a specialization module to a dictionary.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(mod.name)
        obj['description'] = mod.description
        obj['id'] = mod.id
        obj['contact'] = mod.contact

        return obj
