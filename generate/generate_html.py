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

_HTML='''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>ES-DOC - Specialization</title>
        <link rel="shortcut icon" type="image/x-icon" href="media/app/img/favicon.ico" />
        <link href="media/ext/bootstrap-3.3.6/css/bootstrap.min.css" rel="stylesheet" type="text/css" media="screen" />
        <link href="media/app/css/header.css" media="screen" rel="stylesheet" type="text/css" />
        <link href="media/app/css/main.css" media="screen" rel="stylesheet" type="text/css" />
    </head>
    <body>
    <header class="clearfix main">
        <img src="media/app/img/logo-1.png" alt="Earth System Documentation" title="Earth System Documentation" class="pull-left" />
        <h1 class="pull-right">
            <small><b>Specializations Viewer</b>
            </small>
            <b class="h6"> v0.9.7.5</b>
            <button class="esdoc-support btn btn-success">Support</button>
        </h1>
    </header>
    </body>
</html>
'''

_HTML_ARTICLE = '''
<article id='{}'>
    <header>
        <h2 class="bg-primary">{}</h2>
    </header>
</article>
'''

_HTML_SECTION = '''
<section id='{}'>
    <header>
        <h3 class="bg-primary">{}</h3>
    </header>
    <table class="table table-striped table-hover table-condensed">
        <thead>
            <tr>
                <th class="prop-name">Property Long Name</th>
                <th class="prop-cardinality">Cardinality</th>
                <th class="prop-typeof">Type</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
</section>
'''

_HTML_PROPERTY = '''
<tr>
    <td class="prop-name">{}</td>
    <td class="prop-cardinality">{}</td>
    <td class="prop-typeof">{}</td>
</tr>
'''

_HTML_ENUM = '''
<select>
    <option>enum</option>
</select>
'''


class Generator(SpecializationParser):
    """Specialization to HTML generator.

    """
    def __init__(self, root, short_tables):
        """Instance constructor.

        """
        super(Generator, self).__init__(root, short_tables)

        self.nodes = {}
        self.article = None
        self.sections = []


    def get_output(self):
        """Returns generated output as a text blob.

        """
        for section in self.sections:
            self.article.append(section)
        html = ET.fromstring(_HTML)
        html[1].append(self.article)

        return ET.tostring(html)


    def on_root_parse(self, root):
        """On root parse event handler.

        """
        html = _HTML_ARTICLE.format(
            root.id,
            'CMIP6 {} Specializations'.format(root.name_camel_case_spaced)
            )

        self.article = ET.fromstring(html)


    def on_grid_parse(self, grid):
        """On grid parse event handler.

        """
        html = _HTML_SECTION.format(grid.id, 'Grid')

        self.sections.append(ET.fromstring(html))


    def on_keyprops_parse(self, key_props):
        """On key-properties parse event handler.

        """
        html = _HTML_SECTION.format(key_props.id, 'Key Properties')

        self.sections.append(ET.fromstring(html))


    def on_process_parse(self, process):
        """On process parse event handler.

        """
        html = _HTML_SECTION.format(process.id, process.name_camel_case_spaced)

        self.sections.append(ET.fromstring(html))


    def on_property_parse(self, prop):
        """On property parse event handler.

        """
        if prop.enum:
            options = ['<option title="{}">{}</option>'.format(i.value, i.value) for i in prop.enum if i.value != 'N/A']
            options = ''.join(options)
            enum = '<select><option>enum</option>{}</select>'.format(options)
            html = _HTML_PROPERTY.format(
                prop.long_name,
                prop.cardinality,
                enum)
        else:
            html = _HTML_PROPERTY.format(
                prop.long_name,
                prop.cardinality,
                prop.typeof.split(':')[0].lower()
                )

        self.sections[-1][1][1].append(ET.fromstring(html))
