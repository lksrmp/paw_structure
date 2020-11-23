"""
paw_structure.tra
-----------------
Trajectory file handling and data storage.

Dependencies:
    :py:mod:`numpy`
    :py:mod:`pandas`
    :mod:`.utility`

.. autosummary::

      Snap
      tra_clean
      tra_detect_change
      tra_extract
      tra_index
      tra_load
      tra_number_atoms
      tra_read
      tra_save
      tra_strc_read
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
# ndarray(3,n) pos              atomic positions of data (select **None** if dataframe is given)
# dict atoms                    atomic information (name, id, index) (select **None** if dataframe is given)
# pandas DataFrame dataframe    contains atoms and pos input (selection with 'name', 'id', 'index', 'pos')
# dict hbonds                   hydrogen bond information
########################################################################################################################
class Snap:
    """
    Information storage.

    Contains the relevant information for one snapshot taken from the simulation.

    Args:
        iter (int): iteration in simulation
        time (float): time [ps] in simulation
        cell (ndarray[float]): 3x3 array containing the unit cell of simulation
        pos (ndarray[float]): 3xN array containing atomic positions (select **None** if :data:`dataframe` is given)
        atoms (dict): atomic information (name, id, index) (select **None** if :data:`dataframe` is given)
        dataframe (pandas DataFrame, optional): contains :data:`atoms` and :data:`pos` input (selection with 'name', 'id', 'index', 'pos')
        hbonds (dict, optional): NOT IN USE; hydrogen bond information

    Attributes:
        iter (int): see above
        time (float): see above
        cell (ndarray[float]): see above
        atoms (pandas DataFrame): combination of :data:`atoms` and :data:`pos` input or equal to :data:`dataframe` input if given
        hbonds (dict, optional): default is **None**
    """
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
    """
    Read ".strc_out" file to obtain atom identifiers.

    Necessary to correctly identify atomic positions extracted from the trajectory file.

    Args:
        root (str): root name of the file

    Returns:
        pandas DataFrame: contains information 'name', 'id', 'index' of all the atoms
    """
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
    """
    Indices of snapshots closest to equally spaced times in a given interval.

    Args:
        times (ndarray[float]): simulation times
        t1 (float): beginning of interval
        t2 (float): end of interval
        n (int): number of wanted snapshots

    Returns:
        list[int]: index of the selected snapshots

    Todo:
        Check behaviour for when selected snapshots are really close to each other.
    """
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
    counter = 0
    idx = []
    for i in range(1, len(times)):
        if (times[i] - snapshot[counter]) > 0:
            if np.abs(times[i-1] - snapshot[counter]) < (times[i] - snapshot[counter]):
                idx.append(i - 1)
                counter += 1
                if counter == len(snapshot):
                    break
            else:
                idx.append(i)
                counter += 1
                if counter == len(snapshot):
                    break
    if len(idx) > len(set(idx)):
        utility.err('tra_index', 3, [n, idx[-1] - idx[0]])

    # inefficient version
    # idx = [(np.abs(times - snap)).argmin() for snap in snapshot]
    # catching double selection
    # if len(idx) > len(set(idx)):
    #     utility.err('tra_index', 3, [n, idx[-1] - idx[0]])
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
    """
    Extract raw data from trajectory file "_r.tra".

    Args:
        root (str): root name of the trajectory file
        n_atoms (int): number of atoms per snapshot

    Returns:
        ndarray: data structure containing information

    For formatting of the trajectory file please see the manual for the CP-PAW_ code by Peter Blöchl.

    .. _CP-PAW: https://www2.pt.tu-clausthal.de/paw/

    The units are transformed into ps (time) and Angstrom (distance) at this step.

    Todo:
        Unit cell reading not clear if correct or transpose (not relevant for simple cubic).
    """
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


def tra_clean(data):
    """
    Remove doubled simulation time intervals coming from the trajectory file.

    Args:
        data (ndarray): data structure output from :func:`.tra_extract`

    Returns:
        ndarray: data structure without doubled simulation times

    Occasions where the iteration changes by a value smaller 1 (also negative) are detected. The interval previous to
    that point which appears a second time later on is deleted. This procedure is recursive such that the latest
    simulations interval is kept.

    .. figure:: ../Images/tra_clean.png
        :width: 400
        :align: center
        :alt: tra_clean illustration
        :figclass: align-center

        Removing doubled simulation times.

    Note:
        Positive jumps as in skipping iterations steps are not accounted for.

    Todo:
        Test if more than one jump and convoluted jumps work.
    """
    # detect negative iteration jumps
    shift = np.diff(data['iter'])
    # find position in array
    jumps = np.where(shift < 1)
    # if no jumps are found, return
    if len(jumps[0]) == 0:
        return data
    # if some are found
    else:
        # find position of double before the jump to determine the interval to be deleted
        overlap = np.where(data['iter'][:jumps[0][0]] == data['iter'][jumps[0][0] + 1])
        print("NEGATIVE ITERATION JUMP IN DATA DETECTED\nFROM %d TO %d\nREMOVING OVERLAP"
              % (data['iter'][jumps[0][0]], data['iter'][jumps[0][0] + 1]))
        # recursively go through all jumps present
        return tra_clean(np.delete(data, np.s_[overlap[0][0]:jumps[0][0] + 1], 0))


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
    """
    Read the trajectory file and extract relevant information for selected snapshots.

    Args:
        root (str): root name of the trajectory file
        t1 (float): beginning of interval
        t2 (float): end of interval
        n (int): number of wanted snapshots

    Returns:
        list[:class:`.Snap`]: snapshots extracted from the trajectory file
    """
    print("READING TRAJECTORY FILE")
    atoms = tra_strc_read(root)  # get atom identifiers
    n_atoms = len(atoms['index'].values)  # get number of atoms
    data = tra_extract(root, n_atoms)  # read trajectory file
    data = tra_clean(data)  # removed doubled time intervals
    select = tra_index(data['time'], t1, t2, n)  # select snapshots for analysis
    data = data[select]
    snapshots = []
    # initialize Snap data structure for each snapshot
    print("INITIALIZING DATA STRUCTURES")
    for i in range(len(data['time'])):
        snapshots.append(Snap(data['iter'][i], data['time'][i], data['cell'][i], data['pos'][i], atoms))
    print("FINISHED READING TRAJECTORY FILE")
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
    """
    Save information of selected snapshots to file :ref:`Output_snap`.

    Args:
        root (str): root name for file
        snapshots (list[:class:`.Snap`]): snapshots to be saved

    Note:
        Not suitable for dynamic / changing unit cells.

    Todo:
        Implement variable unit cell.
    """
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
        f.write("-" * 84 + "\n")
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
    """
    Load information from the :ref:`Output_snap` file previously created by :func:`.tra_save`.

    Args:
        root (root): root name of file

    Returns:
        list[:class:`.Snap`]: snapshots loaded from file

    Note:
        Reading is line sensitive. Do not alter the output file before loading.

    Todo:
        Remove line sensitivity.
    """
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


def tra_number_atoms(snapshots):
    """
    Get atom number, time and iteration from multiple snapshots.

    Args:
        snapshots (list[:class:`.Snap`]): snapshots the atomic information

    Returns:
        (tuple): tuple containing:

            - list[int]: number of atoms in each snapshot
            - list[float]: time in simulation of the snapshots
            - list[int]: iteration in simulation of the snapshots
    """
    atoms = []
    times = []
    iterations = []
    # loop through snapshots and save information to list
    for i in range(len(snapshots)):
        atoms.append(len(snapshots[i].atoms))
        times.append(snapshots[i].time)
        iterations.append(snapshots[i].iter)
    return atoms, times, iterations


def tra_detect_change(snapshots):
    """
    Detect changes in atoms contained in a snapshot and save index of snapshots between which the change occurs.

    Args:
        snapshots (list[:class:`.Snap`]): snapshots containing the atoms

    Returns:
        ndarray[int]: indices of snapshots where atoms change
    """
    idx_change = []
    for i in range(len(snapshots) - 1):
        # check if atom number changes
        if len(snapshots[i].atoms['name'].values) != len(snapshots[i + 1].atoms['name'].values):
            idx_change.append(i)
            idx_change.append(i + 1)
        # check if atom names change
        else:
            if not (snapshots[i].atoms['name'].values == snapshots[i + 1].atoms['name'].values).all():
                idx_change.append(i)
                idx_change.append(i + 1)
    return np.unique(idx_change)