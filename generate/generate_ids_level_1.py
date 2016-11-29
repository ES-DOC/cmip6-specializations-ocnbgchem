# -*- coding: utf-8 -*-

"""
.. module:: generate_ids_level_1.py
   :platform: Unix, Windows
   :synopsis: Generates level 1 identifiers.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from generate_ids import Generator as IdentifierGenerator



class Generator(IdentifierGenerator):
    """Specialization to mindmap generator.

    """
    def on_realm_parse(self, realm):
        """On realm parse event handler.

        """
        self.set_id(realm)


    def on_grid_parse(self, grid):
        """On grid parse event handler.

        """
        self.emit_null_row(grid)
        self.set_id(grid)


    def on_keyproperties_parse(self, key_properties):
        """On key_properties parse event handler.

        """
        self.emit_null_row(key_properties)
        self.set_id(key_properties)


    def on_process_parse(self, process):
        """On process parse event handler.

        """
        self.emit_null_row(process)
        self.set_id(process)


    def on_subprocess_parse(self, subprocess):
        """On sub-process parse event handler.

        """
        self.set_id(subprocess)
