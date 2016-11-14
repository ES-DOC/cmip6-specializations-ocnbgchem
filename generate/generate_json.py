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
from utils_model import ProcessSpecialization
from utils_model import RealmSpecialization
from utils_parser import Parser



# Map of output types to keys.
_JSON_KEYS = {
    ProcessSpecialization: "process"
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


    def on_realm_parse(self, realm):
        """On realm parse event handler.

        """
        obj = self._map_module(realm)
        obj['processes'] = []


    def on_grid_parse(self, realm, grid):
        """On grid parse event handler.

        """
        obj = self._map_module(grid)

        self._maps[realm]['grid'] = obj


    def on_key_properties_parse(self, realm, key_properties):
        """On key_properties parse event handler.

        """
        obj = self._map_module(key_properties)

        self._maps[realm]['keyProperties'] = obj


    def on_process_parse(self, realm, process):
        """On process parse event handler.

        """
        obj = self._map_module(process)
        obj['subProcesses'] = []

        self._maps[realm]['processes'].append(obj)


    def on_subprocess_parse(self, process, subprocess):
        """On sub-process parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(subprocess.name)
        obj['description'] = subprocess.description
        obj['id'] = subprocess.id

        self._maps[process]['subProcesses'].append(obj)
        self._maps[subprocess] = obj


    def on_detail_set_parse(self, owner, detail_set):
        """On process detail set parse event handler.

        """
        if owner not in self._maps:
            return

        obj = collections.OrderedDict()
        obj['label'] = get_label(detail_set.name)
        obj['description'] = detail_set.description
        if detail_set.id is None:
            detail_set.id = "{}.{}".format(owner.id, detail_set.name)
        obj['id'] = detail_set.id
        obj['details'] = []

        owner = self._maps[owner]
        owner['detailSets'] = owner.get('detailSets', [])
        owner['detailSets'].append(obj)
        self._maps[detail_set] = obj


    def on_detail_parse(self, detail_set, detail):
        """On detail parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(detail.name)
        obj['description'] = detail.description
        obj['id'] = detail.id
        obj['uiOrdinal'] = len(self._maps[detail_set]['details']) + 1
        obj['cardinality'] = detail.cardinality
        obj['type'] = "enum" if detail.typeof.find("ENUM") >= 0 else detail.typeof
        if detail.enum:
            obj['enum'] = {
                'label': detail.enum.name,
                'description': detail.enum.description,
                'isOpen': True,
                'choices': []
            }

        self._maps[detail_set]['details'].append(obj)
        self._maps[detail] = obj


    def on_enum_item_parse(self, detail_set, detail, item):
        """On process detail property choice parse event handler.

        """
        if item.is_other:
            return

        obj = collections.OrderedDict()
        obj['label'] = item.value
        obj['description'] = item.description

        self._maps[detail]['enum']['choices'].append(obj)


    def get_output(self):
        """Returns generated output as a text blob.

        """
        return json.dumps(self._maps[self.realm], indent=4)


    def _map_module(self, mod):
        """Maps a specialization module to a dictionary.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(mod.name)
        obj['description'] = mod.description
        obj['id'] = mod.id
        obj['contact'] = mod.contact
        self._maps[mod] = obj

        return obj
