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
		"category",
		"citations",
		"description",
		"key_properties",
		"name",
		"long_name",
		"processes",
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
	   "citations",
	   "keywords",
	   "overview"
	],
	"exclude": []
}

# science.process constraints.
CIM_PROFILE["science.process"] = {
	"include": [
	   "citations",
	   "keywords",
	   "overview"
	],
	"exclude": []
}

# science.sub_process constraints.
CIM_PROFILE["science.sub_process"] = {
	"include": [
	   "citations",
	   "keywords",
	   "overview"
	],
	"exclude": []
}

# science.key_properties constraints.
CIM_PROFILE["science.key_properties"] = {
	"include": [
	   "citations",
	   "keywords",
	],
	"exclude": [
		"extent",
		"extra_conservation_properties",
		"implementation_overview",
		"keywords",
		"resolution",
		"tuning_applied"
	]
}

# science.model[ocean].key_properties constraints.
CIM_PROFILE["science.realm[ocean].key_properties"] = {
	"include": [
		"citations",
		"detail_sets",
		"description"
		"extra_conservation_properties",
		"keywords",
		"resolution",
		"short_name",
		"sub_processes",
		"tuning_applied"
	],
	"exclude": [
		"extent",
		"implementation_overview",
		"keywords",
	]
}
