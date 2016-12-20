# -*- coding: utf-8 -*-

"""
.. module:: model.py
   :platform: Unix, Windows
   :synopsis: A repesentation of CMIP6 specializations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
class TopicSpecialization(object):
    """Wraps a topic specialization.

    """
    def __init__(self):
        """Instance initializer.

        """
        self.authors = None
        self.cfg_section = None
        self.contact = None
        self.contributors = None
        self.description = None
        self.details = []
        self.detailsets = []
        self.id = None
        self.qc_status = None
        self.name = None
        self.name_camel_case = None
        self.name_camel_case_spaced = None
        self.parent = None
        self.spec = None
        self.subtopics = []
        self.type_key = None


    @property
    def ENUMS(self):
        try:
            return self.spec.ENUMERATIONS
        except AttributeError:
            try:
                return self.parent.spec.ENUMERATIONS
            except AttributeError:
                return []


class DetailSetSpecialization(object):
    """Wraps a detail set specialization.

    """
    def __init__(self):
        """Instance initializer.

        """
        super(DetailSetSpecialization, self).__init__()

        self.cfg_section = "detail-set"
        self.description = None
        self.details = []
        self.detailsets = []
        self.id = None
        self.name = None
        self.owner = None
        self.topic = None


class DetailSpecialization(object):
    """Wraps a detail specialization.

    """
    def __init__(self):
        """Instance initializer.

        """
        super(DetailSpecialization, self).__init__()

        self.cardinality = None
        self.cfg_section = "detail"
        self.description = None
        self.enum = None
        self.id = None
        self.name = None
        self.owner = None
        self.topic = None
        self.typeof = None


    @property
    def is_mandatory(self):
        """Gets flag indicating whether cardinality is mandatory or not.

        """
        return self.cardinality.split(".")[0] == "0"


    @property
    def is_collection(self):
        """Gets flag indicating whether property is a collection or not.

        """
        try:
            int(self.cardinality.split(".")[1])
        except ValueError:
            return True
        return False


    @property
    def typeof_label(self):
        """Gets label for the property type.

        """
        if self.typeof == 'str':
            return "STRING"
        elif self.typeof == 'bool':
            return "BOOLEAN"
        elif self.typeof == 'int':
            return "INTEGER"
        elif self.typeof == 'float':
            return "FLOAT"

        return self.typeof.upper()


class EnumSpecialization(object):
    """Wraps an enumeration specialization.

    """
    def __init__(self):
        """Instance initializer.

        """
        self.cfg_section = "enum"
        self.choices = []
        self.description = None
        self.id = None
        self.is_open = False
        self.label = None
        self.name = None


class EnumChoiceSpecialization(object):
    """Wraps an enumeration choice specialization.

    """
    def __init__(self):
        """Instance initializer.

        """
        self.cfg_section = "enum-choice"
        self.description = None
        self.enum = None
        self.id = None
        self.value = None
        self.is_other = None
