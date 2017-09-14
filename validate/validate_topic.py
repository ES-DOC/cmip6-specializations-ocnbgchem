"""
.. module:: validate_topic.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a specialized CMIP6 scientific topic.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import collections
import re

import utils
import validate_property_set
import validate_enum



# Regular expression to apply over a specialization key.
_RE_KEY = '^[a-z0-9_:,CO2,CH4,N20,CFC,SO4]+$'


def validate(ctx, topic):
    """Validates a CMIP6 scientific detail topic.

    :param DefinitionsValidationContext ctx: Validation contextual information.
    :param module detail_topic: A python module containing specializations.

    """
    if topic is None:
        return

    # Set current module.
    ctx.module = topic

    # Level-1 validation.
    _validate_fields(ctx, topic)
    _validate_sections(ctx, topic)
    if ctx.errors[topic]:
        return

    # Level-2 validation.
    ctx.errors[topic] += \
        validate_property_set.validate(topic, topic.DETAILS)
    ctx.errors[topic] += \
        validate_enum.validate(topic.ENUMERATIONS)


def _validate_fields(ctx, module):
    """Validates a module's standard attributes.

    """
    for field, typeof in {
        ('AUTHORS', str),
        ('CONTACT', str),
        ('DESCRIPTION', str),
        ('DETAILS', collections.OrderedDict),
        ('ENUMERATIONS', collections.OrderedDict),
        ('QC_STATUS', str)
        }:
        utils.validate_field(ctx, module, field, typeof)


def _validate_sections(ctx, module):
    """Validates a module's standard attributes.

    """
    for section in {'ENUMERATIONS', 'DETAILS'}:
        if utils.validate_field(ctx, module, section, collections.OrderedDict):
            _validate_section(ctx, module, section)


def _validate_section(ctx, module, section):
    """Validates a section within a module.

    """
    for key, obj in getattr(module, section).items():
        if not isinstance(key, (str, unicode)) or \
           len(key.strip()) == 0:
            err = "{}: all keys must be strings".format(section)
            ctx.error(err)

        elif not re.match(_RE_KEY, key):
            err = "{}[{}]: all keys must be lower-case with underscore spacing".format(section, key)
            ctx.error(err)

        elif not isinstance(obj, dict):
            err = "{}[{}]: must be a dictionary".format(section, key)
            ctx.error(err)
