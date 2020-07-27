.. _Output:

Output files
============

Explanation of the output files.

.. contents::
    :local:
    
.. _Output_snap:
    
".snap"
-------
Contains all the atomic information extracted from the trajectory file.

File produced by function :func:`.tra_save` while running XXX paw\_structure\_fast XXX if **SAVE** is TRUE in :ref:`Control_TRA`.

The header contains general information like the time interval and number of snapshots that have been extracted, the number of atoms in each snapshot and the unit cell matrix.

Every snapshot contains the simulation time and iteration and for every atom the internal name, species identifier, index and atomic positions from the CP-PAW code.

Lines were replaced by "..." for better visibility of the structure.

.. literalinclude:: Images/manganese.snap

.. _Output_ion:

".ion"
------
Contains all the atoms contained in an ion complex.

File produced by function :func:`.ion_save` while running XXX paw\_structure\_fast XXX if :ref:`Control_ION` block is active.

The header contains general information like the time interval and number of snapshots that have been extracted, the unit cell matrix and the parameter selected in the control file.

Every snapshot contains the simulation time, iteration and number of atoms in the complex. For those atoms the internal name, species identifier, index and atomic positions from the CP-PAW code are listed.

Lines were replaced by "..." for better visibility of the structure.

.. literalinclude:: Images/manganese.ion

.. _Output_water:

".water"
--------
Contains all the atoms contained in water complexes.

File produced by function :func:`.water_save` while running XXX paw\_structure\_fast XXX if :ref:`Control_WATER` block is active.

The header contains general information like the time interval and number of snapshots that have been extracted, the unit cell matrix and the parameter selected in the control file.

Every snapshot contains the simulation time, iteration and number of atoms in the complex. For those atoms the internal name, species identifier, index and atomic positions from the CP-PAW code are listed.

Lines were replaced by "..." for better visibility of the structure.

.. literalinclude:: Images/manganese.water
    
.. _Output_radial:

".radial"
---------
Contains values for radial distribution function and coordination number.

File produced by function :func:`.radial_save` while running XXX paw\_structure\_fast XXX if :ref:`Control_RADIAL` block is active.

The header contains general information like the time interval and number of snapshots that have been extracted, the unit cell matrix and the parameter selected in the control file.

Additionally there is the average atom density **RHO** of the species **ID2**.

The column **RDF** contains the values for the radial distribution function and **COORDINATION** for the coordination number corresponding to the radii in column **RADIUS**.

Lines were replaced by "..." for better visibility of the structure.

.. literalinclude:: Images/manganese.radial
    
.. _Output_hbonds_c:

".hbonds\_c"
------------

.. _Output_ion_out:

".ion\_out"
-----------

.. _Output_water_out:

".water\_out"
-------------

.. _Output_water_ion:

".water\_ion"
-------------

