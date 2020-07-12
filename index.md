[paw\_structure](#)

0.0.1

-   [Introduction](index.html#document-Introduction)
-   [Installation](index.html#document-Installation)
-   [Documentation](index.html#document-Documentation)
    -   [paw\_structure.utility](index.html#document-Modules/paw_structure.utility)
    -   [paw\_structure.pbc](index.html#document-Modules/paw_structure.pbc)
    -   [paw\_structure.neighbor](index.html#document-Modules/paw_structure.neighbor)
    -   [paw\_structure.scntl](index.html#document-Modules/paw_structure.scntl)
    -   [paw\_structure.ion](index.html#document-Modules/paw_structure.ion)
    -   [paw\_structure.tra](index.html#document-Modules/paw_structure.tra)
    -   [paw\_structure.water](index.html#document-Modules/paw_structure.water)
    -   [paw\_structure.radial](index.html#document-Modules/paw_structure.radial)
    -   [paw\_structure.hbonds\_c](index.html#document-Modules/paw_structure.hbonds_c)
    -   [paw\_structure.radial\_c](index.html#document-Modules/paw_structure.radial_c)

** [paw\_structure](#)

-   [](#) »
-   paw\_structure Documentation
-   

* * * * *

paw\_structure Documentation[¶](#paw-structure-documentation "Permalink to this headline")
==========================================================================================

Introduction[¶](#introduction "Permalink to this headline")
-----------------------------------------------------------

Here is a bit of text motivation and describing the project.

Installation[¶](#installation "Permalink to this headline")
-----------------------------------------------------------

Here are the steps in order to install and manage everything.

Documentation[¶](#documentation "Permalink to this headline")
-------------------------------------------------------------

Here is the documentation of the program.

### paw\_structure.utility[¶](#paw-structure-utility "Permalink to this headline")

Error and input handling.

Dependencies: [`argparse`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/argparse.html#module-argparse "(in Python v3.8)")
[`sys`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/sys.html#module-sys "(in Python v3.8)")
[`time`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/time.html#module-time "(in Python v3.8)")

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------
  [`argcheck`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.utility.argcheck "paw_structure.utility.argcheck")(argv, extension)                           Checks console input and arguments.
  [`err`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.utility.err "paw_structure.utility.err")(func, id, arg[, info])                                    Raise specific errors for internal checks.
  [`err_file`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.utility.err_file "paw_structure.utility.err_file")(func, path)                                Terminate program if error during file opening.
  [`structure_ion_input`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.utility.structure_ion_input "paw_structure.utility.structure_ion_input")()         Get console input for `structure_ion`{.xref .py .py-mod .docutils .literal .notranslate}.
  [`structure_water_input`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.utility.structure_water_input "paw_structure.utility.structure_water_input")()   Get console input for `structure_ion`{.xref .py .py-mod .docutils .literal .notranslate}.
  [`timing`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.utility.timing "paw_structure.utility.timing")(f)                                               Time of execution for a function.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------

 `paw_structure.utility.`{.sig-prename .descclassname}`argcheck`{.sig-name .descname}(*argv*, *extension*)[¶](#paw_structure.utility.argcheck "Permalink to this definition")
:   Checks console input and arguments.

    Parameters
    :   -   **argv**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]*)
            – two element list with arguments being extracted with
            `sys.argv()`{.xref .py .py-func .docutils .literal
            .notranslate}

        -   **extension**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – expected extension of second argument (e.g. ‘.ion’,
            ‘.water’, ‘.hbonds’)

    Returns
    :   name with extension removed

    Return type
    :   [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")

    Calls [`utility.err()`{.xref .py .py-func .docutils .literal
    .notranslate}](#paw_structure.utility.err "paw_structure.utility.err")
    in case of wrong input.

 `paw_structure.utility.`{.sig-prename .descclassname}`err`{.sig-name .descname}(*func*, *id*, *arg*, *info=''*)[¶](#paw_structure.utility.err "Permalink to this definition")
:   Raise specific errors for internal checks.

    With `func`{.xref .py .py-data .docutils .literal .notranslate} and
    `id`{.xref .py .py-data .docutils .literal .notranslate} a
    dictionary of error functions is accessed.

    Parameters
    :   -   **func**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – name of function in which error occured

        -   **id**
            ([*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)"))
            – number of dictionary entry for function `func`{.xref .py
            .py-data .docutils .literal .notranslate}

        -   **arg**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)"))
            – list of arguments specific for each error (can vary in
            length and type)

        -   **info**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*,**optional*)
            – text displayed in error message

    Returns
    :   [`sys.exit()`{.xref .py .py-func .docutils .literal
        .notranslate}](https://docs.python.org/3/library/sys.html#sys.exit "(in Python v3.8)")
        displaying an error message

 `paw_structure.utility.`{.sig-prename .descclassname}`err_file`{.sig-name .descname}(*func*, *path*)[¶](#paw_structure.utility.err_file "Permalink to this definition")
:   Terminate program if error during file opening.

    Parameters
    :   -   **func**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – name of function in which error occured

        -   **path**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – path of file where opening failed

    Returns
    :   

        [`sys.exit()`{.xref .py .py-func .docutils .literal
        .notranslate}](https://docs.python.org/3/library/sys.html#sys.exit "(in Python v3.8)")
        displaying an error message:

            PROGRAM TERMINATED
            ERROR IN FUNCTION: <func>

            COULD NOT OPEN FILE
            <path>

 `paw_structure.utility.`{.sig-prename .descclassname}`structure_ion_input`{.sig-name .descname}()[¶](#paw_structure.utility.structure_ion_input "Permalink to this definition")
:   Get console input for `structure_ion`{.xref .py .py-mod .docutils
    .literal .notranslate}.

    Returns
    :   [`argparse`{.xref .py .py-mod .docutils .literal
        .notranslate}](https://docs.python.org/3/library/argparse.html#module-argparse "(in Python v3.8)")
        object

 `paw_structure.utility.`{.sig-prename .descclassname}`structure_water_input`{.sig-name .descname}()[¶](#paw_structure.utility.structure_water_input "Permalink to this definition")
:   Get console input for `structure_ion`{.xref .py .py-mod .docutils
    .literal .notranslate}.

    Returns
    :   [`argparse`{.xref .py .py-mod .docutils .literal
        .notranslate}](https://docs.python.org/3/library/argparse.html#module-argparse "(in Python v3.8)")
        object

 `paw_structure.utility.`{.sig-prename .descclassname}`timing`{.sig-name .descname}(*f*)[¶](#paw_structure.utility.timing "Permalink to this definition")
:   Time of execution for a function.

    Use as decorator:

        @timing
        def function():
            #code

### paw\_structure.pbc[¶](#paw-structure-pbc "Permalink to this headline")

Functions for application of periodic boundary conditions.

Dependencies: [`utility`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.utility "paw_structure.utility")
[`copy`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/copy.html#module-copy "(in Python v3.8)")
`numpy`{.xref .py .py-mod .docutils .literal .notranslate}

  ---------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------
  [`pbc_apply3x3`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.pbc.pbc_apply3x3 "paw_structure.pbc.pbc_apply3x3")(snap[, id, names])   Create 3x3 supercell.
  [`pbc_folding`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.pbc.pbc_folding "paw_structure.pbc.pbc_folding")(snapshots)              Folding of atoms into a single unit cell.
  [`pbc_general`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.pbc.pbc_general "paw_structure.pbc.pbc_general")(snap, directions)       Apply general periodic boundary conditions.
  ---------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------

 `paw_structure.pbc.`{.sig-prename .descclassname}`pbc_apply3x3`{.sig-name .descname}(*snap*, *id=None*, *names=None*)[¶](#paw_structure.pbc.pbc_apply3x3 "Permalink to this definition")
:   Create 3x3 supercell.

    Parameters
    :   -   **snap** ([`Snap`{.xref .py .py-class .docutils .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap"))
            – single snapshot containing the initial atomic positions

        -   **id**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**,**optional*)
            – list of identifiers of selected atom species (e.g.
            “[O\_](#id1)” or “[H\_](#id3)”)

        -   **names**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**,**optional*)
            – list of names of selected atoms (e.g. “O\_43” or “H\_15”)

    Takes all atoms if `id`{.xref .py .py-data .docutils .literal
    .notranslate} and `names`{.xref .py .py-data .docutils .literal
    .notranslate} is not given.

    Returns
    :   snapshot with atomic positions of a 3x3 supercell

    Return type
    :   [`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")

    Is used to apply periodic boundary conditions when for example
    searching for atomic neighbors (see e.g. [`neighbor`{.xref .py
    .py-mod .docutils .literal
    .notranslate}](index.html#module-paw_structure.neighbor "paw_structure.neighbor")).
    Original unit cell is in the middle.

    Note

    Implement creation of smaller super cell that still garantees
    periodic boundary conditions.

 `paw_structure.pbc.`{.sig-prename .descclassname}`pbc_folding`{.sig-name .descname}(*snapshots*)[¶](#paw_structure.pbc.pbc_folding "Permalink to this definition")
:   Folding of atoms into a single unit cell.

    Parameters
    :   **snapshots** (list[[`Snap`{.xref .py .py-class .docutils
        .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")])
        – list of Snap objects of which the atomic positions should be
        adjusted

    During AIMD simulations atoms can move outside of the initial unit
    cell. For easier calculation and later analysis it is advised to
    project them into a common unit cell.

    The origin is at (0,0,0).

    Note

    Only works for cubic unit cells. Directly operates and alters the
    atomic positions.

 `paw_structure.pbc.`{.sig-prename .descclassname}`pbc_general`{.sig-name .descname}(*snap*, *directions*)[¶](#paw_structure.pbc.pbc_general "Permalink to this definition")
:   Apply general periodic boundary conditions.

    Parameters
    :   -   **snap** ([`Snap`{.xref .py .py-class .docutils .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap"))
            –

        -   **directions**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            –

    Returns
    :   snapshot with periodic boundary conditions applied to atomic
        positions

    Return type
    :   [`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")

    Original unit cell is at the corner of the supercell.

### paw\_structure.neighbor[¶](#paw-structure-neighbor "Permalink to this headline")

Helper functions for atomic neighbor search.

Dependencies: `numpy`{.xref .py .py-mod .docutils .literal .notranslate}
[`pbc`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.pbc "paw_structure.pbc")

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------
  [`neighbor_find`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.neighbor.neighbor_find "paw_structure.neighbor.neighbor_find")(snap, id1, id2, cut[, names])                   param snap
                                                                                                                                                                                                     :   
                                                                                                                                                                                                     
                                                                                                                                                                                                     

  [`neighbor_find_name`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.neighbor.neighbor_find_name "paw_structure.neighbor.neighbor_find_name")(snap, id1, id2, cut[, names])    param snap
                                                                                                                                                                                                     :   
                                                                                                                                                                                                     
                                                                                                                                                                                                     

  [`neighbor_single`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.neighbor.neighbor_single "paw_structure.neighbor.neighbor_single")(center, pbc\_atoms, cut)                  param center
                                                                                                                                                                                                     :   
                                                                                                                                                                                                     
                                                                                                                                                                                                     

  [`neighbor_single_name`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.neighbor.neighbor_single_name "paw_structure.neighbor.neighbor_single_name")(center, pbc\_atoms, cut)   Find names of neighbor atoms
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------

 `paw_structure.neighbor.`{.sig-prename .descclassname}`neighbor_find`{.sig-name .descname}(*snap*, *id1*, *id2*, *cut*, *names=None*)[¶](#paw_structure.neighbor.neighbor_find "Permalink to this definition")
:   Parameters
    :   -   **snap** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **names** –

    Returns:

 `paw_structure.neighbor.`{.sig-prename .descclassname}`neighbor_find_name`{.sig-name .descname}(*snap*, *id1*, *id2*, *cut*, *names=None*)[¶](#paw_structure.neighbor.neighbor_find_name "Permalink to this definition")
:   Parameters
    :   -   **snap** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **names** –

    Returns:

 `paw_structure.neighbor.`{.sig-prename .descclassname}`neighbor_single`{.sig-name .descname}(*center*, *pbc\_atoms*, *cut*)[¶](#paw_structure.neighbor.neighbor_single "Permalink to this definition")
:   Parameters
    :   -   **center** –

        -   **pbc\_atoms** –

        -   **cut** –

    Returns:

 `paw_structure.neighbor.`{.sig-prename .descclassname}`neighbor_single_name`{.sig-name .descname}(*center*, *pbc\_atoms*, *cut*)[¶](#paw_structure.neighbor.neighbor_single_name "Permalink to this definition")
:   Find names of neighbor atoms

    Parameters
    :   -   **center** (*pandas DataFrame*) – central atom of reference

        -   **pbc\_atoms** (*pandas DataFrame*) – atoms as possible
            neighbors

        -   **cut**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for search

    Returns
    :   list of names as strings

### paw\_structure.scntl[¶](#paw-structure-scntl "Permalink to this headline")

Read control input file for `structure_fast`{.xref .py .py-mod .docutils
.literal .notranslate}.

Main routine is [`scntl_read()`{.xref .py .py-func .docutils .literal
.notranslate}](#paw_structure.scntl.scntl_read "paw_structure.scntl.scntl_read").

Dependencies: [`utility`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.utility "paw_structure.utility")
[`os`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/os.html#module-os "(in Python v3.8)")

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------
  [`scntl_read`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read "paw_structure.scntl.scntl_read")(root)                                  Read and interpret the control file \<root\>.scntl.
  [`scntl_read_hbonds`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read_hbonds "paw_structure.scntl.scntl_read_hbonds")(text, idx)        Interpret the control block for `hbonds`{.xref .py .py-mod .docutils .literal .notranslate}.
  [`scntl_read_ion`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read_ion "paw_structure.scntl.scntl_read_ion")(text, idx)                 Interpret the control block for [`ion`{.xref .py .py-mod .docutils .literal .notranslate}](index.html#module-paw_structure.ion "paw_structure.ion").
  [`scntl_read_radial`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read_radial "paw_structure.scntl.scntl_read_radial")(text, idx)        Interpret the control block for [`radial`{.xref .py .py-mod .docutils .literal .notranslate}](index.html#module-paw_structure.radial "paw_structure.radial").
  [`scntl_read_scntl`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read_scntl "paw_structure.scntl.scntl_read_scntl")(text, idx, delete)   Interpret the control block for general information.
  [`scntl_read_tra`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read_tra "paw_structure.scntl.scntl_read_tra")(text, idx)                 Interpret the control block for [`tra`{.xref .py .py-mod .docutils .literal .notranslate}](index.html#module-paw_structure.tra "paw_structure.tra").
  [`scntl_read_water`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_read_water "paw_structure.scntl.scntl_read_water")(text, idx)           Interpret the control block for [`water`{.xref .py .py-mod .docutils .literal .notranslate}](index.html#module-paw_structure.water "paw_structure.water").
  [`scntl_text`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.scntl.scntl_text "paw_structure.scntl.scntl_text")(root[, ext])                           Read text from `root`{.xref .py .py-data .docutils .literal .notranslate}.scntl file and identify different control blocks.
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read`{.sig-name .descname}(*root*)[¶](#paw_structure.scntl.scntl_read "Permalink to this definition")
:   Read and interpret the control file \<root\>.scntl.

    Parameters
    :   **root**
        ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
        – root name for the control file

    Returns
    :   dictionary of all dictionaries obtained from all the control
        blocks

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")[[dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")]

    Note

    Error checking with !TRA and !RADIAL does not work properly.

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read_hbonds`{.sig-name .descname}(*text*, *idx*)[¶](#paw_structure.scntl.scntl_read_hbonds "Permalink to this definition")
:   Interpret the control block for `hbonds`{.xref .py .py-mod .docutils
    .literal .notranslate}.

    Parameters
    :   -   **text**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**]*)
            – text from the control file; each line is a list of words
            within the outer list

        -   **idx**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            – list with two indices marking beginning and end of control
            block

    Returns
    :   dictionary containing all information obtained from the control
        block

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read_ion`{.sig-name .descname}(*text*, *idx*)[¶](#paw_structure.scntl.scntl_read_ion "Permalink to this definition")
:   Interpret the control block for [`ion`{.xref .py .py-mod .docutils
    .literal
    .notranslate}](index.html#module-paw_structure.ion "paw_structure.ion").

    Parameters
    :   -   **text**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**]*)
            – text from the control file; each line is a list of words
            within the outer list

        -   **idx**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            – list with two indices marking beginning and end of control
            block

    Returns
    :   dictionary containing all information obtained from the control
        block

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read_radial`{.sig-name .descname}(*text*, *idx*)[¶](#paw_structure.scntl.scntl_read_radial "Permalink to this definition")
:   Interpret the control block for [`radial`{.xref .py .py-mod
    .docutils .literal
    .notranslate}](index.html#module-paw_structure.radial "paw_structure.radial").

    Parameters
    :   -   **text**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**]*)
            – text from the control file; each line is a list of words
            within the outer list

        -   **idx**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            – list with two indices marking beginning and end of control
            block

    Returns
    :   dictionary containing all information obtained from the control
        block

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")

    Note

    Implement name identification for central atoms.

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read_scntl`{.sig-name .descname}(*text*, *idx*, *delete*)[¶](#paw_structure.scntl.scntl_read_scntl "Permalink to this definition")
:   Interpret the control block for general information.

    Parameters
    :   -   **text**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**]*)
            – text from the control file; each line is a list of words
            within the outer list

        -   **idx**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            – list with two indices marking beginning and end of control
            block

    Returns
    :   dictionary containing all information obtained from the control
        block

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read_tra`{.sig-name .descname}(*text*, *idx*)[¶](#paw_structure.scntl.scntl_read_tra "Permalink to this definition")
:   Interpret the control block for [`tra`{.xref .py .py-mod .docutils
    .literal
    .notranslate}](index.html#module-paw_structure.tra "paw_structure.tra").

    Parameters
    :   -   **text**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**]*)
            – text from the control file; each line is a list of words
            within the outer list

        -   **idx**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            – list with two indices marking beginning and end of control
            block

    Returns
    :   dictionary containing all information obtained from the control
        block

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_read_water`{.sig-name .descname}(*text*, *idx*)[¶](#paw_structure.scntl.scntl_read_water "Permalink to this definition")
:   Interpret the control block for [`water`{.xref .py .py-mod .docutils
    .literal
    .notranslate}](index.html#module-paw_structure.water "paw_structure.water").

    Parameters
    :   -   **text**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*]**]*)
            – text from the control file; each line is a list of words
            within the outer list

        -   **idx**
            ([*list*](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")*[*[*int*](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*]*)
            – list with two indices marking beginning and end of control
            block

    Returns
    :   dictionary containing all information obtained from the control
        block

    Return type
    :   [dict](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.8)")

 `paw_structure.scntl.`{.sig-prename .descclassname}`scntl_text`{.sig-name .descname}(*root*, *ext='.scntl'*)[¶](#paw_structure.scntl.scntl_text "Permalink to this definition")
:   Read text from `root`{.xref .py .py-data .docutils .literal
    .notranslate}.scntl file and identify different control blocks.

    XXX REFERENCE TO CONTROL FILE STRUCTURE XXX

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name for the control file

        -   **ext**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*,**optional*)
            – Default “.scntl”. DO NOT USE!

    Returns
    :   text from the control file; each line is a list of words within
        the outer list dict: dictionary with control blocks and their
        position within the text

    Return type
    :   [list](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")[[list](https://docs.python.org/3/library/stdtypes.html#list "(in Python v3.8)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")]]

    Note

    Remove forced line structure (flatten text and search for key
    words).

    Implement variable extension.

### paw\_structure.ion[¶](#paw-structure-ion "Permalink to this headline")

Ion complex detection.

Main routine is [`ion_find_parallel()`{.xref .py .py-func .docutils
.literal
.notranslate}](#paw_structure.ion.ion_find_parallel "paw_structure.ion.ion_find_parallel").

Dependencies: [`functools`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/functools.html#module-functools "(in Python v3.8)")
`miniutils`{.xref .py .py-mod .docutils .literal .notranslate}
`numpy`{.xref .py .py-mod .docutils .literal .notranslate}
`pandas`{.xref .py .py-mod .docutils .literal .notranslate}
[`neighbor`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.neighbor "paw_structure.neighbor")
[`utility`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.utility "paw_structure.utility")
[`Snap`{.xref .py .py-class .docutils .literal
.notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------
  [`ion_find_parallel`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.ion.ion_find_parallel "paw_structure.ion.ion_find_parallel")(root, snapshots, id1, id2, …)   Find ion complexes for multiple snapshots of atomic configurations.
  [`ion_find_wrapper`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.ion.ion_find_wrapper "paw_structure.ion.ion_find_wrapper")(snap, id1, id2, id3, cut1, cut2)   Wrapper for [`ion_single()`{.xref .py .py-func .docutils .literal .notranslate}](#paw_structure.ion.ion_single "paw_structure.ion.ion_single").
  [`ion_load`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.ion.ion_load "paw_structure.ion.ion_load")(root[, ext])                                               Load information previously saved by [`ion_save()`{.xref .py .py-func .docutils .literal .notranslate}](#paw_structure.ion.ion_save "paw_structure.ion.ion_save").
  [`ion_save`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.ion.ion_save "paw_structure.ion.ion_save")(root, snapshots, id1, id2, id3, …)                         Save results to file.
  [`ion_single`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.ion.ion_single "paw_structure.ion.ion_single")(snap, id1, id2, id3, cut1, cut2)                     Find ion complex of a single snapshot of atomic positions.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------------------------------------------------------------------------

XXX REFERENCE TO ALGORITHM EXPLANATION XXX

 `paw_structure.ion.`{.sig-prename .descclassname}`ion_find_parallel`{.sig-name .descname}(*root*, *snapshots*, *id1*, *id2*, *id3*, *cut1*, *cut2*)[¶](#paw_structure.ion.ion_find_parallel "Permalink to this definition")
:   Find ion complexes for multiple snapshots of atomic configurations.

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name of the files

        -   **snapshots** (list[[`Snap`{.xref .py .py-class .docutils
            .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")])
            – list of snapshots containing the atomic information

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘MN’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible first neighbors (e.g.
            ‘[O\_](#id1)’)

        -   **id3**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors of first
            neighbors (e.g. ‘[H\_](#id3)’)

        -   **cut1**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for first neighbor search

        -   **cut2**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for second neighbor search

    Returns
    :   list of snapshots containing an ion complex

    Return type
    :   list[[`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")]

    Parallelization based on [`multiprocessing`{.xref .py .py-mod
    .docutils .literal
    .notranslate}](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "(in Python v3.8)").

    Note

    Only one atom of type `id1`{.xref .py .py-data .docutils .literal
    .notranslate} allowed to be in a snapshot at the moment.

 `paw_structure.ion.`{.sig-prename .descclassname}`ion_find_wrapper`{.sig-name .descname}(*snap*, *id1*, *id2*, *id3*, *cut1*, *cut2*)[¶](#paw_structure.ion.ion_find_wrapper "Permalink to this definition")
:   Wrapper for [`ion_single()`{.xref .py .py-func .docutils .literal
    .notranslate}](#paw_structure.ion.ion_single "paw_structure.ion.ion_single").

    Parameters
    :   -   **snap** ([`Snap`{.xref .py .py-class .docutils .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap"))
            – single snapshot containing the atomic information

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘MN’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible first neighbors (e.g.
            ‘[O\_](#id5)’)

        -   **id3**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors of first
            neighbors (e.g. ‘[H\_](#id7)’)

        -   **cut1**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for first neighbor search

        -   **cut2**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for second neighbor search

    Returns
    :   snapshot containing an ion complex

    Return type
    :   [`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")

 `paw_structure.ion.`{.sig-prename .descclassname}`ion_load`{.sig-name .descname}(*root*, *ext='.ion'*)[¶](#paw_structure.ion.ion_load "Permalink to this definition")
:   Load information previously saved by [`ion_save()`{.xref .py
    .py-func .docutils .literal
    .notranslate}](#paw_structure.ion.ion_save "paw_structure.ion.ion_save").

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name for the file to be loaded

        -   **ext**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*,**optional*)
            – default “.ion” - extension for the file to be loaded: name
            = root + ext

    Returns
    :   list of snapshots containing an ion complex

    Return type
    :   list[[`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")]

    Note

    Reading is line sensitive. Do not alter the output file before
    loading.

 `paw_structure.ion.`{.sig-prename .descclassname}`ion_save`{.sig-name .descname}(*root*, *snapshots*, *id1*, *id2*, *id3*, *cut1*, *cut2*, *ext='.ion'*)[¶](#paw_structure.ion.ion_save "Permalink to this definition")
:   Save results to file.

    XXX REFERENCE TO EXPLANATION OF .ion FILE FORMAT XXX

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name for saving file

        -   **snapshots** (list[[`Snap`{.xref .py .py-class .docutils
            .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")])
            – list of snapshots containing an ion complex

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘MN’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible first neighbors (e.g.
            ‘[O\_](#id9)’)

        -   **id3**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors of first
            neighbors (e.g. ‘[H\_](#id11)’)

        -   **cut1**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for first neighbor search

        -   **cut2**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for second neighbor search

        -   **ext**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*,**optional*)
            – default “.ion” - extension for the saved file: name = root
            + ext

 `paw_structure.ion.`{.sig-prename .descclassname}`ion_single`{.sig-name .descname}(*snap*, *id1*, *id2*, *id3*, *cut1*, *cut2*)[¶](#paw_structure.ion.ion_single "Permalink to this definition")
:   Find ion complex of a single snapshot of atomic positions.

    Parameters
    :   -   **snap** ([`Snap`{.xref .py .py-class .docutils .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap"))
            – single snapshot containing the atomic information

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘MN’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible first neighbors (e.g.
            ‘[O\_](#id13)’)

        -   **id3**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors of first
            neighbors (e.g. ‘[H\_](#id15)’)

        -   **cut1**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for first neighbor search

        -   **cut2**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for second neighbor search

    Returns
    :   atomic information about complex centered around id1

    Return type
    :   `pandas.DataFrame`{.xref .py .py-mod .docutils .literal
        .notranslate}

    Note

    Implement possibility for more atoms or allow selection by name.

### paw\_structure.tra[¶](#paw-structure-tra "Permalink to this headline")

Trajectory file handling and data storage.

Dependencies: `numpy`{.xref .py .py-mod .docutils .literal .notranslate}
`pandas`{.xref .py .py-mod .docutils .literal .notranslate}
[`utility`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.utility "paw_structure.utility")

  ---------------------------------------------------------------------------------------------------------------------------------------------------- -------------
  [`Snap`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.Snap "paw_structure.tra.Snap")(iter, time, cell, pos, atoms[, …])     

  [`tra_extract`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.tra_extract "paw_structure.tra.tra_extract")(root, n\_atoms)   param root
                                                                                                                                                       :   
                                                                                                                                                       
                                                                                                                                                       

  [`tra_index`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.tra_index "paw_structure.tra.tra_index")(times, t1, t2, n)       param times
                                                                                                                                                       :   
                                                                                                                                                       
                                                                                                                                                       

  [`tra_load`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.tra_load "paw_structure.tra.tra_load")(root)                      param root
                                                                                                                                                       :   
                                                                                                                                                       
                                                                                                                                                       

  [`tra_read`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.tra_read "paw_structure.tra.tra_read")(root, t1, t2, n)           param root
                                                                                                                                                       :   
                                                                                                                                                       
                                                                                                                                                       

  [`tra_save`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.tra_save "paw_structure.tra.tra_save")(root, snapshots)           param root
                                                                                                                                                       :   
                                                                                                                                                       
                                                                                                                                                       

  [`tra_strc_read`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.tra.tra_strc_read "paw_structure.tra.tra_strc_read")(root)       param root
                                                                                                                                                       :   
                                                                                                                                                       
                                                                                                                                                       
  ---------------------------------------------------------------------------------------------------------------------------------------------------- -------------

 *class*`paw_structure.tra.`{.sig-prename .descclassname}`Snap`{.sig-name .descname}(*iter*, *time*, *cell*, *pos*, *atoms*, *dataframe=None*, *hbonds=None*)[¶](#paw_structure.tra.Snap "Permalink to this definition")
:   

 `paw_structure.tra.`{.sig-prename .descclassname}`tra_extract`{.sig-name .descname}(*root*, *n\_atoms*)[¶](#paw_structure.tra.tra_extract "Permalink to this definition")
:   Parameters
    :   -   **root** –

        -   **n\_atoms** –

    Returns:

 `paw_structure.tra.`{.sig-prename .descclassname}`tra_index`{.sig-name .descname}(*times*, *t1*, *t2*, *n*)[¶](#paw_structure.tra.tra_index "Permalink to this definition")
:   Parameters
    :   -   **times** –

        -   **t1** –

        -   **t2** –

        -   **n** –

    Returns:

 `paw_structure.tra.`{.sig-prename .descclassname}`tra_load`{.sig-name .descname}(*root*)[¶](#paw_structure.tra.tra_load "Permalink to this definition")
:   Parameters
    :   **root** –

    Returns:

 `paw_structure.tra.`{.sig-prename .descclassname}`tra_read`{.sig-name .descname}(*root*, *t1*, *t2*, *n*)[¶](#paw_structure.tra.tra_read "Permalink to this definition")
:   Parameters
    :   -   **root** –

        -   **t1** –

        -   **t2** –

        -   **n** –

    Returns:

 `paw_structure.tra.`{.sig-prename .descclassname}`tra_save`{.sig-name .descname}(*root*, *snapshots*)[¶](#paw_structure.tra.tra_save "Permalink to this definition")
:   Parameters
    :   -   **root** –

        -   **snapshots** –

    Returns:

 `paw_structure.tra.`{.sig-prename .descclassname}`tra_strc_read`{.sig-name .descname}(*root*)[¶](#paw_structure.tra.tra_strc_read "Permalink to this definition")
:   Parameters
    :   **root** –

    Returns:

### paw\_structure.water[¶](#paw-structure-water "Permalink to this headline")

Water complex detection.

Find configurations that deviate from the normal molecule structure.

Main routine is [`water_find_parallel()`{.xref .py .py-func .docutils
.literal
.notranslate}](#paw_structure.water.water_find_parallel "paw_structure.water.water_find_parallel").

Dependencies: [`functools`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/functools.html#module-functools "(in Python v3.8)")
`miniutils`{.xref .py .py-mod .docutils .literal .notranslate}
`numpy`{.xref .py .py-mod .docutils .literal .notranslate}
`pandas`{.xref .py .py-mod .docutils .literal .notranslate}
`neighbors`{.xref .py .py-mod .docutils .literal .notranslate}
[`utility`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.utility "paw_structure.utility")
[`Snap`{.xref .py .py-class .docutils .literal
.notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  [`water_find_parallel`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.water.water_find_parallel "paw_structure.water.water_find_parallel")(root, snapshots, id1, id2)   Find water complexes for multiple snapshots of atomic configurations.
  [`water_find_wrapper`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.water.water_find_wrapper "paw_structure.water.water_find_wrapper")(snap, id1, id2, cut)            Wrapper for [`water_single()`{.xref .py .py-func .docutils .literal .notranslate}](#paw_structure.water.water_single "paw_structure.water.water_single").
  [`water_load`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.water.water_load "paw_structure.water.water_load")(root[, ext])                                            Load information previously saved by [`water_save()`{.xref .py .py-func .docutils .literal .notranslate}](#paw_structure.water.water_save "paw_structure.water.water_save").
  [`water_save`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.water.water_save "paw_structure.water.water_save")(root, snapshots, id1, id2, cut[, ext])                  Save results to file.
  [`water_single`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.water.water_single "paw_structure.water.water_single")(snap, id1, id2, cut)                              Find water complex of a single snapshot of atomic positions.
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

XXX REFERENCE TO ALGORITHM EXPLANATION XXX

 `paw_structure.water.`{.sig-prename .descclassname}`water_find_parallel`{.sig-name .descname}(*root*, *snapshots*, *id1*, *id2*, *cut=1.4*)[¶](#paw_structure.water.water_find_parallel "Permalink to this definition")
:   Find water complexes for multiple snapshots of atomic
    configurations.

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name of the files

        -   **snapshots** (list[[`Snap`{.xref .py .py-class .docutils
            .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")])
            – list of snapshots containing the atomic information

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘[O\_](#id1)’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors (e.g.
            ‘[H\_](#id3)’)

        -   **cut**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for neighbor search

    Returns
    :   list of snapshots containing water complexes

    Return type
    :   list[[`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")]

    Parallelization based on [`multiprocessing`{.xref .py .py-mod
    .docutils .literal
    .notranslate}](https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing "(in Python v3.8)").

 `paw_structure.water.`{.sig-prename .descclassname}`water_find_wrapper`{.sig-name .descname}(*snap*, *id1*, *id2*, *cut*)[¶](#paw_structure.water.water_find_wrapper "Permalink to this definition")
:   Wrapper for [`water_single()`{.xref .py .py-func .docutils .literal
    .notranslate}](#paw_structure.water.water_single "paw_structure.water.water_single").

    Parameters
    :   -   **snap** ([`Snap`{.xref .py .py-class .docutils .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap"))
            – single snapshot containing the atomic information

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘[O\_](#id5)’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors (e.g.
            ‘[H\_](#id7)’)

        -   **cut**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for neighbor search

    Returns
    :   snapshot containing water complexes

    Return type
    :   [`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")

 `paw_structure.water.`{.sig-prename .descclassname}`water_load`{.sig-name .descname}(*root*, *ext='.water'*)[¶](#paw_structure.water.water_load "Permalink to this definition")
:   Load information previously saved by [`water_save()`{.xref .py
    .py-func .docutils .literal
    .notranslate}](#paw_structure.water.water_save "paw_structure.water.water_save").

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name for the file to be loaded

        -   **ext**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*,**optional*)
            – default “.water” - extension for the file to be loaded:
            name = root + ext

    Returns
    :   list of snapshots containing water complexes

    Return type
    :   list[[`Snap`{.xref .py .py-class .docutils .literal
        .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")]

    Note

    Reading is line sensitive. Do not alter the output file before
    loading.

 `paw_structure.water.`{.sig-prename .descclassname}`water_save`{.sig-name .descname}(*root*, *snapshots*, *id1*, *id2*, *cut*, *ext='.water'*)[¶](#paw_structure.water.water_save "Permalink to this definition")
:   Save results to file.

    XXX REFERENCE TO EXPLANATION OF .water FILE FORMAT XXX

    Parameters
    :   -   **root**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – root name for saving file

        -   **snapshots** (list[[`Snap`{.xref .py .py-class .docutils
            .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap")])
            – list of snapshots containing the water complexes

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘[O\_](#id9)’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors (e.g.
            ‘[H\_](#id11)’)

        -   **cut**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for neighbor search

        -   **ext**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)")*,**optional*)
            – default “.water” - extension for the saved file: name =
            root + ext

 `paw_structure.water.`{.sig-prename .descclassname}`water_single`{.sig-name .descname}(*snap*, *id1*, *id2*, *cut*)[¶](#paw_structure.water.water_single "Permalink to this definition")
:   Find water complex of a single snapshot of atomic positions.

    Parameters
    :   -   **snap** ([`Snap`{.xref .py .py-class .docutils .literal
            .notranslate}](index.html#paw_structure.tra.Snap "paw_structure.tra.Snap"))
            – single snapshot containing the atomic information

        -   **id1**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atom used as center (e.g. ‘[O\_](#id13)’)

        -   **id2**
            ([*str*](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.8)"))
            – identifier for atoms as possible neighbors (e.g.
            ‘[H\_](#id15)’)

        -   **cut**
            ([*float*](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)"))
            – cutoff distance for neighbor search

    Returns
    :   atomic information about unusual complexes

    Return type
    :   `pandas.DataFrame`{.xref .py .py-mod .docutils .literal
        .notranslate}

    Note

    Refine detection criteria.

### paw\_structure.radial[¶](#paw-structure-radial "Permalink to this headline")

Radial distribution function calculation.

Dependencies: [`functools`{.xref .py .py-mod .docutils .literal
.notranslate}](https://docs.python.org/3/library/functools.html#module-functools "(in Python v3.8)")
`matplotlib`{.xref .py .py-mod .docutils .literal .notranslate}
`miniutils.progress_bar`{.xref .py .py-mod .docutils .literal
.notranslate} `numpy`{.xref .py .py-mod .docutils .literal .notranslate}
`pandas`{.xref .py .py-mod .docutils .literal .notranslate}
`scipy`{.xref .py .py-mod .docutils .literal .notranslate} [`pbc`{.xref
.py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.pbc "paw_structure.pbc")
[`utility`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.utility "paw_structure.utility")

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------
  [`radial_calculate`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_calculate "paw_structure.radial.radial_calculate")(snapshots, id1, id2, cut, nbins)             param snapshots
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_distance`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_distance "paw_structure.radial.radial_distance")(snap, id1, id2, cut[, names])                   param snap
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_distance_parallel`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_distance_parallel "paw_structure.radial.radial_distance_parallel")(snapshots, id1, …)   param snapshots
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_distance_single`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_distance_single "paw_structure.radial.radial_distance_single")(center, pbc\_atoms, cut)   param center
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_integrate`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_integrate "paw_structure.radial.radial_integrate")(radius, rdf, rho)                            param radius
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_load`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_load "paw_structure.radial.radial_load")(root[, ext])                                                param root
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_plot`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_plot "paw_structure.radial.radial_plot")(radius, rdf[, integration])                                 param radius
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       

  [`radial_save`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial.radial_save "paw_structure.radial.radial_save")(root, radius, rdf, snapshots, …)                            param root
                                                                                                                                                                                                       :   
                                                                                                                                                                                                       
                                                                                                                                                                                                       
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -----------------

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_calculate`{.sig-name .descname}(*snapshots*, *id1*, *id2*, *cut*, *nbins*, *names=None*)[¶](#paw_structure.radial.radial_calculate "Permalink to this definition")
:   Parameters
    :   -   **snapshots** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **nbins** –

        -   **names** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_distance`{.sig-name .descname}(*snap*, *id1*, *id2*, *cut*, *names=None*)[¶](#paw_structure.radial.radial_distance "Permalink to this definition")
:   Parameters
    :   -   **snap** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **names** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_distance_c`{.sig-name .descname}(*snap*, *id1*, *id2*, *cut*, *names=None*)[¶](#paw_structure.radial.radial_distance_c "Permalink to this definition")
:   Parameters
    :   -   **snap** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **names** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_distance_c_parallel`{.sig-name .descname}(*snapshots*, *id1*, *id2*, *cut*, *names=None*)[¶](#paw_structure.radial.radial_distance_c_parallel "Permalink to this definition")
:   Parameters
    :   -   **snapshots** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **names** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_distance_parallel`{.sig-name .descname}(*snapshots*, *id1*, *id2*, *cut*, *names=None*)[¶](#paw_structure.radial.radial_distance_parallel "Permalink to this definition")
:   Parameters
    :   -   **snapshots** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **names** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_distance_single`{.sig-name .descname}(*center*, *pbc\_atoms*, *cut*)[¶](#paw_structure.radial.radial_distance_single "Permalink to this definition")
:   Parameters
    :   -   **center** –

        -   **pbc\_atoms** –

        -   **cut** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_integrate`{.sig-name .descname}(*radius*, *rdf*, *rho*)[¶](#paw_structure.radial.radial_integrate "Permalink to this definition")
:   Parameters
    :   -   **radius** –

        -   **rdf** –

        -   **rho** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_load`{.sig-name .descname}(*root*, *ext='.radial'*)[¶](#paw_structure.radial.radial_load "Permalink to this definition")
:   Parameters
    :   -   **root** –

        -   **ext** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_plot`{.sig-name .descname}(*radius*, *rdf*, *integration=None*)[¶](#paw_structure.radial.radial_plot "Permalink to this definition")
:   Parameters
    :   -   **radius** –

        -   **rdf** –

        -   **integration** –

    Returns:

 `paw_structure.radial.`{.sig-prename .descclassname}`radial_save`{.sig-name .descname}(*root*, *radius*, *rdf*, *snapshots*, *id1*, *id2*, *cut*, *nbins*, *rho*, *ext='.radial'*)[¶](#paw_structure.radial.radial_save "Permalink to this definition")
:   Parameters
    :   -   **root** –

        -   **radius** –

        -   **rdf** –

        -   **snapshots** –

        -   **id1** –

        -   **id2** –

        -   **cut** –

        -   **nbins** –

        -   **rho** –

        -   **ext** –

    Returns:

### paw\_structure.hbonds\_c[¶](#paw-structure-hbonds-c "Permalink to this headline")

Dependencies: `numpy`{.xref .py .py-mod .docutils .literal .notranslate}
[`pbc`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.pbc "paw_structure.pbc")

  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------
  [`calc_angle`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.calc_angle "paw_structure.hbonds_c.calc_angle")(arg0, arg1, arg2)                           
  [`calc_dist_vec`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.calc_dist_vec "paw_structure.hbonds_c.calc_dist_vec")(arg0, arg1)                        
  [`calc_norm`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.calc_norm "paw_structure.hbonds_c.calc_norm")(arg0)                                          
  [`calc_skalar`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.calc_skalar "paw_structure.hbonds_c.calc_skalar")(v1, v2)                                  Calculate scalar.
  [`hbonds_number`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.hbonds_number "paw_structure.hbonds_c.hbonds_number")(arg0, arg1, arg2, arg3, arg4, …)   
  [`hbonds`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.hbonds "paw_structure.hbonds_c.hbonds")(arg0, arg1, arg2, arg3, arg4, arg5)                     
  [`pbc_apply3x3`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.hbonds_c.pbc_apply3x3 "paw_structure.hbonds_c.pbc_apply3x3")(arg0, arg1, arg2)                     
  ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`calc_angle`{.sig-name .descname}(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg1: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")[¶](#paw_structure.hbonds_c.calc_angle "Permalink to this definition")
:   

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`calc_dist_vec`{.sig-name .descname}(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg1: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")[¶](#paw_structure.hbonds_c.calc_dist_vec "Permalink to this definition")
:   

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`calc_norm`{.sig-name .descname}(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")[¶](#paw_structure.hbonds_c.calc_norm "Permalink to this definition")
:   

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`calc_skalar`{.sig-name .descname}(*v1: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *v2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")[¶](#paw_structure.hbonds_c.calc_skalar "Permalink to this definition")
:   Calculate scalar.

    Parameters
    :   -   **v1** (*double \**) – pointer on 3-dim. vector

        -   **v2** (*double \**) – pointer on 3-dim. vector

    Returns
    :   double

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`hbonds`{.sig-name .descname}(*arg0: numpy.ndarray[longdouble]*, *arg1: numpy.ndarray[longdouble]*, *arg2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg3: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg4: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg5: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")[¶](#paw_structure.hbonds_c.hbonds "Permalink to this definition")
:   

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`hbonds_number`{.sig-name .descname}(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg1: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*, *arg2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg3: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*, *arg4: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg5: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg6: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg7: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")[¶](#paw_structure.hbonds_c.hbonds_number "Permalink to this definition")
:   

 `paw_structure.hbonds_c.`{.sig-prename .descclassname}`pbc_apply3x3`{.sig-name .descname}(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg1: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*, *arg2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")[¶](#paw_structure.hbonds_c.pbc_apply3x3 "Permalink to this definition")
:   

### paw\_structure.radial\_c[¶](#paw-structure-radial-c "Permalink to this headline")

Dependencies: `numpy`{.xref .py .py-mod .docutils .literal .notranslate}
[`pbc`{.xref .py .py-mod .docutils .literal
.notranslate}](index.html#module-paw_structure.pbc "paw_structure.pbc")

  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------
  [`radial`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial_c.radial "paw_structure.radial_c.radial")(arg0, arg1, arg2, arg3)                                    Calculate scalar.
  [`radial_calculate`{.xref .py .py-obj .docutils .literal .notranslate}](#paw_structure.radial_c.radial_calculate "paw_structure.radial_c.radial_calculate")(arg0, arg1, arg2, arg3, …)   
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- -------------------

 `paw_structure.radial_c.`{.sig-prename .descclassname}`radial`{.sig-name .descname}(*arg0: numpy.ndarray[float64]*, *arg1: numpy.ndarray[float64]*, *arg2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg3: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → numpy.ndarray[float64][¶](#paw_structure.radial_c.radial "Permalink to this definition")
:   Calculate scalar.

    Parameters
    :   -   **v1** (*double \**) – pointer on 3-dim. vector

        -   **v2** (*double \**) – pointer on 3-dim. vector

    Returns
    :   double

 `paw_structure.radial_c.`{.sig-prename .descclassname}`radial_calculate`{.sig-name .descname}(*arg0: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg1: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*, *arg2: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg3: [int](https://docs.python.org/3/library/functions.html#int "(in Python v3.8)")*, *arg4: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*, *arg5: [float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")*) → List[[float](https://docs.python.org/3/library/functions.html#float "(in Python v3.8)")][¶](#paw_structure.radial_c.radial_calculate "Permalink to this definition")
:   

* * * * *

© Copyright 2020, Lukas Rump

Built with [Sphinx](http://sphinx-doc.org/) using a
[theme](https://github.com/rtfd/sphinx_rtd_theme) provided by [Read the
Docs](https://readthedocs.org).
