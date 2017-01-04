# -*- coding: utf-8 -*-

"""
.. module:: cim_profile.py
   :platform: Unix, Windows
   :synopsis: Set of CIM constraints pertinent to CMIP6.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from collections import OrderedDict



# Declare profile over CIM v2.
CIM_PROFILE = OrderedDict()

# science.model constraints.
CIM_PROFILE["science.model"] = {
    "include": [
        "canonical_id",
        "citations",
        "description",
        "key_properties",
        "long_name",
        "model_type",
        "name",
        "realms",
        "version"
    ],
    "exclude": [
        "coupled_components",
        "coupler",
        "development_history",
        "development_path",
        "internal_software_components",
        "release_date”",
        "repository",
    ]
}

# science.realm constraints.
CIM_PROFILE["science.realm"] = {
    "include": [
        "canonical_name",
        "citations",
        "keywords",
        "overview",
        "responsible_parties"
    ],
    "exclude": []
}

# science.topic constraints.
CIM_PROFILE["science.topic"] = {
    "include": [
        "citations",
        "keywords",
        "overview",
        "responsible_parties"
    ],
    "exclude": []
}
