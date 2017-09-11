# -*- coding: utf-8 -*-

"""
.. module:: generator.py
   :platform: Unix, Windows
   :synopsis: Encodes a cmip6 specialization as HTML.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os

from utils_parser import SpecializationParser



class Generator(SpecializationParser):
    """Specialization to HTML generator.

    """
    def get_output(self):
        """Returns generated output as a text blob.

        """
        fpath = '{}/generate_html.template'.format(os.path.dirname(__file__))
        with open(fpath) as fstream:
            fcontent = fstream.read()

        return fcontent.replace('SPECIALIZATION', self.root.name)
