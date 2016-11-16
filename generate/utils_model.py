# -*- coding: utf-8 -*-

"""
.. module:: model.py
   :platform: Unix, Windows
   :synopsis: A repesentation of CMIP6 specializations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from collections import OrderedDict

from cim_profile import CIM_PROFILE



class RealmSpecialization(object):
    """Wraps a CMIP6 realm specialization.

    """
    def __init__(self, defn):
        """Instance constructor.

        :param tuple defn: 4 member tuple of realm, grid, key-properties & processes.

        """
        mixin_topic(self, defn[0], "realm", None)
        self.details = []
        self.grid = GridSpecialization(self, defn[1]) if defn[1] else None
        self.key_properties = KeyPropertiesSpecialization(self, defn[2]) if defn[2] else None
        self.processes = [ProcessSpecialization(self, i) for i in defn[3]]


class GridSpecialization(object):
    """Wraps a CMIP6 grid specialization.

    """
    def __init__(self, owner, defn):
        """Instance constructor.

        """
        mixin_topic(self, defn, "grid", owner)
        mixin_detail_sets(self, defn)


class KeyPropertiesSpecialization(object):
    """Wraps a CMIP6 key-properties specialization.

    """
    def __init__(self, owner, defn):
        """Instance constructor.

        """
        mixin_topic(self, defn, "key-properties", owner)
        mixin_detail_sets(self, defn)


class ProcessSpecialization(object):
    """Wraps a CMIP6 process specialization.

    """
    def __init__(self, realm, defn):
        """Instance constructor.

        :param model.RealmSpecialization realm: Wrapper around realm specialization.
        :param module defn: Python module that process is defined as.

        """
        mixin_topic(self, defn, "process", realm)
        mixin_detail_sets(self, defn)
        self.details = []
        self.sub_processes = [SubProcessSpecialization(i, defn.SUB_PROCESSES[i], self)
                              for i in defn.SUB_PROCESSES if len(i.split(":")) == 1]


class SubProcessSpecialization(object):
    """Wraps a CMIP6 sub-process specialization.

    """
    def __init__(self, name, defn, process):
        """Instance constructor.

        :param str name: Name of sub-process.
        :param dictionary defn: Sub-process definition.
        :param model.Process process: Wrapper around process specialization.

        """
        self.cfg_section = "sub-process"
        self.description = defn['description']
        self.details = [DetailSpecialization(i, self, process.defn.ENUMERATIONS) for i in defn.get('properties', [])]
        self.detail_sets = []
        self.id = "{}.{}".format(process.id, name)
        self.name = name
        self.name_camel_case = to_camel_case(self.name)
        self.name_camel_case_spaced = to_camel_case_spaced(self.name)

        # Set associated detail sets.
        # TODO wire hierachy
        for i, j in process.defn.SUB_PROCESSES.items():
            if i.startswith("{}:".format(name)):
                self.detail_sets.append(DetailSetSpecialization(i, j, self, process.defn.ENUMERATIONS))


class DetailSetSpecialization(object):
    """Wraps a CMIP6 detail set specialization.

    """
    def __init__(self, name, defn, container, enumerations):
        """Instance constructor.

        :param str name: Detail set name.
        :param dict defn: Detail set definition.
        :param object container: Specializations with which the detail set is associated.
        :param dict enumerations: Associated collection of enumerations.

        """
        self.name = name.split(":")[-1]
        self.cfg_section = "detail-set"
        self.defn = defn
        self.description = defn['description']
        self.detail_sets = []
        self.parent = None
        try:
            self.id = "{}.{}".format(container.id, self.name)
        except AttributeError:
            self.id = None
        self.details = [DetailSpecialization(i, self, enumerations) for i in defn.get('properties', [])]


class DetailSpecialization(object):
    """Wraps a CMIP6 detail specialization.

    """
    def __init__(self, defn, container, enumerations):
        """Instance constructor.

        """
        self.name, self.typeof, self.cardinality, self.description = defn
        self.container = container
        self.cfg_section = "detail"
        if self.typeof.startswith("ENUM"):
            enum_name = self.typeof.split(":")[-1]
            self.enum = EnumSpecialization(enum_name, enumerations[enum_name])
            self.typeof = "enum"
        else:
            self.enum = None


    @property
    def id(self):
        """Gets detail id - very important when building a comparator.

        """
        return "{}.{}".format(self.container.id, self.name)


    def short_id(self, idx):
        return ".".join(self.id.split(".")[idx:])


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
        else:
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
    """Wraps a CMIP6 enumeration specialization.

    """
    def __init__(self, name, defn):
        """Instance constructor.

        :param str name: Name of enumeration.
        :param dict defn: Enumeration specialization.

        """
        self.cfg_section = "enum"
        self.description = defn['description']
        self.id = name
        self.is_open = defn['is_open']
        self.label = name
        self.name = name
        self.choices = [EnumChoiceSpecialization(i[0], i[1], self) for i in
                        sorted(defn['members'])]
        if self.is_open:
            self.choices.append(EnumChoiceSpecialization("Other", None, self))


class EnumChoiceSpecialization(object):
    """Wraps a CMIP6 enumeration choice specialization.

    """
    def __init__(self, value, description, enum):
        """Instance constructor.

        :param model.Enum enum: Wrapper around enum specialization.
        :param str value: Enum choice value.
        :param str description: Enum choice description.

        """
        self.cfg_section = "enum-choice"
        self.description = description
        self.id = "{}.{}".format(enum.id, value)
        self.value = value
        self.is_other = (value == 'Other')


def mixin_topic(spec, defn, cfg_section, owner):
    """Topic mixin to extend specialization wrappers.

    """
    spec.authors = defn.AUTHORS
    spec.cfg_section = cfg_section
    spec.contact = defn.CONTACT
    try:
        spec.contributors = defn.CONTRIBUTORS
    except AttributeError:
        spec.contributors = ""
    spec.description = defn.DESCRIPTION
    spec.defn = defn
    spec.qc_status = defn.QC_STATUS

    if owner:
        spec.name = "_".join(defn.__name__.split(".")[-1].split("_")[1:])
        spec.id = "{}.{}".format(owner.id, spec.name)
    else:
        spec.name = defn.__name__
        spec.id = "cmip6.{}".format(spec.name)

    spec.name_camel_case = to_camel_case(spec.name)
    spec.name_camel_case_spaced = to_camel_case_spaced(spec.name)
    try:
        spec.description = defn.DESCRIPTION
    except AttributeError:
        spec.description = spec.name


def mixin_detail_sets(spec, defn, target="DETAILS"):
    """Detail sets mixin to extend specialization wrappers.

    """
    # Set master collection.
    detail_sets = OrderedDict()
    for i, j in getattr(defn, target).items():
        detail_sets[i] = DetailSetSpecialization(i, j, spec, defn.ENUMERATIONS)
    # detail_sets = {i: DetailSetSpecialization(i, j, spec, defn.ENUMERATIONS)
    #                for i, j in getattr(defn, target).items()
    #                if isinstance(j, dict)}

    # Wire hierarchy.
    for i in defn.DETAILS:
        if not i.split(":")[0:-1]:
            continue
        child = detail_sets[i]
        parent = detail_sets[":".join(i.split(":")[0:-1])]
        child.parent = parent
        child.parent.detail_sets.append(child)
        del detail_sets[i]

    # Set parsed collection.
    spec.detail_sets = detail_sets.values()


def to_camel_case_spaced(name, separator='_'):
    """Converts passed name to camel case with space.

    :param str name: A name as specified in ontology specification.
    :param str separator: Separator to use in order to split name into constituent parts.

    """
    s = to_camel_case(name, separator)
    r = s[0]
    for s in s[1:]:
        if s.upper() == s:
            r += " "
        r += s

    return r


def to_camel_case(name, separator='_'):
    """Converts passed name to camel case.

    :param str name: A name as specified in ontology specification.
    :param str separator: Separator to use in order to split name into constituent parts.

    """
    r = ''
    if name is not None:
        s = name.split(separator)
        for s in s:
            if (len(s) > 0):
                r += s[0].upper()
                if (len(s) > 1):
                    r += s[1:]
    return r


