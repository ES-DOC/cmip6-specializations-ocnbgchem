# -*- coding: utf-8 -*-

"""
.. module:: generator.py
   :platform: Unix, Windows
   :synopsis: Encodes a cmip6 specialization as JSON.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import json
import operator
import os


from utils import get_label
from utils_constants import *
from utils_parser import SpecializationParser



class Generator(SpecializationParser):
    """Specialization to Javascript generator.

    """
    def __init__(self, project, root, short_tables):
        """Instance constructor.

        """
        super(Generator, self).__init__(project, root, short_tables)

        self._maps = collections.OrderedDict()
        self.on_grid_parse = self.on_topic_parse
        self.on_keyprops_parse = self.on_topic_parse
        self.on_process_parse = self.on_topic_parse


    def get_output(self):
        """Returns generated output as a text blob.

        """
        data = json.dumps(self._maps[self.root])
        fpath = '{}/generate_js.template'.format(os.path.dirname(__file__))
        with open(fpath) as fstream:
            return fstream.read().replace('TOPIC', data)


    def _on_topic_parse(self, topic):
        """On topic parse event handler.

        """
        obj = collections.OrderedDict()
        obj['label'] = get_label(topic.name)
        obj['description'] = topic.description
        obj['id'] = topic.id
        obj['contact'] = topic.contact
        obj['properties'] = []
        self._maps[topic] = obj


    def on_root_parse(self, root):
        """On root parse event handler.

        """
        obj = collections.OrderedDict()
        obj['id'] = root.id
        obj['label'] = get_label(root.name)
        obj['description'] = root.description
        obj['contact'] = root.contact
        obj['project'] = 'cmip6'
        obj['shortTables'] = []
        obj['subTopics'] = []

        self._maps[root] = obj


    def on_root_parsed(self, root):
        """On root parsed event handler.

        """
        for obj in [self._maps[i] for i in self.root.sub_topics]:
            self._maps[root]['subTopics'].append(obj)
        for obj in [self._maps[i] for i in self.short_tables]:
            self._maps[root]['shortTables'].append(obj)


    def on_topic_parse(self, topic):
        """On topic parse event handler.

        """
        obj = collections.OrderedDict()
        obj['id'] = topic.id
        obj['label'] = get_label(topic.name)
        obj['description'] = topic.description
        obj['properties'] = []

        self._maps[topic] = obj


    def on_property_parse(self, prop):
        """On property parse event handler.

        """
        obj = collections.OrderedDict()
        obj['id'] = prop.id
        obj['label'] = " > ".join([get_label(i) for i in prop.id.split('.')[3:]])
        obj['description'] = prop.description
        obj['cardinality'] = prop.cardinality
        obj['type'] = "enum" if prop.enum else prop.typeof
        if prop.enum:
            obj['enum'] = self._get_enum(prop.enum)

        properties = self._maps[prop.root_topic]['properties']
        properties.append(obj)


    def _get_enum(self, enum):
        """Returns enumeration encoded as a dictionary.

        """
        obj = collections.OrderedDict()
        obj['id'] = enum.description
        obj['label'] = get_label(enum.name)
        obj['description'] = enum.description
        obj['is_open'] = enum.is_open
        obj['choices'] = []
        for choice in enum:
            obj['choices'].append({
                'description': choice.description,
                'value': choice.value
                })

        return obj

    def on_short_table_parse(self, short_table):
        """On short tables parse event handler.

        """
        obj = collections.OrderedDict()
        obj['id'] = short_table.name
        obj['label'] = short_table.label
        obj['properties'] = [collections.OrderedDict(
            id=i.identifier,
            priority=i.priority
        ) for i in short_table]

        self._maps[short_table] = obj
