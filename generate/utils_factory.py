"""
.. module:: factory.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Takes specialization modules and returns instances of wrapper classes.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from utils_model import DetailSpecialization
from utils_model import DetailSetSpecialization
from utils_model import EnumSpecialization
from utils_model import EnumChoiceSpecialization
from utils_model import TopicSpecialization



def create_specialization(spec):
    """Returns a realm specialization wrapper.

    :param spec: 4 member tuple: realm, grid, key-properties, processes.

    :returns: A realm specialization wrapper.
    :rtype: TopicSpecialization

    """
    r = _create_topic(None, spec[0], "realm")
    r.grid = _create_topic(r, spec[1], "grid")
    r.key_properties = _create_topic(r, spec[2], "key-properties")
    r.processes = [_create_topic(r, i, "process") for i in spec[3]]

    return r


def _create_topic(parent, spec, type_key, key=None):
    """Creates & returns a topic specialization wrapper.

    """
    topic = TopicSpecialization()
    topic.cfg_section = type_key
    topic.type_key = type_key
    topic.spec = spec

    if isinstance(spec, dict):
        _set_topic_from_dict(parent, topic, key)
    else:
        _set_topic_from_module(parent, topic)

    topic.name_camel_case = _to_camel_case(topic.name)
    topic.name_camel_case_spaced = _to_camel_case_spaced(topic.name)
    if parent:
        topic.parent = parent
        parent.subtopics.append(topic)

    return topic


def _set_topic_from_module(parent, topic):
    """Set topic specialization attributes from a module.

    """
    topic.authors = topic.spec.AUTHORS
    topic.contact = topic.spec.CONTACT
    topic.qc_status = topic.spec.QC_STATUS
    topic.description = topic.spec.DESCRIPTION
    if parent:
        topic.change_history = parent.change_history
        topic.contributors = parent.contributors
        topic.name = "_".join(topic.spec.__name__.split(".")[-1].split("_")[1:])
        topic.id = "{}.{}".format(parent.id, topic.name)
    else:
        topic.change_history = topic.spec.CHANGE_HISTORY
        topic.contributors = topic.spec.CONTRIBUTORS
        topic.name = topic.spec.__name__
        topic.id = "cmip6.{}".format(topic.name)

    # Assign detail / detail sets.
    for key, obj in topic.spec.DETAILS.items():
        # ... topic toplevel details
        if key == "toplevel":
            _set_details(topic, key, obj, topic.spec.ENUMERATIONS)

        # ... topic toplevel detail sets
        elif key.startswith("toplevel"):
            _set_detailset(topic, key, obj, topic.spec.ENUMERATIONS)

        # ... sub-process
        elif topic.type_key == "process" and len(key.split(":")) == 1:
            _create_topic(topic, obj, "sub-process", key)
            _set_details(topic.subtopics[-1], key, obj, topic.spec.ENUMERATIONS)

        # ... sub-process detail set
        elif topic.type_key == "process" and len(key.split(":")) == 2:
            for t in topic.subtopics:
                if t.name == key.split(":")[0]:
                    _set_detailset(t, key, obj, topic.spec.ENUMERATIONS)

        # ... grid / key-properties details
        elif len(key.split(":")) == 1:
            _set_detailset(topic, key, obj, topic.spec.ENUMERATIONS)

        # ... grid / key-properties detail set
        elif len(key.split(":")) == 2:
            for ds in topic.detailsets:
                if ds.name == key.split(":")[0]:
                    _set_detailset(ds, key, obj, topic.spec.ENUMERATIONS)


def _set_topic_from_dict(parent, topic, name):
    """Set topic specialization attributes from a dictionary.

    """
    topic.authors = parent.authors
    topic.contact = parent.contact
    topic.change_history = parent.change_history
    topic.contributors = parent.contributors
    topic.description = topic.spec['description']
    topic.id = "{}.{}".format(parent.id, name)
    topic.name = name
    topic.qc_status = parent.qc_status


def _set_detailset(owner, key, obj, enumerations):
    """Set detail set attributes from a dictionary.

    """
    ds = DetailSetSpecialization()
    ds.description = obj['description']
    ds.id = "{}.{}".format(owner.id, key.split(":")[-1])
    ds.key = key
    ds.name = key.split(":")[-1]
    ds.owner = owner
    _set_details(ds, key, obj, enumerations)

    owner.detailsets.append(ds)


def _set_details(owner, key, obj, enumerations):
    """Set detail attributes from a dictionary.

    """
    for name, typeof, cardinality, description in obj['properties']:
        d = DetailSpecialization()
        d.cardinality = cardinality
        d.description = description
        d.enum = _create_enum(d, typeof, enumerations) if typeof.startswith("ENUM:") else None
        d.id = "{}.{}".format(owner.id, name)
        d.key = name
        d.name = name
        d.owner = owner
        d.typeof = typeof

        owner.details.append(d)


def _create_enum(detail, typeof, enumerations):
    """Creates & returns an enumeration specialzation wrapper.

    """
    key = typeof.split(":")[-1]
    obj = enumerations[key]

    e = EnumSpecialization()
    e.description = obj['description']
    e.detail = detail
    e.id = "{}.{}".format(detail.id, key)
    e.is_open = obj['is_open']
    e.label = key
    e.name = key
    e.id = key
    e.choices = [_create_enum_choice(e, i[0], i[1]) for i in obj.get('members', [])]
    if e.is_open:
        e.choices.append(_create_enum_choice(e, "Other", None))

    return e


def _create_enum_choice(enum, value, description):
    """Creates & returns an enumeration choice specialzation wrapper.

    """
    ec = EnumChoiceSpecialization()
    ec.description = description
    ec.enum = enum
    ec.id = "{}.{}".format(enum.id, value)
    ec.is_other = (value == 'Other')
    ec.value = value

    return ec


def _to_camel_case_spaced(name, separator='_'):
    """Converts passed name to camel case with space.

    :param str name: A name as specified in ontology specification.
    :param str separator: Separator to use in order to split name into constituent parts.

    """
    s = _to_camel_case(name, separator)
    r = s[0]
    for s in s[1:]:
        if s.upper() == s:
            r += " "
        r += s

    return r


def _to_camel_case(name, separator='_'):
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
