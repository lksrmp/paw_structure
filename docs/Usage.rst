.. _Usage:

Usage
=====

The usage of the *paw\_structure* analysis tool is based on the command line executables::
    
    paw_structure_fast
    paw_structure_ion
    paw_structure_water
    paw_structure_radial

.. _Usage_paw_structure_fast:

paw\_structure\_fast
--------------------
Reads, extracts and analyses atomic information from the "_r.tra" trajectory file produced during the CP-PAW simulation. This process is controlled by the :ref:`control file ".scntl" <Control>`.

The routine is started inside the directory containing the input data with::

    paw_structure_fast <root>.scntl
    
This executes the module :mod:`.structure_fast` internally.

Several output files containing the raw data results from the analysis are created. For a detailed description of each see section :ref:`Output`. 

Possible output files are

.. hlist::
    :columns: 3

    - :ref:`Output_snap`
    - :ref:`Output_ion` 
    - :ref:`Output_water`
    - :ref:`Output_radial`
    - :ref:`Output_hbonds_c`
    
    
paw\_structure\_ion
-------------------
Performs further analysis of the data extracted by :ref:`Usage_paw_structure_fast` which is saved in the :ref:`Output_ion` file.

The routine is started inside the directory containing the input data with::

    paw_structure_fast [-p] <root>.ion
    
This executes the module :mod:`structure_ion` internally.
    
The number of atoms as a function of time is plotted and saved into a :ref:`Output_ion_png` file. With the optional flag **-p** the image is opened in an interactive plotting dialog.

It detects changes in the atom composition of the ion cluster and saves snapshots where these changes occur into a seperate :ref:`Output_ion_out` file. 

paw\_structure\_water
---------------------
Performs further analysis of the data extracted by :ref:`Usage_paw_structure_fast` which is saved in the :ref:`Output_water` file.

The routine is started inside the directory containing the input data with::

    paw_structure_fast [-p] [-i <root>.ion] <root>.water
    
This executes the module :mod:`structure_water` internally.

The optional flag **-i** allows the consideration of an :ref:`Output_ion` file while analysing unusual water structures. This is to ensure that the water complexes are not part of an ion cluster. 

The number of atoms as a function of time is plotted and saved into a :ref:`Output_water_png` file. With the optional flag **-p** the image is opened in an interactive plotting dialog. If no ion complex is present the total number of atoms in water complexes is plotted. If an ion complex is present, both the total number of atoms in any complex and the number of atoms only in water complexes is plotted.

It detects changes in the atom composition inside the :ref:`Output_water` file and saves snapshots where these changes occur into a seperate :ref:`Output_water_out` file.

.. Todo::
    
    Clean files of eventual ion complex contributions before change detection happens.
    
If an ion complex is present, all atoms in this complex and the water complexes are combined and written into a :ref:`Output_water_ion` file.

.. Todo::

    Change detection in ".water_ion" file as well.
    
paw\_structure\_radial
----------------------
Plotting of the radial distribution function (RDF) extracted by :ref:`Usage_paw_structure_fast` which is saved in the :ref:`Output_radial` file.

The routine is started inside the directory containing the input data with::

    paw_structure_radial [-i] <root>.radial
    
This exectures the module :mod:`structure_radial` internally.

The optional flag **-i** stands for integration and also includes the numerically integrated coordination number into the plot.

