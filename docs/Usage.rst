.. _Usage:

Usage
=====

The usage of the *paw\_structure* analysis tool is based on the command line executables::
    
    paw_structure_fast
    paw_structure_ion
    paw_structure_water
    paw_structure_radial
    paw_structure_hbonds
    paw_structure_gap
    
.. figure:: Images/workflow.png
    :width: 800
    :align: center
    :alt: workflow illustration
    :figclass: align-center

    Workflow in combination with CP-PAW.

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
    
.. _Usage_paw_structure_ion:
    
paw\_structure\_ion
-------------------
Performs further analysis of the data extracted by :ref:`Usage_paw_structure_fast` which is saved in the :ref:`Output_ion` file.

The routine is started inside the directory containing the input data with::

    paw_structure_ion [-p] [-x XMIN XMAX] [-y YMIN YMAX] ion
    
**mandatory**  

:ion: path of :ref:`Output_ion` complex file produced by :ref:`Usage_paw_structure_fast`

**optional**

:-p: show interactive graph of atom number in ion complex
:-x [XMIN XMAX]: select range for x axis of plot
:-y [YMIN YMAX]: select range for y axis of plot
    
This executes the module :mod:`.structure_ion` internally.
    
The number of atoms as a function of time is plotted and saved into the :ref:`Output_ion_png` file. It detects changes in the atom composition of the ion cluster and saves snapshots where these changes occur into a seperate :ref:`Output_ion_out` file.

Output files are

.. hlist::
    :columns: 2
    
    - :ref:`Output_ion_out`
    - :ref:`Output_ion_png`
    
.. _Usage_paw_structure_water:

paw\_structure\_water
---------------------
Performs further analysis of the data extracted by :ref:`Usage_paw_structure_fast` which is saved in the :ref:`Output_water` file.

The routine is started inside the directory containing the input data with::

    paw_structure_water [-i ION] [-p] [-x XMIN XMAX] [-y YMIN YMAX] water
    
**mandatory**  

:water: path of :ref:`Output_water` complex file produced by :ref:`Usage_paw_structure_fast`

**optional**

:-i [ION]: path of :ref:`Output_ion` complex file produced by :ref:`Usage_paw_structure_fast`
:-p: show interactive graph of atom number in water complexes
:-x [XMIN XMAX]: select range for x axis of plot
:-y [YMIN YMAX]: select range for y axis of plot
    
This executes the module :mod:`.structure_water` internally.

The optional flag **-i** allows the consideration of an :ref:`Output_ion` file while analysing unusual water structures. This is to ensure that the water complexes are not part of an ion cluster. 

The number of atoms as a function of time is plotted and saved to a file. If no ion complex is present the total number of atoms in water complexes is plotted. If an ion complex is present, both the total number of atoms in any complex and the number of atoms only in water complexes is plotted.

It detects changes in the atom composition inside the :ref:`Output_water` file and saves snapshots where these changes occur into a seperate :ref:`Output_water_out` file.

If an ion complex is present, all atoms in this complex and the water complexes are combined and written into a :ref:`Output_water_ion` file.

Output files are

.. hlist::
    :columns: 3
    
    - :ref:`Output_water_out`
    - :ref:`Output_water_png`
    - :ref:`Output_water_ion`

.. Todo::
    
    Clean files of eventual ion complex contributions before change detection happens.

    Change detection in :ref:`Output_water_ion` file as well.
    
.. _Usage_paw_structure_radial:
    
paw\_structure\_radial
----------------------
Plotting of the radial distribution function (RDF) extracted by :ref:`Usage_paw_structure_fast` which is saved in the :ref:`Output_radial` file.

The routine is started inside the directory containing the input data with::

    paw_structure_radial [-i] [-fwhm] [-p] [-x XMIN XMAX] [-y YMIN YMAX] radial
    
**mandatory**  

:radial: path of :ref:`Output_radial` complex file produced by :ref:`Usage_paw_structure_fast`

**optional**

:-i: integrate RDF to obtain the coordination number
:-fwhm: peak detection and analysis
:-p: show interactive graph of radial distribution function
:-x [XMIN XMAX]: select range for x axis of plot
:-y [YMIN YMAX]: select range for y axis of plot
    
This exectures the module :mod:`.structure_radial` internally.

The radial distribution function is integrated numerically according to XXXSCHEMEXXX in oder to obtain the coordination number.

The peak detection is performed using XXXSCIPYXXX DESCRIBE HOW IT WORKS AND WHAT OUTPUT MEANS.

Output files are

.. hlist::
    :columns: 1
    
    - :ref:`Output_radial_png`
    
.. Todo::

    Additional output of peak detection into file. At the moment only printed into console.
    
    Describe determination of RDF and coordination number mathematically.
    
    Details on peak detection using :py:mod:`scipy`.
    
.. _Usage_paw_structure_hbonds:

paw\_structure\_hbonds
----------------------
ADD HBONDS COMMANDS

.. _Usage_paw_structure_gap:

paw\_structure\_gap
-------------------
Plotting of the energy gap and the HOMO/LUMO energy taken from the CP-PAW protocol file ".prot".

The routine is started inside the directory containing the input data with::

    paw_structure_gap [-p] [-x XMIN XMAX] [-y1 YMIN1 YMAX1] [-y2 YMIN2 YMAX2] prot
    
**mandatory**

:prot: path of ".prot" file produced by CP-PAW code

**optional**

:-p: show interactive graph of the energies
:-x XMIN XMAX: select range for x axis of plot
:-y1 YMIN1 YMAX1: select range for y1 axis of plot (energy gap)
:-y2 YMIN2 YMAX2: select range for y2 axis of plot (HOMO/LUMO energy)

This executes the module :mod:`.structure_gap` internally.

The three different energies are plotted as a function of simulation time with HOMO/LUMO energies sharing a y axis.

Output files are

.. hlist::
    :columns: 1
    
    - :ref:`Output_gap_png`

.. Todo::

    Implement removal of doubled simulation times similar to :func:`.tra_clean`.
    
    Implement check if energy gap is even present in protocol file (variable occupations).
