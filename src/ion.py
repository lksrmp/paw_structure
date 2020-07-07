"""
ion
___
.. module:: ion

Ion complex search
"""

import numpy as np
import pandas as pd
from functools import partial
import miniutils.progress_bar as progress
# MODULES WITHIN PROJECT
from . import neighbor
from . import utility
from .tra import Snap



########################################################################################################################
# FIND ION COMPLEX FOR A SINGLE SNAPSHOT
########################################################################################################################
# INPUT
# class Snap snap   snapshot containing all information
# str id1           identifier for atom used as center (e.g. 'MN'); only one allowed to be in snap
# TODO: change id1 to name to avoid error when two atoms with id1 are present
# str id2           identifier for atoms as possible first neighbors (e.g. 'O_')
# str id3           identifier for atoms as possible neighbors of first neighbors (e.g. 'H_')
# float cut1        cutoff distance for first neighbor search
# float cut2        cutoff distance for second neighbor search
#####
# OUTPUT
# pandas DataFrame  contains the whole complex centered around id1
########################################################################################################################
def ion_single(snap, id1, id2, id3, cut1, cut2):
    # check if only one atom is selected as ion
    if len(snap.atoms[snap.atoms['id'] == id1]) != 1:
        utility.err('ion_single', 0, [len(snap.atoms[snap.atoms['id'] == id1])])
    # check if all three are different species
    if id1 == id2 or id2 == id3 or id1 == id3:
        utility.err('ion_single', 1, [id1, id2, id3])
    # search first neighbors
    next1 = neighbor.neighbor_find_name(snap, id1, id2, cut1)
    # extract name lists
    id1_list = [atom[0] for atom in next1]
    id2_list = [y for x in [atom[1:] for atom in next1] for y in x]
    # search second neighbors
    next2 = neighbor.neighbor_find_name(snap, id2, id3, cut2, names=id2_list)
    # extract name list
    id3_list = [y for x in [atom[1:] for atom in next2] for y in x]
    # extract correct atom information
    id1_list = snap.atoms.loc[snap.atoms['name'].isin(id1_list)]
    id2_list = snap.atoms.loc[snap.atoms['name'].isin(id2_list)]
    id3_list = snap.atoms.loc[snap.atoms['name'].isin(id3_list)]
    return pd.concat([id1_list, id2_list, id3_list])


########################################################################################################################
# SAVE INFORMATION FROM ion_find TO FILE <root>.ext FOR LATER ANALYSIS
# TODO: check if snapshots is empty
########################################################################################################################
# INPUT
# str root                      root name for saving file
# list class Snap snapshots     list with information to be saved
# str id1                       identifier for atom used as center (e.g. 'MN'); only one allowed to be in snap
# str id2                       identifier for atoms as possible first neighbors (e.g. 'O_')
# str id3                       identifier for atoms as possible neighbors of first neighbors (e.g. 'H_')
# float cut1                    cutoff distance for first neighbor search
# float cut2                    cutoff distance for second neighbor search
# str ext (optional)            extension for the saved file: name = root + ext
########################################################################################################################
def ion_save(root, snapshots, id1, id2, id3, cut1, cut2, ext='.ion'):
    # open file
    path = root + ext
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('ion_save', path)
    # write header
    f.write("ION COMPLEXES\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
    f.write("%-14s%14s\n" % ("ID1", id1))
    f.write("%-14s%14s\n" % ("ID2", id2))
    f.write("%-14s%14s\n" % ("ID3", id3))
    f.write("%-14s%14.8f\n" % ("CUT1", cut1))
    f.write("%-14s%14.8f\n" % ("CUT2", cut2))
    f.write("%-14s\n" % ("UNIT CELL"))
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
# LOAD INFORMATION PREVIOUSLY SAVED BY ion_save()
# WARNING: READING IS LINE SENSITIVE! ONLY USE ON UNCHANGED FILES WRITTEN BY ion_save()
# TODO: remove line sensitivity
########################################################################################################################
# INPUT
# str root                      root name for the file to be loaded
# str ext (optional)            extension for the file to be loaded: name = root + ext
#####
# OUTPUT
# list class Snap snapshots     list of all information
########################################################################################################################
def ion_load(root, ext='.ion'):
    path = root + ext
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('ion_load', path)
    text = f.readlines()  # read text as lines
    for i in range(len(text)):
        text[i] = text[i].split()  # split each line into list with strings as elements
    snapshots = []  # storage list
    cell = np.array(text[10:13], dtype=float)  # get unit cell
    for i in range(len(text)):
        if text[i][0] == "TIME":  # search for trigger of new snapshot
            iter = int(text[i][3])
            time = float(text[i][1])
            n_atoms = int(text[i][5])
            test = np.array(text[i + 2:i + 2 + n_atoms])
            atoms = {}
            atoms['name'] = test[:, 0]
            atoms['id'] = test[:, 1]
            atoms['index'] = np.array(test[:, 2], dtype=int)
            df = pd.DataFrame(data=atoms)
            # save information as class Snap
            snapshots.append(Snap(iter, time, cell, np.array(test[:, 3:6], dtype=np.float64), df))
    return snapshots


########################################################################################################################
# FIND ION COMPLEXES IN MULTIPLE SNAPSHOTS
# WARNING: NOT IN USE BECAUSE NO PARALLEL COMPUTING
########################################################################################################################
# INPUT
# str root                      root name for saving file
# list class Snap snapshots     list with information to be saved
# str id1                       identifier for atom used as center (e.g. 'MN'); only one allowed to be in snap
# str id2                       identifier for atoms as possible first neighbors (e.g. 'O_')
# str id3                       identifier for atoms as possible neighbors of first neighbors (e.g. 'H_')
# float cut1 (optional)         cutoff distance for first neighbor search
# float cut2 (optional)         cutoff distance for second neighbor search
#####
# OUTPUT
# list class Snap complex       list with all ion complexes found
########################################################################################################################
# def ion_find(root, snapshots, id1, id2, id3, cut1=3.0, cut2=1.4):
#     complex = []
#     # loop through different snapshots
#     for snap in snapshots:
#         # get complex information
#         comp = ion_single(snap, id1, id2, id3, cut1, cut2)
#         # append Snap object for data storage
#         complex.append(Snap(snap.iter, snap.time, snap.cell, None, None, dataframe=comp))
#     # save information to file
#     ion_save(root, complex, id1, id2, id3, cut1, cut2)
#     return complex


########################################################################################################################
# WRAPPER FOR THE PARALLEL VERSIONS OF ion_find
# HELPER FUNCTION TO FIND ION COMPLEX FOR SINGLE SNAPSHOT (NECESSARY FOR PARALLEL COMPUTING)
########################################################################################################################
# INPUT
# class Snap snap
# str id1               identifier for atom used as center (e.g. 'MN'); only one allowed to be in snap
# str id2               identifier for atoms as possible first neighbors (e.g. 'O_')
# str id3               identifier for atoms as possible neighbors of first neighbors (e.g. 'H_')
# float cut1            cutoff distance for first neighbor search
# float cut2            cutoff distance for second neighbor search
#####
# OUTPUT
# class Snap res        ion complex information extracted from snap
########################################################################################################################
def ion_find_wrapper(snap, id1, id2, id3, cut1, cut2):
    comp = ion_single(snap, id1, id2, id3, cut1, cut2)  # find ion complex as pandas DataFrame
    # create new class Snap with ion complex information
    res = Snap(snap.iter, snap.time, snap.cell, None, None, dataframe=comp)
    return res


########################################################################################################################
# ROUTINE TO FIND ION COMPLEXES FOR MULTIPLE SNAPSHOTS
# PARALLEL VERSION OF ion_find() WITH PROGRESS BAR IN CONSOLE
########################################################################################################################
# INPUT
# str root                      root name for saving file
# list class Snap snapshots     list with information to be saved
# str id1                       identifier for atom used as center (e.g. 'MN'); only one allowed to be in snap
# str id2                       identifier for atoms as possible first neighbors (e.g. 'O_')
# str id3                       identifier for atoms as possible neighbors of first neighbors (e.g. 'H_')
# float cut1 (optional)         cutoff distance for first neighbor search
# float cut2 (optional)         cutoff distance for second neighbor search
#####
# OUTPUT
# list class Snap ion_comp      list of ion complexes found
########################################################################################################################
def ion_find_parallel(root, snapshots, id1, id2, id3, cut1=3.0, cut2=1.4):
    print("ION COMPLEX DETECTION IN PROGRESS")
    # set other arguments (necessary for parallel computing)
    multi_one = partial(ion_find_wrapper, id1=id1, id2=id2, id3=id3, cut1=cut1, cut2=cut2)
    # run data extraction
    ion_comp = progress.parallel_progbar(multi_one, snapshots)
    # create output file
    ion_save(root, ion_comp, id1, id2, id3, cut1, cut2)
    print("ION COMPLEX DETECTION FINISHED")
    return ion_comp