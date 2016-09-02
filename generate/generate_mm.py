# -*- coding: utf-8 -*-

"""
.. module:: write_cmip6_xmind.py
   :platform: Unix, Windows
   :synopsis: Rewrites a cmip6 realm specialization to mindmap.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import json

import xml.etree.ElementTree as ET

from utils_model import Process
from utils_model import SpecializationModule
from utils_parser import Parser



# HTML snippet for a set of notes.
_NOTES = """
<html>
  <head></head>
  <body>
    <dl>
        {}
    </dl>
  </body>
</html>
"""

# HTML snippet for a note.
_NOTE = "<dt><b>{}</b></dt><dd>{}</dd>"

# Set of configuration sections.
_CONFIG_SECTIONS = [
    "realm",
    "grid",
    "key-properties",
    "process",
    "sub-process",
    "detail",
    "detail-property",
    "enum-choice"
    ]



class _Configuration(object):
    """Wraps access to configuration information stored in associated config file.

    """
    def __init__(self):
        """Instance constructor.

        """
        fpath = "{}.conf".format(__file__.split(".")[0])
        with open(fpath, 'r') as fstream:
            self._data = json.loads(fstream.read())


    def get_section(self, key):
        """Returns a section within the config file.

        """
        return self._data.get(key, {})


class Generator(Parser):
    """Specialization to mindmap generator.

    """
    def __init__(self, realm):
        """Instance constructor.

        """
        super(Generator, self).__init__(realm)

        self.cfg = _Configuration()
        self.mmap = None
        self.nodes = {}


    def get_output(self):
        """Returns generated output as a text blob.

        """
        return ET.tostring(self.mmap)


    def on_realm_parse(self, realm):
        """On realm parse event handler.

        """
        self.mmap = ET.Element('map', {})
        self._emit_node(self.mmap, realm, style="fork")
        self._emit_legend(realm)


    def on_grid_parse(self, realm, grid):
        """On grid parse event handler.

        """
        self._emit_node(realm, grid)


    def on_grid_discretisation_parse(self, realm, grid, discretisation):
        """On grid discretisation parse event handler.

        """
        self._emit_node(grid, discretisation, cfg_section="grid")


    def on_key_properties_parse(self, realm, key_properties):
        """On key_properties parse event handler.

        """
        self._emit_node(realm, key_properties)


    def on_key_properties_conservation_parse(self, realm, key_properties, conservation):
        """On grid discretisation parse event handler.

        """
        self._emit_node(key_properties, conservation, cfg_section="key-properties")


    def on_process_parse(self, realm, process):
        """On process parse event handler.

        """
        self._emit_node(realm, process)
        self._emit_notes(process)


    def on_subprocess_parse(self, process, subprocess):
        """On sub-process parse event handler.

        """
        self._emit_node(process, subprocess)


    def on_detail_parse(self, owner, detail):
        """On process detail parse event handler.

        """
        self._emit_node(owner, detail)


    def on_detail_property_parse(self, detail, detail_property):
        """On detail property parse event handler.

        """
        self._emit_node(detail, detail_property)
        self._emit_notes(detail_property)

        if detail_property.enum:
            for choice in detail_property.enum.choices:
                self._emit_node(detail_property, choice, text=choice.value)


    def _emit_node(
        self,
        parent,
        owner,
        text=None,
        style=None,
        cfg_section=None
        ):
        """Sets a mindmap node.

        """
        # Get section style config.
        cfg = self.cfg.get_section(cfg_section if cfg_section else owner.cfg_section)

        # Initialise mindmap node attributes.
        atts = {
            'FOLDED': str(cfg['is-collapsed']).lower(),
            'COLOR': cfg['font-color'],
            'BACKGROUND_COLOR': cfg['bg-color'],
            'STYLE': style or "bubble",
            'TEXT': text if text else owner.name
        }

        # Set node url.
        try:
            owner.url
        except AttributeError:
            pass
        else:
            atts['LINK'] = owner.url

        # Get node parent.
        if not isinstance(parent, ET.Element):
            parent = self.nodes[parent]

        # Create new node & cache.
        self.nodes[owner] = ET.SubElement(parent, 'node', atts)

        # Set node font / notes.
        self._emit_font(owner, cfg)
        self._emit_notes(owner)


    def _emit_font(self, owner, cfg):
        """Set node font information.

        """
        ET.SubElement(self.nodes[owner], 'font', {
            'BOLD': str(cfg['font-bold']),
            'NAME': cfg['font-name'],
            'SIZE': str(cfg['font-size'])
            })


    def _emit_notes(self, owner, notes=None):
        """Set mindmap notes.

        """
        # Set parent mm node.
        if not isinstance(owner, ET.Element):
            parent = self.nodes[owner]
        else:
            parent = owner

        # Set notes.
        if not notes:
            try:
                notes = owner.notes
            except AttributeError:
                return

        # Convert to HTML.
        notes = [_NOTE.format(k, v) for k, v in notes if v]
        notes = _NOTES.format("".join(notes))

        # Extend mindmap.
        content = ET.SubElement(parent, 'richcontent', {"TYPE": "NOTE"})
        content.append(ET.fromstring(notes))


    def _emit_legend(self, realm):
        """Emits mindmap legend.

        """
        cfg = self.cfg.get_section
        legend = ET.SubElement(self.nodes[realm], 'node', {
            'STYLE': "bubble",
            'TEXT': "legend",
            'POSITION': "left"
            })
        for section in _CONFIG_SECTIONS:
            node = ET.SubElement(legend, 'node', {
                'BACKGROUND_COLOR': cfg(section)['bg-color'],
                'COLOR': cfg(section)['font-color'],
                'STYLE': "bubble",
                'TEXT': section
                })
            self._emit_notes(node, notes=[
                ('Description', cfg(section)['description']),
                ])
