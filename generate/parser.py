# -*- coding: utf-8 -*-

"""
.. module:: parser.py
   :platform: Unix, Windows
   :synopsis: An event style specializations parser.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
class Parser(object):
    """An event driven CMIP6 realm specializations parser.

    """
    def __init__(self, realm):
        """Instance constructor.

        """
        self.realm = realm


    def run(self):
        """Runs the parser raising events as it does so.

        """
        self._parse_realm(self.realm)


    def _parse_realm(self, r):
        """Parses a realm.

        """
        self.on_realm_parse(r)
        self._parse_details(r)

        if r.grid:
            self.on_grid_parse(r.grid)
            self._parse_details(r.grid)
            self.on_grid_parsed(r.grid)

        if r.key_properties:
            self.on_keyproperties_parse(r.key_properties)
            self._parse_details(r.key_properties)
            self.on_keyproperties_parsed(r.key_properties)

        for p in r.processes:
            self.on_process_parse(p)
            self._parse_details(p)
            for sp in p.subtopics:
                self.on_subprocess_parse(sp)
                self._parse_details(sp)
                self.on_subprocess_parsed(sp)
            self.on_process_parsed(p)

        self.on_realm_parsed(r)


    def _parse_details(self, container):
        """Parses a set of details.

        """
        for d in container.details:
            self.on_detail_parse(d)
            if d.enum:
                self.on_enum_parse(d.enum)
                for ec in d.enum.choices:
                    self.on_enumchoice_parse(ec)
                    self.on_enumchoice_parsed(ec)
                self.on_enum_parsed(d.enum)
            self.on_detail_parsed(d)

        for ds in container.detailsets:
            self.on_detailset_parse(ds)
            self._parse_details(ds)
            self.on_detailset_parsed(ds)


    def on_realm_parse(self, realm):
        """On realm parse event handler.

        """
        pass


    def on_realm_parsed(self, realm):
        """On realm parsed event handler.

        """
        pass


    def on_grid_parse(self, grid):
        """On grid parse event handler.

        """
        pass


    def on_grid_parsed(self, grid):
        """On grid parsed event handler.

        """
        pass


    def on_keyproperties_parse(self, key_properties):
        """On key-properties parse event handler.

        """
        pass


    def on_keyproperties_parsed(self, key_properties):
        """On key-properties parsed event handler.

        """
        pass


    def on_process_parse(self, process):
        """On process parse event handler.

        """
        pass


    def on_process_parsed(self, process):
        """On process parsed event handler.

        """
        pass


    def on_subprocess_parse(self, subprocess):
        """On sub-process parse event handler.

        """
        pass


    def on_subprocess_parsed(self, subprocess):
        """On sub-process parsed event handler.

        """
        pass


    def on_detailset_parse(self, detail_set):
        """On detail set parse event handler.

        """
        pass


    def on_detailset_parsed(self, detail_set):
        """On detail set parsed event handler.

        """
        pass


    def on_detail_parse(self, detail):
        """On detail parse event handler.

        """
        pass


    def on_detail_parsed(self, detail):
        """On detail parsed event handler.

        """
        pass


    def on_enum_parse(self, enum):
        """On enum parse event handler.

        """
        pass


    def on_enum_parsed(self, enum):
        """On enum parsed event handler.

        """
        pass


    def on_enumchoice_parse(self, choice):
        """On enum choice parse event handler.

        """
        pass


    def on_enumchoice_parsed(self, choice):
        """On enum choice parsed event handler.

        """
        pass
