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
def neighbor_single_name(center, pbc_atoms, cut):
    """
    Find names of neighbor atoms



    Args:
        center (pandas DataFrame): central atom of reference
        pbc_atoms (pandas DataFrame): atoms as possible neighbors
        cut (float): cutoff distance for search

    Returns:
        list of names as strings
    """
    dist = np.linalg.norm(center['pos'] - pbc_atoms['pos'], axis=1)  # calculate distance to center
    neighbors = pbc_atoms[[a and not b for a, b in zip(dist < cut, np.isclose(dist, 0.0))]]  # select fitting atoms
    return neighbors['name'].values  # return their names as a list

########################################################################################################################
# TODO: get rid of neighbor_find_name in whole code, might be very inefficient
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
def neighbor_find_name(snap, id1, id2, cut, names=None):
    pbc_atoms = pbc.pbc_apply3x3(snap, id=[id2])  # create 3x3 unit cell of atom species id2
    neighbors = []  # initialize dictionary for storage of neighbor names
    if names is None:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['id'] == id1:
                next = neighbor_single_name(row, pbc_atoms, cut)
                neighbors.append(np.insert(next, 0, row['name']))
    else:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['name'] in names:
                next = neighbor_single_name(row, pbc_atoms, cut)
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
def neighbor_single(center, pbc_atoms, cut):
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
    pbc_atoms = pbc.pbc_apply3x3(snap, id=[id2])  # create 3x3 unit cell of atom species id2
    neighbors = {}  # initialize dictionary for storage of neighbor names
    if names is None:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['id'] == id1:
                next = neighbor_single(row, pbc_atoms, cut)
                neighbors[row['name']] = next
    else:
        for index, row in snap.atoms.iterrows():  # iterate through all atoms of species id1
            if row['name'] in names:
                next = neighbor_single(row, pbc_atoms, cut)
                neighbors[row['name']] = next
    return neighbors  # return dictionary
