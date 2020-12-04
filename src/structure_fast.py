"""
paw_structure.structure_fast
----------------------------
Data extraction from trajectory file.

**Usage in command line:**

    ::

        paw_structure_fast filename

    :data:`filename` is the name of the :ref:`control file ".scntl" <Control>`.

Dependencies:
    :py:mod:`sys`
    :mod:`.angle`
    :mod:`.hbonds`
    :mod:`.ion`
    :mod:`.pbc`
    :mod:`.radial`
    :mod:`.scntl`
    :mod:`.tra`
    :mod:`.utility`
    :mod:`.water`

.. autosummary::

    main

"""
import sys

# MODULES WITHIN PROJECT
from . import angle
from . import hbonds
from . import ion
from . import pbc
from . import radial
from .scntl import scntl_read
from . import tra
from . import utility
from . import water


import io
from contextlib import redirect_stdout


########################################################################################################################
# MAIN PROGRAM FOR DATA EXTRACTION FROM TRAJECTORY FILE
########################################################################################################################
# USAGE
# python3 structure_fast.py <root>.scntl
# <root>.scntl  CONTROL FILE FOR DATA EXTRACTION
#####
# OUTPUT (depends on options selected in control file)
# <root>.snap       all atomic positions and information about all selected snapshots
# <root>.ion        atomic position of ion complex and information about extraction method
# <root>.water      atomic positions of water complexes and information about extraction method
# <root>.hbonds     names of atoms connected by hydrogen bonds and information about extraction method
# <root>.radial     values for radius and RDF
########################################################################################################################
def main():
    """
    Entry point for :mod:`.structure_fast`.
    """
    args = utility.structure_fast_input()
    # check argument passed
    scntl_root = utility.argcheck([sys.argv[0], args.scntl], '.scntl')

    # read control file
    scntl = scntl_read(scntl_root)

    # check for ROOT name in control file
    if scntl['GENERAL']['ROOT']:
        root = scntl['GENERAL']['ROOT']
    else:
        root = scntl_root

    if '!TRA' in scntl.keys():
        # check for LOAD of <root>.snap file, else read trajectory file
        if scntl['!TRA']['LOAD']:
            snapshots = tra.tra_load(root)
        else:
            snapshots = tra.tra_read(root, scntl['!TRA']['T1'], scntl['!TRA']['T2'], scntl['!TRA']['N'])

        # check if atoms project into unit cell
        if scntl['GENERAL']['PBC_FOLDING']:
            # pbc.pbc_folding(snapshots)  non-parallel version
            snapshots = pbc.pbc_folding_parallel(snapshots)

        # check for saving <root>.snap
        if scntl['!TRA']['SAVE']:
            tra.tra_save(root, snapshots)

    # check for ION COMPLEX ANALYSIS
    if '!ION' in scntl.keys():
        ion.ion_find_parallel(root, snapshots, scntl['!ION']['ID1'], scntl['!ION']['ID2'],
                                            scntl['!ION']['ID3'], scntl['!ION']['CUT1'], scntl['!ION']['CUT2'])

    # check for WATER COMPLEX ANALYSIS
    if '!WATER' in scntl.keys():
        water.water_find_parallel(root, snapshots, scntl['!WATER']['ID1'], scntl['!WATER']['ID2'],
                                                  cut=scntl['!WATER']['CUT'])

    # check for HYDROGEN BONDS ANALYSIS
    if '!HBONDS' in scntl.keys():
        # USED FOR OLD CRITERION
        # args = [scntl['!HBONDS']['OO_MIN'], scntl['!HBONDS']['OO_MAX'], scntl['!HBONDS']['G_FACTOR'],
        #         scntl['!HBONDS']['THRESHOLD']]
        hbonds.hbonds_find_parallel(root, snapshots, scntl['!HBONDS']['ID1'], scntl['!HBONDS']['ID2'],
                                    scntl['!HBONDS']['CUT1'], scntl['!HBONDS']['CUT2'], scntl['!HBONDS']['ANGLE'])

    # check for RADIAL DISTRIBUTION FUNCTION ANALYSIS
    if '!RADIAL' in scntl.keys():
        if scntl['!RADIAL']['TRA_EXTRACT']:
            snapshots_r = tra.tra_read(root, scntl['!RADIAL']['T1'], scntl['!RADIAL']['T2'], scntl['!RADIAL']['N'])
            # check if atoms project into unit cell
            if scntl['GENERAL']['PBC_FOLDING']:
                # pbc.pbc_folding(snapshots_r) non-parallel version
                snapshots_r = pbc.pbc_folding_parallel(snapshots_r)
        else:
            snapshots_r = snapshots
        radius, rdf, coord, rho = radial.radial_calculate(snapshots_r, scntl['!RADIAL']['ID1'], scntl['!RADIAL']['ID2'],
                                       scntl['!RADIAL']['CUT'], scntl['!RADIAL']['NBINS'])
        radial.radial_save(root, radius, rdf, coord, snapshots_r, scntl['!RADIAL']['ID1'], scntl['!RADIAL']['ID2'],
                           scntl['!RADIAL']['CUT'], scntl['!RADIAL']['NBINS'], rho)

    # check for ANGLE DISTRIBUTION FUNCTION ANALYSIS
    if '!ANGLE' in scntl.keys():
        if scntl['!ANGLE']['TRA_EXTRACT']:
            snapshots_r = tra.tra_read(root, scntl['!ANGLE']['T1'], scntl['!ANGLE']['T2'], scntl['!ANGLE']['N'])
            # check if atoms project into unit cell
            if scntl['GENERAL']['PBC_FOLDING']:
                # pbc.pbc_folding(snapshots_r) non-parallel version
                snapshots_r = pbc.pbc_folding_parallel(snapshots_r)
        else:
            snapshots_r = snapshots
        degree, adf = angle.angle_calculate(snapshots_r, scntl['!ANGLE']['ID1'], scntl['!ANGLE']['ID2'],
                                                          scntl['!ANGLE']['CUT'], scntl['!ANGLE']['NBINS'])
        angle.angle_save(root, degree, adf, snapshots_r, scntl['!ANGLE']['ID1'], scntl['!ANGLE']['ID2'],
                           scntl['!ANGLE']['CUT'], scntl['!ANGLE']['NBINS'])
