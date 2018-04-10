# -*- coding: utf-8 -*-

"""
.. module:: generator.py
   :platform: Unix, Windows
   :synopsis: Encodes a cmip6 specialization as JSON.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import json

from utils import get_label
from utils_constants import *
from utils_parser import SpecializationParser



class Generator(SpecializationParser):
    """Specialization to JSON generator.

    """
    def __init__(self, project, root, short_tables):
        """Instance constructor.

        """
        super(Generator, self).__init__(project, root, short_tables)

        self._maps = collections.OrderedDict()
        self.on_root_parse = self._on_topic_parse
        self.on_grid_parse = self._on_topic_parse
        self.on_keyprops_parse = self._on_topic_parse
        self.on_process_parse = self._on_topic_parse
        self.on_subprocess_parse = self._on_topic_parse


    def get_output(self):
        """Returns generated output as a text blob.

        """
        return json.dumps(self._maps[self.root], indent=4)


    def _on_topic_parse(self, topic):
        """On topic parse event handler.

        """
        self._map_topic(topic)


    def on_property_set_parse(self, prop_set):
        """On property set parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(prop_set.name)
        obj['description'] = prop_set.description
        obj['id'] = prop_set.id
        obj['properties'] = []
        obj['propertySets'] = []

        self._maps[prop_set] = obj


    def on_property_parse(self, prop):
        """On property parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(prop.name)
        obj['description'] = prop.description
        obj['id'] = prop.id
        obj['cardinality'] = prop.cardinality
        obj['type'] = "enum" if prop.enum else prop.typeof
        obj['is_cim_property'] = prop.was_injected

        self._maps[prop] = obj


    def on_enum_parse(self, enum):
        """On enum parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(enum.name)
        obj['description'] = enum.description
        obj['isOpen'] = enum.is_open
        obj['choices'] = []

        self._maps[enum] = obj


    def on_enum_choice_parse(self, choice):
        """On process detail property enum choice parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = choice.value
        obj['description'] = choice.description

        self._maps[choice] = obj


    def on_root_parsed(self, root):
        """On root parsed event handler.

        """
        obj = self._maps[root]
        if root[TYPE_KEY_GRID] is not None:
            obj['grid'] = self._maps[root[TYPE_KEY_GRID]]
        if root[TYPE_KEY_KEYPROPS] is not None:
            obj['keyProperties'] = self._maps[root[TYPE_KEY_KEYPROPS]]
        obj['processes'] = [self._maps[i] for i in root[TYPE_KEY_PROCESS]]
        self._strip(obj)


    def on_grid_parsed(self, grid):
        """On grid parsed event handler.

        """
        self._strip(self._maps[grid])


    def on_keyprops_parsed(self, key_props):
        """keyprops parsed event handler.

        """
        self._strip(self._maps[key_props])


    def on_process_parsed(self, process):
        """On process parse event handler.

        """
        obj = self._maps[process]
        self._strip(obj)

        owner = self._maps[self.root]
        owner['processes'] = owner.get('processes', [])
        owner['processes'].append(obj)


    def on_subprocess_parsed(self, subprocess):
        """On sub-process parsed event handler.

        """
        obj = self._maps[subprocess]
        self._strip(obj)

        owner = self._maps[subprocess.parent]
        owner['subProcesses'] = owner.get('subProcesses', [])
        owner['subProcesses'].append(obj)


    def on_property_set_parsed(self, prop_set):
        """On property set parsed event handler.

        """
        obj = self._maps[prop_set]
        self._strip(obj)

        owner = self._maps[prop_set.owner]
        owner['propertySets'] = owner.get('propertySets', [])
        owner['propertySets'].append(obj)


    def on_property_parsed(self, prop):
        """On property parsed event handler.

        """
        owner = self._maps[prop.owner]
        owner['properties'] = owner.get('properties', [])
        owner['properties'].append(self._maps[prop])
        self._maps[prop]['uiOrdinal'] = len(owner['properties'])


    def on_enum_parsed(self, enum):
        """On enum parsed event handler.

        """
        detail = self._maps[enum.detail]
        detail['enum'] = self._maps[enum]


    def on_enum_choice_parsed(self, choice):
        """On process detail property enum choice parse event handler.

        """
        enum = self._maps[choice.enum]
        enum['choices'].append(self._maps[choice])


    def _map_topic(self, topic):
        """Maps a specialization topic to a dictionary.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(topic.name)
        obj['description'] = topic.description
        obj['id'] = topic.id
        obj['contact'] = topic.contact
        obj['properties'] = []
        obj['propertySets'] = []
        self._maps[topic] = obj

        return obj


    def _strip(self, obj):
        """Strips null keys from mapped objects.

        """
        if not obj['properties']:
            del obj['properties']
        if not obj['propertySets']:
            del obj['propertySets']
