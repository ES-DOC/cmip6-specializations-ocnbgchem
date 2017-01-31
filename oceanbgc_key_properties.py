"""A realm key-properties specialization.

For further information goto http://wordpress.es-doc.org/cmip6-model-specializations.

"""
# --------------------------------------------------------------------
# INTERNAL (do not change)
# --------------------------------------------------------------------
from collections import OrderedDict

DETAILS = OrderedDict()
ENUMERATIONS = OrderedDict()

# --------------------------------------------------------------------
# CONTACT: Set to realm specialization co-ordinator.
# --------------------------------------------------------------------
CONTACT = 'Eric Guilyardi'

# --------------------------------------------------------------------
# AUTHORS: Set to realm specialization authors (comma delimited).
# --------------------------------------------------------------------
AUTHORS = 'Eric Guilyardi'

# --------------------------------------------------------------------
# QUALITY CONTROL STATUS: Set to 'draft' or 'complete'
# --------------------------------------------------------------------
QC_STATUS = 'draft'

# --------------------------------------------------------------------
# DESCRIPTION: Short description of the specialization.
# --------------------------------------------------------------------
DESCRIPTION = 'Ocean Biogeochemistry key properties'

# --------------------------------------------------------------------
# KEY PROPERTIES: top level
# --------------------------------------------------------------------
DETAILS['toplevel'] = {
    'description': 'General key properties in ocean biogeochemistry',
    'properties': [
        ('model_name', 'str', '1.1',
            'Name of ocean biogeochemistry model code (PISCES 2.0,...)'),
        ('model_family', 'str', '1.1',
            'Type of ocean biogeochemistry model'),
        ('basic_approximations', 'str', '1.1',
            'Basic approximations made in the ocean biogeochemistry',),
        ('prognostic_variables', 'str', '1.N',
            'List of prognostic variables in the ocean biogeochemistry component'),
        ('damping', 'str', '0.1',
            'Describe any tracer damping used'),
        ]
    }

# --------------------------------------------------------------------
# KEY PROPERTIES: details
# --------------------------------------------------------------------

DETAILS['Time_stepping_framework'] = {
    'description': 'Time stepping framework for ocean biogeochemistry',
    'properties' : [
        ]
    }

DETAILS['Time_stepping_framework:passive_tracers_transport'] = {
    'description': 'Time stepping method for passive tracers transport in ocean biogeochemistry',
    'properties' : [
        ('method', 'ENUM:passive_tracers_transport', '1.1',
            'Time stepping framework for passive tracers'),
        ('timestep_if_not_from_ocean', 'int', '0.1',
            'Time step for passive tracers (if different from ocean)'),
        ]
    }

DETAILS['Time_stepping_framework:biology_sources_sinks'] = {
    'description': 'Time stepping framework for biology sources and sinks in ocean biogeochemistry',
    'properties' : [
        ('method', 'ENUM:passive_tracers_transport', '1.1',
            'Time stepping framework for biology sources and sinks'),
        ('timestep_if_not_from_ocean', 'int', '0.1',
            'Time step for biology sources and sinks (if different from ocean)'),
        ]
    }

DETAILS['Transport_scheme'] = {
    'description': 'Transport scheme in ocean biogeochemistry',
    'properties' : [
        ('type', 'ENUM:transport_types', '1.1',
            'Type of transport scheme'),
        ('scheme', 'ENUM:transport_scheme', '1.1',
            'Transport scheme used'),
        ('use_different_scheme', 'str', '0.1',
            'Decribe transport scheme if different than that of ocean model'),
        ]
    }

DETAILS['Boundary_forcing'] = {
    'description': 'Properties of biogeochemistry boundary forcing',
    'properties': [
        ('atmospheric_deposition', 'ENUM:sources_atmos_deposition', '1.1',
            'Describe how atmospheric deposition is modeled'),
        ('river_input', 'ENUM:sources_river_input', '1.1',
            'Describe how river input is modeled'),
        ('sediments_from_boundary_conditions', 'str', '0.1',
            'List which sediments are speficied from boundary condition'),
        ('sediments_from_explicit_model', 'str', '0.1',
            'List which sediments are speficied from explicit sediment model'),
        ]
    }

DETAILS['Gas_exchange'] = {
    'description': 'Properties of gas exchange in ocean biogeochemistry ',
    'properties': [
        ('CO2_exchange_present', 'bool', '1.1',
            'Is CO2 gas exchange modeled ?'),
        ('CO2_exchange_type', 'ENUM:gas_exchange_types', '0.1',
            'Describe CO2 gas exchange'),
        ('O2_exchange_present', 'bool', '1.1',
            'Is O2 gas exchange modeled ?'),
        ('O2_exchange_type', 'ENUM:gas_exchange_types', '0.1',
            'Describe O2 gas exchange'),
        ('DMS_exchange_present', 'bool', '1.1',
            'Is DMS gas exchange modeled ?'),
        ('DMS_exchange_type', 'str', '0.1',
            'Specify DMS gas exchange scheme type'),
        ('N2_exchange_present', 'bool', '1.1',
            'Is N2 gas exchange modeled ?'),
        ('N2_exchange_type', 'str', '0.1',
            'Specify N2 gas exchange scheme type'),
        ('N2O_exchange_present', 'bool', '1.1',
            'Is N2O gas exchange modeled ?'),
        ('N2O_exchange_type', 'str', '0.1',
            'Specify N2O gas exchange scheme type'),
        ('CO_exchange_present', 'bool', '1.1',
            'Is CO gas exchange modeled ?'),
        ('CO_exchange_type', 'str', '0.1',
            'Specify CO gas exchange scheme type'),
        ('other_gases', 'str', '0.1',
            'Specify any other gas exchange'),
        ]
    }

DETAILS['Carbon_chemistry'] = {
    'description': 'Properties of carbon chemistry biogeochemistry',
    'properties': [
        ('type', 'ENUM:carbon_chemistry', '1.1',
            'Describe how carbon chemistry is modeled'),
        ('pH_scale', 'ENUM:ph_scale', '0.1',
            'If NOT OMIP protocol, describe pH scale.'),
        ('constants_if_not_OMIP', 'str', '0.1',
            'If NOT OMIP protocol, list carbon chemistry constants.'),
        ]
    }


# --------------------------------------------------------------------
# KEY PROPERTIES: ENUMERATIONS
# --------------------------------------------------------------------
ENUMERATIONS['passive_tracers_transport'] = {
    'description': 'Types of time stepping framework for passive tracers ocean biogeochemistry',
    'is_open': False,
    'members': [
        ('use ocean model transport time step', None),
        ('use specific time step', None),
        ]
    }

ENUMERATIONS['transport_types'] = {
    'description': 'Types of transport in ocean biogeochemistry',
    'is_open': False,
    'members': [
        ('Offline', None),
        ('Online', None),
        ]
    }

ENUMERATIONS['transport_scheme'] = {
    'description': 'Types of transport in ocean biogeochemistry',
    'is_open': True,
    'members': [
        ('Use that of ocean model', None),
        ]
    }

ENUMERATIONS['sources_atmos_deposition'] = {
    'description': 'Type of atmospheric deposition in ocean biogeochemistry',
    'is_open': False,
    'members': [
        ('from file', None),
        ('from Atmospheric Chemistry model', None),
        ]
    }

ENUMERATIONS['sources_river_input'] = {
    'description': 'Type of river input in ocean biogeochemistry',
    'is_open': False,
    'members': [
        ('from file', None),
        ('from Land Surface model', None),
        ]
    }

ENUMERATIONS['gas_exchange_types'] = {
    'description': 'Type of gas exchange in ocean biogeochemistry',
    'is_open': True,
    'members': [
        ('OMIP protocol', None),
        ]
    }

ENUMERATIONS['carbon_chemistry'] = {
    'description': 'Type of carbon chemistry in ocean biogeochemistry',
    'is_open': False,
    'members': [
        ('OMIP protocol', None),
        ('Other protocol', None),
        ]
    }

ENUMERATIONS['ph_scale'] = {
    'description': 'Type of carbon chemistry pH scale in ocean biogeochemistry',
    'is_open': True,
    'members': [
        ('Sea water', None),
        ('Free', None),
        ]
    }


