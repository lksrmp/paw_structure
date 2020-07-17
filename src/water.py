"""
paw_structure.water
-------------------
Water complex detection.

Find configurations that deviate from the normal molecule structure.

Main routine is :func:`water_find_parallel`.

Dependencies:
:py:mod:`functools`
:py:mod:`miniutils`
:py:mod:`numpy`
:py:mod:`pandas`
:mod:`.neighbors`
:mod:`.utility`
:class:`.Snap`

.. autosummary::

      water_find_parallel
      water_load
      water_save
      water_single

XXX REFERENCE TO ALGORITHM EXPLANATION XXX
"""

import numpy as np
import pandas as pd
from functools import partial
import miniutils.progress_bar as progress
# MODULES WITHIN PROJECT
from . import neighbor
from .tra import Snap
from . import utility


########################################################################################################################
# FIND UNUSUAL WATER COMPLEXES FOR ONE SNAPSHOT
# TODO: find single hydrogen atoms which are not near an oxygen atom?
########################################################################################################################
# INPUT
# class Snap snap   snapshot containing all information
# str id1           identifier for atoms used as center (e.g. 'O_')
# str id2           identifier for atoms as possible neighbors (e.g. 'H_')
# float cut         cutoff distance for neighbor search
#####
# OUTPUT
# pandas DataFrame  contains the whole complex centered around id1
########################################################################################################################
def water_single(snap, id1, id2, cut):
    """
    Find water complex of a single snapshot of atomic positions.

    Args:
        snap (:class:`.Snap`): single snapshot containing the atomic information
        id1 (str): identifier for atom used as center (e.g. 'O_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'H_')
        cut (float): cutoff distance for neighbor search

    Returns:
        :class:`.Snap`: snapshot containing water complexes

    Note:
        Refine detection criteria.
    """
    if id1 == id2:
        utility.err('water_single', 0, [id1, id2])
    next = neighbor.neighbor_find_name(snap, id1, id2, cut)
    atoms = []
    # next1 = neighbor.neighbor_find_name(snap, id2, id1, cut)
    for i in range(len(next)):
        # TODO: determine criterion for water complex detection
        # if oxygen has more or less than 2 hydrogen neighbors
        if len(next[i]) != 3:
            atoms.append(next[i])
        # if two oxygen atoms share a hydrogen atom
        for j in range(i+1, len(next)):
            if set(next[i][1:]) & set(next[j][1:]):
                atoms.append(next[i])
                atoms.append(next[j])
    # for i in range(len(next1)):
    #     if len(next1[i]) > 2:
    #         atoms.append(next1[i])

    # formatting necessary because of function np.unique
    if len(atoms) < 2:
        atoms = np.unique(atoms).tolist()  # structured list
    elif len(np.unique([len(i) for i in atoms])) == 1:
        atoms = np.unique(atoms).tolist()  # structured list
    else:
        atoms = np.unique(atoms).tolist()  # structured list
        atoms = [x for y in atoms for x in y]  # flatten list
        atoms = np.unique(atoms).tolist()  # unique names
    atoms = snap.atoms.loc[snap.atoms['name'].isin(atoms)]  # select parts of DataFrame
    return Snap(snap.iter, snap.time, snap.cell, None, None, dataframe=atoms)


########################################################################################################################
# SAVE INFORMATION FROM water_find(_parallel)() TO FILE <root>.ext FOR LATER ANALYSIS
########################################################################################################################
# INPUT
# str root                      root name for saving file
# list class Snap snapshots     list with information to be saved
# str id1                       identifier for atoms used as center (e.g. 'O_')
# str id2                       identifier for atoms as possible neighbors (e.g. 'H_')
# float cut                     cutoff distance for neighbor search
# str ext (optional)            extension for the saved file: name = root + ext
########################################################################################################################
def water_save(root, snapshots, id1, id2, cut, ext='.water'):
    """
    Save results to file.

    XXX REFERENCE TO EXPLANATION OF .water FILE FORMAT XXX

    Args:
        root (str): root name for saving file
        snapshots (list[:class:`.Snap`]): list of snapshots containing the water complexes
        id1 (str): identifier for atom used as center (e.g. 'O_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'H_')
        cut (float): cutoff distance for neighbor search
        ext (str, optional): default ".water" - extension for the saved file: name = root + ext
    """
    # open file
    path = root + ext
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('water_save', path)
    # write header
    f.write("WATER COMPLEXES\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
    f.write("%-14s%14s\n" % ("ID1", id1))
    f.write("%-14s%14s\n" % ("ID2", id2))
    f.write("%-14s%14.8f\n" % ("CUT", cut))
    f.write("%-14s\n" % "UNIT CELL")
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    # write structure information
    for i in range(len(snapshots)):
        f.write("-" * 84 + "\n")
        f.write("%-14s%-14.8f%-14s%-14d%-14s%-14d\n" %
                ("TIME", snapshots[i].time, "ITERATION", snapshots[i].iter, "ATOMS", len(snapshots[i].atoms)))
        f.write("%-14s%-14s%-14s%14s%14s%14s\n" % ('NAME', 'ID', 'INDEX', 'X', 'Y', 'Z'))
        np.savetxt(f, snapshots[i].atoms, fmt="%-14s%-14s%-14d%14.8f%14.8f%14.8f")
    f.close()
    return


########################################################################################################################
# LOAD INFORMATION PREVIOUSLY SAVED BY water_save()
# WARNING: READING IS LINE SENSITIVE! ONLY USE ON UNCHANGED FILES WRITTEN BY water_save()
# TODO: remove line sensitivity
########################################################################################################################
# INPUT
# str root                      root name for the file to be loaded
# str ext (optional)            extension for the file to be loaded: name = root + ext
#####
# OUTPUT
# list class Snap snapshots     list of all information
########################################################################################################################
def water_load(root, ext='.water'):
    """
    Load information previously saved by :func:`.water_save`.

    Args:
        root (str): root name for the file to be loaded
        ext (str, optional): default ".water" - extension for the file to be loaded: name = root + ext

    Returns:
        list[:class:`.Snap`]: list of snapshots containing water complexes

    Note:
        Reading is line sensitive. Do not alter the output file before loading.
    """
    # open file
    path = root + ext
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('water_load', path)
    text = f.readlines()  # read text as lines
    for i in range(len(text)):
        text[i] = text[i].split()  # split each line into list with strings as elements
    snapshots = []  # storage list
    cell = np.array(text[8:11], dtype=float)  # get unit cell
    for i in range(len(text)):
        if text[i][0] == "TIME":  # search for trigger of new snapshot
            iteration = int(text[i][3])
            time = float(text[i][1])
            n_atoms = int(text[i][5])
            # TODO: check read and write functions for compatibility for empty input
            if n_atoms == 0:
                df = pd.DataFrame(columns=['name', 'id', 'index', 'pos', 'pos', 'pos'])
                snapshots.append(Snap(iteration, time, cell, None, None, dataframe=df))
            else:
                test = np.array(text[i + 2:i + 2 + n_atoms])
                atoms = {}
                atoms['name'] = test[:, 0]
                atoms['id'] = test[:, 1]
                atoms['index'] = np.array(test[:, 2], dtype=int)
                df = pd.DataFrame(data=atoms)
                # save information as class Snap
                snapshots.append(Snap(iteration, time, cell, np.array(test[:, 3:6], dtype=np.float64), df))
    return snapshots


########################################################################################################################
# FIND WATER COMPLEXES FOR LIST OF SNAPSHOTS
# WARNING: NOT IN USE BECAUSE NO PARALLEL COMPUTING
########################################################################################################################
# INPUT
# str root                      root name for saving file
# list class Snap snapshots     list with information to be saved
# str id1                       identifier for atoms used as center (e.g. 'O_')
# str id2                       identifier for atoms as possible first neighbors (e.g. 'H_')
# float cut (optional)          cutoff distance for neighbor search
#####
# OUTPUT
# list class Snap complex       list with all water complexes found
########################################################################################################################
# def water_find(root, snapshots, id1, id2, cut=1.4):
#     complex = []
#     # loop through different snapshots
#     for snap in snapshots:
#         # get complex information
#         comp = water_single(snap, id1, id2, cut)
#         # append Snap object for data storage
#         complex.append(Snap(snap.iter, snap.time, snap.cell, None, None, dataframe=comp))
#     # save information to file
#     water_save(root, complex, id1, id2, cut)
#     return complex


########################################################################################################################
# ROUTINE TO FIND WATER COMPLEXES FOR MULTIPLE SNAPSHOTS
# PARALLEL VERSION OF water_find() WITH PROGRESS BAR IN CONSOLE
########################################################################################################################
# INPUT
# str root                      root name for saving file
# list class Snap snapshots     list with all information about atoms
# str id1                       identifier for atom used as center (e.g. 'O_')
# str id2                       identifier for atoms as possible neighbors (e.g. 'H_')
# float cut (optional)          cutoff distance for neighbor search
#####
# OUTPUT
# list class Snap ion_comp      list of water complexes found
########################################################################################################################
def water_find_parallel(root, snapshots, id1, id2, cut=1.4):
    """
    Find water complexes for multiple snapshots of atomic configurations.

    Args:
        root (str): root name of the files
        snapshots (list[:class:`.Snap`]): list of snapshots containing the atomic information
        id1 (str): identifier for atom used as center (e.g. 'O_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'H_')
        cut (float): cutoff distance for neighbor search

    Returns:
        list[:class:`.Snap`]: list of snapshots containing water complexes

    Parallelization based on :py:mod:`multiprocessing`.
    """
    print("WATER COMPLEX DETECTION IN PROGRESS")
    # set other arguments (necessary for parallel computing)
    multi_one = partial(water_single, id1=id1, id2=id2, cut=cut)
    # run data extraction
    complex = progress.parallel_progbar(multi_one, snapshots)
    # create output file
    water_save(root, complex, id1, id2, cut)
    print("WATER COMPLEX DETECTION FINISHED")
    return complex



