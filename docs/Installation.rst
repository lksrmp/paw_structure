.. _Installation:

Installation
============

The package is only tested on **Linux** and **OS X** so far.

**Clone** repository (WARNING: currently private so does not work)::

    git clone https://github.com/lksrmp/paw_structure

**Install** package by executing in directory containing distribution folder *paw\_structure*::

    pip install ./paw_structure
    
Dependencies and packages needed for the program are also installed or updated. Administrator privilege might be necessary depending on the system in order to obtain and install the dependencies.

**Import** package *paw\_structure* in Python with

.. code-block::

    import paw_structure
    
It can be used as a normal Python package and all the internal functions mentioned in the :ref:`Documentation` are accessible.
    
**Executables** are installed for easy access from the command line::

    paw_structure_fast
    paw_structure_ion
    paw_structure_water
    paw_structure_radial
    paw_structure_hbonds
    paw_structure_gap
    
**Documentation** can be build in different ways using::

    cd paw_structure/docs
    make html
    make singlehtml
    make latexpdf
    
The output can be found in the corresponding folder in the directory *paw\_structure/docs/\_build*:

    :*html*: creates interactive documentation with different html files linking to each other (main file *index.html*)
    
    :*singlehtml*: creates interactive documentation with a single html file (*index.html*)
    
    :*latexpdf*: creates pdf version of the documentation
    
For the necessary arguments and the functionality look in section :ref:`Usage`.
    


