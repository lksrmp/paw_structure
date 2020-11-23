"""
paw_structure.neighbor
----------------------
Helper functions for atomic neighbor search.

Dependencies:
    :py:mod:`numpy`
    :mod:`.pbc`

.. autosummary::

      neighbor_find
      neighbor_find_single
      neighbor_name
      neighbor_name_single
"""

import numpy as np
# MODULES WITHIN PROJECT
from . import pbc

########################################################################################################################
# RETURN NAMES OF ATOMS CLOSER THAN cut FROM center ATOM
# ONLY FOR A SINGLE ATOM AS REFERENCE
########################################################################################################################
# INPUT
# pandas DataFrame center       central atom of reference
# pandas DataFrame pbc_atoms    atoms as possible neighbors
# float cut                     cutoff distance for search
#####
# OUTPUT
# list str                      list of names of neighbors
########################################################################################################################
def neighbor_name_single(center, pbc_atoms, cut):
    """
    Find names of neighbor atoms given one central atom.

    Args:
        center (pandas DataFrame): central atom of reference
        pbc_atoms (pandas DataFrame): atoms as possible neighbors
        cut (float): cutoff distance for search

    Returns:
        list[str]: names of neighboring atoms
    """
    dist = np.linalg.norm(center['pos'] - pbc_atoms['pos'], axis=1)  # calculate distance to center
    neighbors = pbc_atoms[[a and not b for a, b in zip(dist < cut, np.isclose(dist, 0.0))]]  # select fitting atoms
    return neighbors['name'].values  # return their names as a list


########################################################################################################################
# TODO: get rid of neighbor_name in whole code, might be very inefficient
#  (output names and then search snapshots from names)
# FIND NAMES OF NEIGHBOR ATOMS
########################################################################################################################
# INPUT
# class Snap snap
# str id1                   identifier for atoms used as center (e.g. 'H_' or 'O_')
# str id2                   identifier for atoms used as potential neighbors
# float cut                 cutoff distance for search
# list str names (optional) use names (e.g. 'O_43', 'H_23') of atoms as center instead of identifiers
########################################################################################################################
# OUTPUT
# list list str             list of list of atom names; first element is center, the following are neighbors of center
########################################################################################################################
def neighbor_name(snap, id1, id2, cut, names=None):
    """
    Find neighbors for a given selection of atoms.

    Args:
        snap (:class:`.Snap`): snapshot containing the atomic information
        id1 (str): identifier for atom used as center (e.g. 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'H\_')
        cut (float): cutoff distance for search
        names (list[str], optional): list of names of atoms used as center; replaces :data:`id1`

    Returns:
        list[list[str]]: list of lists with names according to [center neighbor1 neighbor2]

    .. Todo::
        Very inefficient approach! Still in use in :func:`.ion_single` and :func:`.water_single`.
        Should be replaced by more efficient search approach.
    """
    pbc_atoms = pbc.pbc_apply3x3(snap, id=[id2])  # create 3x3 unit cell of atom species id2
    neighbors = []  # initialize dictionary for storage of neighbor names
    if names is None:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['id'] == id1:
                next = neighbor_name_single(row, pbc_atoms, cut)
                neighbors.append(np.insert(next, 0, row['name']))
    else:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms with name contained in names
            if row['name'] in names:
                next = neighbor_name_single(row, pbc_atoms, cut)
                neighbors.append(np.insert(next, 0, row['name']))
    return [x.tolist() for x in neighbors]  # return list of lists with each first element being the center

########################################################################################################################
# RETURN ATOMS CLOSER THAN cut FROM center ATOM
########################################################################################################################
# INPUT
# pandas DataFrame center       central atom of reference
# pandas DataFrame pbc_atoms    atoms as possible neighbors
# float cut                     cutoff distance for search
#####
# OUTPUT
# pandas DataFrame neighbors    contains all information about the neighbors found
########################################################################################################################
def neighbor_find_single(center, pbc_atoms, cut):
    """
    Find names of neighbor atoms given one central atom.

    Args:
        center (pandas DataFrame): central atom of reference
        pbc_atoms (pandas DataFrame): atoms as possible neighbors
        cut (float): cutoff distance for search

    Returns:
        pandas DataFrame: contains all information about the neighbors found

    """
    dist = np.linalg.norm(center['pos'] - pbc_atoms['pos'], axis=1)  # calculate distance to center
    neighbors = pbc_atoms[[a and not b for a, b in zip(dist < cut, np.isclose(dist, 0.0))]]  # select fitting atoms
    return neighbors  # return dataframe


########################################################################################################################
# FIND NEIGHBOR ATOMS
########################################################################################################################
# INPUT
# class Snap snap           snapshot with all information
# str id1                   identifier for atoms used as center (e.g. 'H_' or 'O_')
# str id2                   identifier for atoms used as potential neighbors
# float cut                 cutoff distance for search
# list str names (optional) use names (e.g. 'O_43', 'H_23') of atoms as center instead of identifiers
#####
# OUTPUT
# dict DataFrame neighbors  dictionary with center atom names as key and pandas DataFrame of neighbors as entry
########################################################################################################################
def neighbor_find(snap, id1, id2, cut, names=None):
    """
    Find neighbor atoms for a given selection of central atom.

    Args:
        snap (:class:`.Snap`): snapshot containing the atomic information
        id1 (str): identifier for atom used as center (e.g. 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'H\_')
        cut (float): cutoff distance for search
        names (list[str], optional): list of names of atoms used as center; replaces :data:`id1`

    Returns:
        dict: name as center atoms are used as keys; pandas DataFrame containing its neighbors is the entry
    """
    pbc_atoms = pbc.pbc_apply3x3(snap, id=[id2])  # create 3x3 unit cell of atom species id2
    neighbors = {}  # initialize dictionary for storage of neighbor names
    if names is None:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['id'] == id1:
                next = neighbor_find_single(row, pbc_atoms, cut)
                neighbors[row['name']] = next
    else:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['name'] in names:
                next = neighbor_find_single(row, pbc_atoms, cut)
                neighbors[row['name']] = next
    return neighbors  # return dictionary
