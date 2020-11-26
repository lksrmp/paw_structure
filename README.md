# paw_structure
A Python package paw\_structure was developed to conduct a structural analysis of ab-*initio* molecular dynamics simulations performed by the CP-PAW code.

Note, that the program package is still in development and especially the documentation might be subject to change and only represents the latest stable release. No guarantee can be provided for the correctness and completeness of the project.

Installation
------------

**On Unix (Linux, OS X)**

 - clone this repository
 - `pip install ./paw_structure`
 
Dependencies and packages needed for the program are also installed or updated. Administrator privilege might be necessary depending on the system in order to obtain and install the dependencies.

Building the documentation
--------------------------

Documentation for the package is generated using Sphinx. Sphinx has the
ability to automatically inspect the signatures and documentation strings in
the extension module to generate a documentation in a variety of formats.
The following commands generate HTML-based reference documentation or a PDF document using LaTex; for other
formats please refer to the Sphinx manual:

 - `cd paw_structure/docs`
 - `make html`
 - `make latexpdf`
