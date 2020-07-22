#!/usr/lib/env python3
import sys

# MODULES WITHIN PROJECT
from . import utility
from . import tra
from . import pbc
from . import ion
from . import water
from .scntl import scntl_read
from . import hbonds
from . import radial


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
    print(sys.argv)
    # check argument passed
    scntl_root = utility.argcheck(sys.argv, '.scntl')

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
            pbc.pbc_folding(snapshots)

        # check for saving <root>.snap
        if scntl['!TRA']['SAVE']:
            tra.tra_save(root, snapshots)

    # check for ION COMPLEX ANALYSIS
    if '!ION' in scntl.keys():
        ion_complex = ion.ion_find_parallel(root, snapshots, scntl['!ION']['ID1'], scntl['!ION']['ID2'],
                                            scntl['!ION']['ID3'], scntl['!ION']['CUT1'], scntl['!ION']['CUT2'])

    # check for WATER COMPLEX ANALYSIS
    if '!WATER' in scntl.keys():
        water_complex = water.water_find_parallel(root, snapshots, scntl['!WATER']['ID1'], scntl['!WATER']['ID2'],
                                                  cut=scntl['!WATER']['CUT'])

    # check for HYDROGEN BONDS ANALYSIS
    if '!HBONDS' in scntl.keys():
        args = [scntl['!HBONDS']['OO_MIN'], scntl['!HBONDS']['OO_MAX'], scntl['!HBONDS']['G_FACTOR'],
                scntl['!HBONDS']['THRESHOLD']]
        h_bonds = hbonds.hbonds_find_parallel(root, snapshots, scntl['!HBONDS']['ID1'], scntl['!HBONDS']['ID2'],
                                              cut1=scntl['!HBONDS']['CUT1'], cut2=scntl['!HBONDS']['CUT2'], args=args)

    # check for RADIAL DISTRIBUTION FUNCTION ANALYSIS
    if '!RADIAL' in scntl.keys():
        if scntl['!RADIAL']['TRA_EXTRACT']:
            snapshots_r = tra.tra_read(root, scntl['!RADIAL']['T1'], scntl['!RADIAL']['T2'], scntl['!RADIAL']['N'])
            # check if atoms project into unit cell
            if scntl['GENERAL']['PBC_FOLDING']:
                pbc.pbc_folding(snapshots_r)
        else:
            snapshots_r = snapshots
        radius, rdf, coord, rho = radial.radial_calculate(snapshots_r, scntl['!RADIAL']['ID1'], scntl['!RADIAL']['ID2'],
                                       scntl['!RADIAL']['CUT'], scntl['!RADIAL']['NBINS'])
        radial.radial_save(root, radius, rdf, coord, snapshots_r, scntl['!RADIAL']['ID1'], scntl['!RADIAL']['ID2'],
                           scntl['!RADIAL']['CUT'], scntl['!RADIAL']['NBINS'], rho)
