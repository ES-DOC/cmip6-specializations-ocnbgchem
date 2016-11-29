# -*- coding: utf-8 -*-

"""
.. module:: write_cmip6_xmind.py
   :platform: Unix, Windows
   :synopsis: Rewrites a cmip6 realm specialization to mindmap.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import json

import xml.etree.ElementTree as ET

from cim_profile import CIM_PROFILE
from utils_model import DetailSpecialization
from utils_model import TopicSpecialization

from utils_parser import Parser



# HTML snippet for a set of notes.
_NOTES_HTML = """
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
_NOTE_HTML = "<dt><b>{}</b></dt><dd>{}</dd>"

# Mind-map sections.
_SECTIONS = collections.OrderedDict()
_SECTIONS['realm'] = "science.realm"
_SECTIONS['process'] = "science.process"
_SECTIONS['sub-process'] = "science.sub_process"
_SECTIONS['key-properties'] = "science.key_properties"
_SECTIONS['grid'] = "science.grid"
_SECTIONS['detail-set'] = "science.detail"
_SECTIONS['detail'] = None
_SECTIONS['enum-choice'] = None


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
        self._emit_change_history(realm)
        self._emit_legend(realm)
        self._emit_cim_profile(realm)


    def on_grid_parse(self, grid):
        """On grid parse event handler.

        """
        self._emit_node(self.realm, grid)


    def on_keyproperties_parse(self, key_properties):
        """On key_properties parse event handler.

        """
        self._emit_node(self.realm, key_properties)


    def on_process_parse(self, process):
        """On process parse event handler.

        """
        self._emit_node(self.realm, process)
        self._emit_notes(process)


    def on_subprocess_parse(self, subprocess):
        """On sub-process parse event handler.

        """
        self._emit_node(subprocess.parent, subprocess)


    def on_detailset_parse(self, detailset):
        """On process detail set parse event handler.

        """
        self._emit_node(detailset.owner, detailset)


    def on_detail_parse(self, detail):
        """On detail property parse event handler.

        """
        self._emit_node(detail.owner, detail)
        self._emit_notes(detail)


    def on_enumchoice_parse(self, choice):
        """On enum property parse event handler.

        """
        self._emit_node(choice.enum.detail, choice, text=choice.value)


    def _emit_node(self, parent, owner, text=None, style="bubble"):
        """Sets a mindmap node.

        """
        # Get section style config.
        cfg = self.cfg.get_section(owner.cfg_section)

        # Initialise mindmap node attributes.
        atts = {
            'FOLDED': str(cfg['is-collapsed']).lower(),
            'COLOR': cfg['font-color'],
            'BACKGROUND_COLOR': cfg['bg-color'],
            'STYLE': style,
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
        parent = owner if isinstance(owner, ET.Element) else \
                 self.nodes[owner]

        # Set notes.
        notes = notes or _get_notes(owner)

        # Convert to HTML.
        html = []
        for k, value in notes:
            try:
                owner.id
            except AttributeError:
                pass
            else:
                value = value(owner)
            html.append(_NOTE_HTML.format(k, value))
        html = _NOTES_HTML.format("".join(html))

        # Extend mindmap.
        node = ET.SubElement(parent, 'richcontent', {"TYPE": "NOTE"})
        node.append(ET.fromstring(html))


    def _emit_legend(self, realm):
        """Emits mindmap legend.

        """
        cfg = self.cfg.get_section
        root_node = ET.SubElement(self.nodes[realm], 'node', {
            'FOLDED': "true",
            'STYLE': "bubble",
            'TEXT': "LEGEND",
            'POSITION': "left"
            })
        for section in _SECTIONS:
            node = ET.SubElement(root_node, 'node', {
                'BACKGROUND_COLOR': cfg(section)['bg-color'],
                'COLOR': cfg(section)['font-color'],
                'STYLE': "bubble",
                'TEXT': section
                })
            self._emit_notes(node, notes=[
                ('Description', cfg(section)['description']),
                ])


    def _emit_cim_profile(self, realm):
        """Emits mindmap cim profile.

        """
        cfg = self.cfg.get_section
        root_node = ET.SubElement(self.nodes[realm], 'node', {
            'FOLDED': "true",
            'STYLE': "bubble",
            'TEXT': "DETAILS INHERITED FROM CIM",
            'POSITION': "left"
            })
        for section, cim_type in _SECTIONS.iteritems():
            if cim_type in CIM_PROFILE:
                node = ET.SubElement(root_node, 'node', {
                    'BACKGROUND_COLOR': cfg(section)['bg-color'],
                    'COLOR': cfg(section)['font-color'],
                    'STYLE': "bubble",
                    'TEXT': section
                    })
                for name in CIM_PROFILE[cim_type]['include']:
                    ET.SubElement(node, 'node', {
                        'BACKGROUND_COLOR': cfg(section)['bg-color'],
                        'COLOR': cfg(section)['font-color'],
                        'STYLE': "bubble",
                        'TEXT': name
                        })


    def _emit_change_history(self, realm):
        """Emits mindmap realm change history.

        """
        root_node = ET.SubElement(self.nodes[realm], 'node', {
            'FOLDED': "true",
            'STYLE': "bubble",
            'TEXT': "CHANGE HISTORY",
            'POSITION': "left"
            })
        for version, date, person, comment in realm.change_history:
            node = ET.SubElement(root_node, 'node', {
                'STYLE': "bubble",
                'TEXT': version
                })
            self._emit_notes(node, [
                ("Version", version),
                ("Date", date),
                ("Person", person),
                ("Comment", comment),
            ])


def _get_notes(spec):
    """Returns notes to be appended to a mindmap node.

    """
    result = [
        ("Description", lambda i: "N/A" if i.description is None else i.description.replace("&", "and"))
    ]
    if isinstance(spec, DetailSpecialization):
        result += [
            ("Type", lambda i: i.typeof),
            ("Cardinality", lambda i: i.cardinality),
            ("Specialization ID", lambda i: i.id)
        ]
    elif isinstance(spec, TopicSpecialization):
        result += [
            ("QC status", lambda i: i.qc_status),
            ("Contact", lambda i: i.contact),
            ("Authors", lambda i: i.authors),
            ("Contributors", lambda i: i.contributors)
        ]

    return result
