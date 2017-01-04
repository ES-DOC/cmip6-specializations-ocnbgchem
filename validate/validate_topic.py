"""
.. module:: validate_topic.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Validates a specialized CMIP6 scientific topic.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from utils import validate_std
from validate_property_sets import validate as validate_property_sets
from validate_enum import validate_enumerations



def validate(ctx, topic):
    """Validates a CMIP6 scientific detail topic.

    :param ValidationContext ctx: Validation contextual information.
    :param module detail_topic: A python module containing specializations.

    """
    # Set expected sections.
    sections = ['ENUMERATIONS', 'DETAILS']

    # Level-1 validation.
    validate_std(ctx, topic, sections)
    if ctx.errors[topic]:
        return

    # Level-2 validation.
    ctx.errors[topic] += \
        validate_enumerations(topic.ENUMERATIONS)
    for section in sections[1:]:
        ctx.errors[topic] += \
            validate_property_sets(topic, getattr(topic, section))
