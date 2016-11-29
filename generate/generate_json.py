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
from utils_parser import Parser



class Generator(Parser):
    """Specialization to mindmap generator.

    """
    def __init__(self, realm):
        """Instance constructor.

        """
        super(Generator, self).__init__(realm)

        self._maps = collections.OrderedDict()
        self.on_realm_parse = self._on_topic_parse
        self.on_grid_parse = self._on_topic_parse
        self.on_keyproperties_parse = self._on_topic_parse
        self.on_process_parse = self._on_topic_parse
        self.on_subprocess_parse = self._on_topic_parse


    def get_output(self):
        """Returns generated output as a text blob.

        """
        return json.dumps(self._maps[self.realm], indent=4)


    def _on_topic_parse(self, topic):
        """On topic parse event handler.

        """
        self._map_topic(topic)


    def on_detailset_parse(self, detailset):
        """On process detail set parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(detailset.name)
        obj['description'] = detailset.description
        obj['id'] = detailset.id
        obj['details'] = []
        obj['detailSets'] = []

        self._maps[detailset] = obj


    def on_detail_parse(self, detail):
        """On detail parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(detail.name)
        obj['description'] = detail.description
        obj['id'] = detail.id
        obj['cardinality'] = detail.cardinality
        obj['type'] = "enum" if detail.enum else detail.typeof

        self._maps[detail] = obj


    def on_enum_parse(self, enum):
        """On enum parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(enum.name)
        obj['description'] = enum.description
        obj['isOpen'] = enum.is_open
        obj['choices'] = []

        self._maps[enum] = obj


    def on_enumchoice_parse(self, choice):
        """On process detail property enum choice parse event handler.

        """
        if choice.is_other:
            return

        obj = collections.OrderedDict()
        obj['label'] = choice.value
        obj['description'] = choice.description

        self._maps[choice] = obj


    def on_realm_parsed(self, realm):
        """On realm parsed event handler.

        """
        obj = self._maps[realm]
        obj['grid'] = self._maps[realm.grid]
        obj['keyProperties'] = self._maps[realm.key_properties]
        obj['processes'] = [self._maps[i] for i in realm.processes]
        self._strip(obj)


    def on_grid_parsed(self, grid):
        """On grid parsed event handler.

        """
        self._strip(self._maps[grid])


    def on_keyproperties_parsed(self, keyproperties):
        """On key properties parsed event handler.

        """
        self._strip(self._maps[keyproperties])


    def on_process_parsed(self, process):
        """On process parse event handler.

        """
        obj = self._maps[process]
        self._strip(obj)

        realm = self._maps[self.realm]
        realm['processes'] = realm.get('processes', [])
        realm['processes'].append(obj)


    def on_subprocess_parsed(self, subprocess):
        """On sub-process parsed event handler.

        """
        obj = self._maps[subprocess]
        self._strip(obj)

        process = self._maps[subprocess.parent]
        process['subProcesses'] = process.get('subProcesses', [])
        process['subProcesses'].append(obj)


    def on_detailset_parsed(self, detailset):
        """On process detail set parse event handler.

        """
        obj = self._maps[detailset]
        self._strip(obj)

        owner = self._maps[detailset.owner]
        owner['detailSets'] = owner.get('detailSets', [])
        owner['detailSets'].append(obj)


    def on_detail_parsed(self, detail):
        """On detail parse event handler.

        """
        owner = self._maps[detail.owner]
        owner['details'] = owner.get('details', [])
        owner['details'].append(self._maps[detail])
        self._maps[detail]['uiOrdinal'] = len(owner['details'])


    def on_enum_parsed(self, enum):
        """On enum parsed event handler.

        """
        detail = self._maps[enum.detail]
        detail['enum'] = self._maps[enum]


    def on_enumchoice_parsed(self, choice):
        """On process detail property enum choice parse event handler.

        """
        if choice.is_other:
            return

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
        obj['details'] = []
        obj['detailSets'] = []
        self._maps[topic] = obj

        return obj


    def _strip(self, obj):
        """Strips null keys from mapped objects.

        """
        if not obj['details']:
            del obj['details']
        if not obj['detailSets']:
            del obj['detailSets']
