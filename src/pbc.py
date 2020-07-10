"""
paw_structure.pbc
-----------------
Functions for application of periodic boundary conditions.

Dependencies:
:mod:`.utility`
:py:mod:`copy`
:py:mod:`numpy`

.. autosummary::

      pbc_apply3x3
      pbc_folding
      pbc_general
"""

import numpy as np
from copy import deepcopy
# MODULES WITHIN PROJECT
from . import utility


########################################################################################################################
# FOLD ATOM POSITIONS INTO CUBIC UNIT CELL STARTING AT ORIGIN
# NECESSARY IF ATOMS ARE FAR APART neighbor DETECTION WORKS WITH 3x3 UNIT CELL -> COULD FAIL
########################################################################################################################
# INPUT
# list class Snap snapshots     data for every snapshot (alteration stays outside the function so no return)
########################################################################################################################
# TODO: only works for cubic lattices of type
# ax  0  0
#  0 ay  0
#  0  0 az
def pbc_folding(snapshots):
    """
    Folding of atoms into a single unit cell.

    Args:
        snapshots (list[:class:`.Snap`]): list of Snap objects of which the atomic positions should be adjusted


    During AIMD simulations atoms can move outside of the initial unit cell. For easier calculation and later analysis
    it is advised to project them into a common unit cell.

    The origin is at (0,0,0).

    Note:
        Only works for cubic unit cells.
        Directly operates and alters the atomic positions.
    """
    print("PROJECTION OF ATOMS INTO CUBIC UNIT CELL")
    for snap in snapshots:  # loop through list
        lattice = [i.max() for i in snap.cell]  # get unit cell
        multiplier = []
        # calculate number of lattice translations needed for each individual atom to get into unit cell
        for i in range(3):
            multiplier.append([int(r/lattice[i]) if r > 0.0 else int(r/lattice[i] - 1)
                               for r in snap.atoms['pos'].values[:,i]])
        multiplier = np.array(multiplier).T
        snap.atoms['pos'] -= multiplier * np.array(lattice)


########################################################################################################################
# CREATE 3x3 SUPERCELL FROM GIVEN UNIT CELL
# THE ORIGINAL UNIT CELL IS LOCATED IN THE CENTER
########################################################################################################################
# INPUT
# class Snap snap               data of single snapshot
# list str id                   list of identifiers of selected atom species (e.g. 'O_' or 'H_')
# list str names                list of names of selected atoms (e.g. 'O_43' or 'H_15')
#####
# OUTPUT
# pandas DataFrame snap_pbc
########################################################################################################################
# TODO: make id optional as well
def pbc_apply3x3(snap, id=None, names=None):
    """
    Create 3x3 supercell.

    Args:
        snap (:class:`.Snap`): single snapshot containing the initial atomic positions
        id (list[str], optional): list of identifiers of selected atom species (e.g. "O_" or "H_")
        names (list[str], optional): list of names of selected atoms (e.g. "O_43" or "H_15")

    Takes all atoms if :data:`id` and :data:`names` is not given.

    Returns:
        :class:`.Snap`: snapshot with atomic positions of a 3x3 supercell

    Is used to apply periodic boundary conditions when for example searching for atomic neighbors
    (see e.g. :mod:`.neighbor`). Original unit cell is in the middle.

    Note:
        Implement creation of smaller super cell that still garantees periodic boundary conditions.
    """
    if id is not None and names is None:
        snap_pbc = snap.atoms[snap.atoms['id'].isin(id)]  # filter for atoms of correct type
    elif id is None and names is not None:
        snap_pbc = snap.atoms[snap.atoms['name'].isin(names)]  # filter atoms for correct names
    elif id is None and names is None:
        snap_pbc = snap.atoms  # take all atoms
    else:
        utility.err('pbc_apply3x3', 0, [])
    for i in range(3):  # loop through the three unit cell vectors
        new = snap_pbc.copy()
        new.loc[:, 'pos'] += snap.cell[i]
        snap_pbc = snap_pbc.append(new, ignore_index=True)
        new['pos'] -= 2. * snap.cell[i]
        snap_pbc = snap_pbc.append(new, ignore_index=True)
    return snap_pbc


########################################################################################################################
# CREATE SUPERCELL FROM GIVEN UNIT CELL AND DIRECTIONS
# ORIGINAL UNIT CELL IS AT ORIGIN OF SUPERCELL
########################################################################################################################
# INPUT
# class Snap snap               data of single snapshot
# list int directions           list of directions for periodic boundary conditions (e.g. [2, 3, 2])
#####
# OUTPUT
# class Snap snap_pbc
########################################################################################################################
def pbc_general(snap, directions):
    """
    Apply general periodic boundary conditions.

    Args:
        snap (:class:`.Snap`):
        directions (list[int]):

    Returns:
        :class:`.Snap`: snapshot with periodic boundary conditions applied to atomic positions

    Original unit cell is at the corner of the supercell.
    """
    snap_pbc = deepcopy(snap)
    # loop through three directions
    for i in range(3):
        new = snap_pbc.atoms.copy()
        # loop through given multiplicity
        for j in range(1, directions[i]):
            new.loc[:, 'pos'] += snap.cell[i]
            snap_pbc.atoms = snap_pbc.atoms.append(new, ignore_index=True)
    return snap_pbc
