"""
paw_structure.tra
-----------------
Trajectory file handling and data storage.

Dependencies:
:py:mod:`numpy`
:py:mod:`pandas`
:mod:`paw_structure.utility`

.. autosummary::
   :toctree: _generate

      Snap
      tra_strc_read
      tra_index
      tra_extract
      tra_read
      tra_save
      tra_load
"""

import numpy as np
import pandas as pd
# MODULES WITHIN PROJECT
from . import utility


########################################################################################################################
# CLASS FOR INFORMATION STORAGE
########################################################################################################################
# INPUT
# int iter                      iteration of data
# float time                    time of data
# ndarray(3,3) cell             unit cell of data
# ndarray(3,n) pos              atomic positions of data (select None if dataframe is given)
# dict atoms                    atomic information (name, id, index) (select None if dataframe is given)
# pandas DataFrame dataframe    contains atoms and pos input (selection with 'name', 'id', 'index', 'pos')
# dict hbonds                   hydrogen bond information
########################################################################################################################
class Snap:
    def __init__(self, iter, time, cell, pos, atoms, dataframe=None, hbonds=None):
        self.iter = iter
        self.time = time
        self.cell = cell
        if dataframe is None:  # initialization with numpy array
            pos = pd.DataFrame(pos, columns=['pos', 'pos', 'pos'], index=atoms.index)
            self.atoms = pd.concat([atoms, pos], axis=1, sort=False)
        else:  # initialization with DataFrame
            self.atoms = dataframe
        self.hbonds = hbonds


########################################################################################################################
# READ root.strc_out FILE TO OBTAIN ATOM IDENTIFIERS
########################################################################################################################
# INPUT
# str root              root name of the project
#####
# OUTPUT
# pandas DataFrame df   contains atom information ('name', 'id', 'index')
########################################################################################################################
def tra_strc_read(root):
    path = root + '.strc_out'
    # open file
    try:
        f = open(path)
    except IOError:
        utility.err_file('tra_strc_read', path)
    text = f.readlines()
    f.close()
    for i in range(len(text)):
        text[i] = text[i].split()  # split the lines gives list of the words
    atoms = {'name': [], 'id': [], 'index': []}  # dictionary for saving of information
    # find identifiers and index of atom (reflects order in root_r.tra file)
    # depends on format of .strc_out file (difference in lines is fixed)
    for i in range(len(text)):
        if text[i][0] == '!ATOM':
            atoms['name'].append(text[i+2][0].strip("\'"))  # save identifier of single atom
            atoms['id'].append(text[i + 8][0].strip("\'"))  # save identifier of atom type
            atoms['index'].append(np.int(text[i+12][0]))  # save index (for order in root_r.tra file
    # create pandas DataFrame object
    df = pd.DataFrame(data=atoms)
    # sort elements by index
    df = df.sort_values(by=['index'])
    return df


########################################################################################################################
# FIND INDICES OF SNAPSHOTS CLOSEST TO SELECTED TIMES
########################################################################################################################
# INPUT
# ndarray times     simulation times
# float t1          beginning of interval
# float t2          end of interval
# int n             number of snapshots
#####
# OUTPUT
# list int idx      index of selected snapshots
########################################################################################################################
def tra_index(times, t1, t2, n):
    times = np.asarray(times)  # times is array of actual simulation times
    # catch wrong input
    if n > len(times):
        utility.err('tra_index', 0, [n, len(times)])
    if t2 < t1:
        utility.err('tra_index', 1, [t1, t2])
    if t1 < times[0] or t1 > times[-1]:
        utility.err('tra_index', 2, [t1, t2, times[0], times[-1]])
    if t2 > times[-1] or t2 < times[0]:
        utility.err('tra_index', 2, [t1, t2, times[0], times[-1]])
    snapshot = np.linspace(t1, t2, n)  # equi-distant array of snapshot times
    # index of simulation step closest to snapshot times
    idx = [(np.abs(times - snap)).argmin() for snap in snapshot]
    # catching double selection
    if len(idx) > len(set(idx)):
        utility.err('tra_index', 3, [n, idx[-1] - idx[0]])
    return idx


########################################################################################################################
# EXTRACT RAW DATA FROM TRAJECTORY FILE
########################################################################################################################
# INPUT
# str root          root name of the project
# int n_atoms       number of atoms per snapshot
#####
# OUTPUT
# ndarray data      data structure containing information
########################################################################################################################
def tra_extract(root, n_atoms):
    path = root + '_r.tra'
    tau = 2.418884E-05  # converts a.u. (time) into ps
    angstrom = 0.52917721  # converts Bohr radius into Angstrom
    # define structure for reading data
    form = np.dtype([('num', np.int32),
                     ('iter', np.int32),
                     ('time', np.float64),
                     ('len', np.int32),
                     ('cell', np.float64, (3, 3)),  # TODO: not sure if cell is correctly converted or transpose is necessary
                     ('pos', np.float64, (n_atoms, 3)),
                     ('q', np.float64, (n_atoms, 1)),
                     ('qm', np.float64, (n_atoms, 4)),
                     ('num2', np.int32)])
    try:
        data = np.fromfile(path, dtype=form, count=-1, offset=0)  # read all of root_r.tra file
    except FileNotFoundError:
        utility.err_file('tra_extract', path)
    data['time'] = data['time'] * tau  # convert times into ps
    data['cell'] = data['cell'] * angstrom  # convert unit cell into Angstrom
    data['pos'] = data['pos'] * angstrom # convert atomic positions into Angstrom
    return data


########################################################################################################################
# READ TRAJECTORY FILE, MAKE SELECTION OF SNAPSHOTS AND RETURN DATA
########################################################################################################################
# INPUT
# str root                      root name of project
# float t1                      beginning of interval
# float t2                      end of interval
# int n                         number of atoms per snapshot
#####
# OUTPUT
# list class Snap snapshots     list of data structures, each ones describes one snapshot
########################################################################################################################
def tra_read(root, t1, t2, n):
    atoms = tra_strc_read(root)  # get atom identifiers
    n_atoms = len(atoms['index'].values)  # get number of atoms
    data = tra_extract(root, n_atoms)  # read trajectory file
    select = tra_index(data['time'], t1, t2, n)  # select snapshots for analysis
    data = data[select]
    snapshots = []
    # initialize Snap data structure for each snapshot
    for i in range(len(data['time'])):
        snapshots.append(Snap(data['iter'][i], data['time'][i], data['cell'][i], data['pos'][i], atoms))
    return snapshots


########################################################################################################################
# SAVE INFORMATION OF SELECTED SNAPSHOTS TO FILE root.snap
########################################################################################################################
# INPUT
# str root                      root name of project
# list class Snap snapshots     data for every selected snapshot
########################################################################################################################
# TODO: losing information about unit cell size for each time step (only constant unit cell works)
def tra_save(root, snapshots):
    # open file
    path = root + '.snap'
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('tra_save', path)
    # write header
    f.write("SELECTED SNAPSHOTS FROM TRAJECTORY FILE\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))  # start time
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))  # end time
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))  # number of snapshots
    f.write("%-14s%14d\n" % ("ATOMS", len(snapshots[0].atoms)))  # atoms per snapshot
    f.write("%-14s\n" % ("UNIT CELL"))  # unit cell
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    # write information for different time steps
    for snap in snapshots:
        f.write("-" * 72 + "\n")
        # time and iteration of snapshot
        f.write("%-14s%-14.8f%-14s%-14d\n" % ("TIME", snap.time, "ITERATION", snap.iter))
        # atomic information
        f.write("%-14s%-14s%-14s%14s%14s%14s\n" % ('NAME', 'ID', 'INDEX', 'X', 'Y', 'Z'))
        np.savetxt(f, snap.atoms.values, fmt="%-14s%-14s%-14d%14.8f%14.8f%14.8f")
    f.close()


########################################################################################################################
# LOAD root.snap FILE PRODUCED BY tra.save()
# WARNING: READING IS LINE SENSITIVE! ONLY USE ON UNCHANGED FILES WRITTEN BY tra_save()
# TODO: remove line sensitivity
########################################################################################################################
# INPUT
# str root                      root name of project
#####
# OUTPUT
# list class Snap snapshots     data for every selected snapshot
########################################################################################################################
def tra_load(root):
    path = root + '.snap'
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('tra_load', path)
    text = f.readlines()  # read text as lines
    for i in range(len(text)):
        text[i] = text[i].split()  # split each line into list with strings as elements
    snapshots = []  # storage list
    n_atoms = int(text[4][1])  # get number of atoms
    cell = np.array(text[6:9], dtype=float)  # get unit cell
    for i in range(len(text)):
        if text[i][0] == "TIME":  # search for trigger of new snapshot
            iter = int(text[i][3])
            time = float(text[i][1])
            test = np.array(text[i+2:i+2+n_atoms])
            atoms = {}
            atoms['name'] = test[:, 0]
            atoms['id'] = test[:, 1]
            atoms['index'] = np.array(test[:, 2], dtype=int)
            df = pd.DataFrame(data=atoms)
            # save information as class Snap
            snapshots.append(Snap(iter, time, cell, np.array(test[:, 3:6], dtype=np.float64), df))
    return snapshots
