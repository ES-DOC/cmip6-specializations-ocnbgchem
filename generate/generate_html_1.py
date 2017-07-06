# -*- coding: utf-8 -*-

"""
.. module:: generatehtml.py
   :platform: Unix, Windows
   :synopsis: Encodes a specialization as HTML.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import json

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

from utils import get_label
from utils_constants import *
from utils_parser import SpecializationParser



_HTML_ARTICLE = '''
<article id='{}'>
    <header>
        <h2>{}</h2>
    </header>
</article>
'''

_HTML_SECTION = '''
<section id='{}'>
    <header>
        <h3>{}</h3>
        <span style='margin-left: 20px;'>{}</span>
    </header>
    <dl style='margin-left: 20px;'></dl>
</section>
'''

_HTML_DETAIL = '''
<dl>
<dt><strong>{}</strong> ({}, {})</dt>
<dd>
    {}
</dd>
</dl>
'''


class Generator(SpecializationParser):
    """Specialization to HTML generator.

    """
    def __init__(self, root, short_tables):
        """Instance constructor.

        """
        super(Generator, self).__init__(root, short_tables)

        self.nodes = {}


    def get_output(self):
        """Returns generated output as a text blob.

        """
        return ET.tostring(self.nodes[self.root])


    def on_root_parse(self, root):
        """On root parse event handler.

        """
        html = _HTML_ARTICLE.format(
            root.id,
            'CMIP6 Specialization: {}'.format(root.name_camel_case_spaced)
            )

        self.nodes[root] = ET.fromstring(html)


    def on_property_parse(self, prop):
        """On property parse event handler.

        """
        if prop.owner not in self.nodes:
            html = _HTML_SECTION.format(
                prop.owner.id,
                prop.owner.names(offset=2),
                prop.owner.description
                )
            html = ET.fromstring(html)
            self.nodes[prop.owner] = html
            self.nodes[self.root].append(html)

        html = _HTML_DETAIL.format(
            prop.name_camel_case_spaced,
            prop.cardinality,
            prop.typeof,
            prop.description
            )

        try:
            html = ET.fromstring(html)
        except ParseError as err:
            print 666, err
            pass
        else:
            self.nodes[prop.owner][1].append(html)
