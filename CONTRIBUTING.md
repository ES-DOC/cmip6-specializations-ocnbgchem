# Contributing to the CMIP6 specializations	

Dear ES-DOC community member,

Thank you for taking the time to consider making a contribution to the
CMIP6 specializations.

This set of guidelines provides a overview of the practices and
procedures that should be used in fixing, updating, or adding to the
CMIP6 specializations

The ES-DOC community takes great pride in respectful and collegial
discourse. Any disrespectful or otherwise derogatory communication
will not be tolerated.

## General Guidelines

* All changes must be logged in the specialization request
  spreadsheet:
  https://docs.google.com/spreadsheets/d/1h1UQEGEBBbmM0Xs3E6ZVbS-5f7Vdiq1tT7e6tUAI4Nw/edit#gid=1921196076

* All changes to the specializations will be in the form of Pull
  Requests (not Issues nor direct commits to the master branch).

* Pull requests can be made at any time, but they will not be merged
  until a public release of the specializations for all 9 realm
  specializations is due (which is envisaged every ~6 months or longer
  during the CMIP6 project).
  
* Multiple changes by the same person should be made by updates to a single pull request. This is to simplify the subsequent merge procedure.

* When a public release is due, the Pull Requests will be merged into
  the master branch, ready to be used by downstream tools (such as the
  spreadsheet generator).

## Version strategy for the CMIP6 specializations

Each individual specialization uses an internal three-level
**major.minor.trivial** numeric version scheme, e.g 1.0.4, that is
independent of other specializations. This version is stored in the
[realm].py file.

Public releases are defined by GitHub tags that are consistent across
all specializations an use a **major.minor** numeric version scheme,
e.g 1.1

