.. _Control:

Control file ".scntl"
=====================

The control file is responsible for what data is extracted and how it is processed.

.. contents::
    :local:

.. _Control_General:

General Structure
-----------------

A block has a given structure with an opening keyword, the different options contained within it and the closing keyword **!END**::

    !SCNTL
      !BLOCK_1
        ITEM_1 VALUE_1
        ITEM_2 VALUE_2
        ITEM_3_OFF VALUE_3
      !END
      !BLOCK_2_OFF
        ITEM_1 VALUE_1
        ITEM_2 VALUE_2
      !END
    !END
    
The control file is line sensitive and only searches for keywords in the first word of each line. Therefore an item can easily be removed by changing it or appending **\_OFF** to it. The same goes for whole blocks as shown for **!BLOCK\_2** but the closing keyword still needs to be present. Note that the `!SCNTL`_ block must suround all other blocks.
   
.. _Control_Example:
   
Example for the control file ".scntl"
-------------------------------------
Following example illustrates a few options of what is available for the user. This should not be taken as a good set of parameters but rather to see how to structure the file correctly. The file could be named *manganese.scntl*.

.. literalinclude:: Images/manganese.scntl

.. _Control_SCNTL:

!SCNTL
------
General control block

Must include all other blocks.

:Rules: mandatory

.. glossary::
    ROOT
        specify project root name if different from control file
        
        WARNING: not fully tested
        
        :Type: str
        :Rules: optional
        :Default: root from control file
        
    PBC\_FOLDING
        fold atomic positions back into one unit cell to ensure sufficient periodic boundary conditions
        
        WARNING: only for cubic unit cells
        
        :Type: logical
        :Rules: optional, activate with TRUE
        :Default: FALSE

.. _Control_TRA:
        
!TRA
----

Trajectory extraction control block

:Rules: optional

.. glossary::
    T1
        starting time for snapshot extraction
        
        :Type: float 
        :Rules: mandatory
        
    T2
        end time of snapshot extraction
        
        :Type: float 
        :Rules: mandatory
        
    N
        number of snapshots
        
        :Type: int 
        :Rules: mandatory

    SAVE
        save snapshots to :ref:`Output_snap` file
        
        :Type: logical 
        :Rules: optional, activate with TRUE
        :Default: FALSE
        
    LOAD
        load snapshots from :ref:`Output_snap` file; disables selection of **T1**, **T2** and **N**
        
        :Type: logical 
        :Rules: optional, activate with TRUE
        :Default: FALSE
        
.. _Control_ION:
        
!ION
----
Ion complex detection control block

XXX REFERENCE TO ALGORITHM EXPLANATION XXX

:Rules: optional, requires `!TRA`_

.. glossary::
    ID1
        identifier for atom used as center
        
        :Type: str
        :Rules: mandatory
    
    ID2
        identifier for atoms as possible first neighbors
        
        :Type: str
        :Rules: mandatory
    
    ID3
        identifier for atoms as possible neighbors of first neighbors
        
        :Type: str
        :Rules: mandatory
    
    CUT1
        cutoff distance for first neighbor search
        
        :Type: float
        :Rules: optional
        :Default: 3.0
    
    CUT2
        cutoff distance for second neighbor search
        
        :Type: float
        :Rules: optional
        :Default: 1.4

.. _Control_WATER:
        
!WATER
------
Water complex detection control block

XXX REFERENCE TO ALGORITHM EXPLANATION XXX

:Rules: optional, requires `!TRA`_

.. glossary::
    ID1
        identifier for atoms used as center
        
        :Type: str
        :Rules: mandatory
    
    ID2
        identifier for atoms as possible neighbors
        
        :Type: str
        :Rules: mandatory
    
    CUT
        cutoff distance for neighbor search
        
        :Type: float
        :Rules: optional
        :Default: 1.4
        
.. _Control_HBONDS:

!HBONDS
-------
Hydrogen bond network control block

XXX REFERENCE TO ALGORITHM EXPLAINATION XXX

:Rules: optional, requires `!TRA`_

.. glossary::
    ID1
        identifier for oxygen atoms
        
        :Type: str
        :Rules: mandatory
        
    ID2
        identifier for hydrogen atoms
        
        :Type: str
        :Rules: mandatory
        
    CUT1
        maximum distance between two oxygen atoms
        
        :Type: float
        :Rules: optional
        :Default: 3.5
        
    CUT2
        maximum distance between an oxygen and a hydrogen atom
        
        :Type: float
        :Rules: optional
        :Default: 3.1
        
    ANGLE
        minimum O-H-O angle for a hydrogen bond in degree
        
        :Type: float
        :Rules: optional
        :Default: 140.0


.. _Control_RADIAL:

!RADIAL
-------
Radial distribution function (RDF) control block

XXX REFERENCE TO ALGORITHM EXPLANATION XXX

:Rules: optional, requires `!TRA`_ if **T1**, **T2** and **N** are not specified

.. glossary::
    ID1
        identifier for atoms used as centers
        
        :Type: str
        :Rules: mandatory
        
    ID2
        identifier for atoms as possible neighbors
        
        :Type: str
        :Rules: mandatory
        
    CUT
        cutoff distance for RDF calculation
        
        :Type: float
        :Rules: optional
        :Default: 5.0
        
    NBINS
        number radius intervals; influences resolution together with **CUT**
        
        :Type: int
        :Rules: optional
        :Default: 1000
    
    T1
        starting time for snapshot extraction; overwrites selection from `!TRA`_ if **T2** and **N** are also given
    
        :Type: float
        :Rules: optional
        
    T2
        end time for snapshot extraction; overwrites selection from `!TRA`_ if **T1** and **N** are also given
    
        :Type: float
        :Rules: optional
        
    N
        number of extracted snapshots; overwrites selection from `!TRA`_ if **T1** and **N** are also given
        
        :Type: int
        :Rules: optional
