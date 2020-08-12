"""
paw_structure.radial
--------------------
Radial distribution function calculation.

Dependencies:
    :py:mod:`functools`
    :py:mod:`matplotlib`
    :py:mod:`miniutils.progress_bar`
    :py:mod:`numpy`
    :py:mod:`pandas`
    :py:mod:`scipy`
    :mod:`.pbc`
    :mod:`.utility`
    :mod:`.radial_c`

.. autosummary::

      radial_calculate
      radial_distance
      radial_integrate
      radial_load
      radial_plot
      radial_save
      radial_single
      radial_single_c
"""

import numpy as np
from functools import partial
import miniutils.progress_bar as progress
import matplotlib.pyplot as plt
import matplotlib
import scipy.integrate as si

from . import utility
from . import pbc

from . import radial_c


########################################################################################################################
# FIND DISTANCES SMALLER THAN A CUTOFF DISTANCE
########################################################################################################################
# INPUT
# pandas DataFrame center       central atom of reference
# pandas DataFrame pbc_atoms    atoms as possible neighbors
# float cut                     cutoff distance
#####
# OUTPUT
# ndarray float                 distances found which are smaller than cutoff distance
########################################################################################################################
def radial_distance(center, pbc_atoms, cut):
    """
    Find distance values smaller than a cutoff distance.

    Note:
        Not in use. Replaced by C++ routines.

    Args:
        center (:py:mod:`pandas.DataFrame`): central atom of reference
        pbc_atoms (:py:mod:`pandas.DataFrame`): atoms as possible neighbors
        cut (float): cutoff distance

    Returns:
        ndarray[float]: distances found which are smaller than cutoff distance
    """
    dist = np.linalg.norm(center['pos'] - pbc_atoms['pos'], axis=1)  # calculate distance to center
    # select distances smaller than cut and not close to 0 to avoid finding the center itself
    return dist[[a and not b for a, b in zip(dist < cut, np.isclose(dist, 0.0))]]


########################################################################################################################
# COLLECT DISTANCES FOR ALL ATOMS OF TYPE id1
########################################################################################################################
# INPUT
# class Snap snap           snapshot with all information
# str id1                   identifier for atoms used as center (e.g. 'MN', 'H_' or 'O_')
# str id2                   identifier for atoms used as potential neighbors
# float cut                 cutoff distance for search
# list str names (optional) use names (e.g. 'O_43', 'H_23') of atoms as center instead of identifiers (replaces id1)
#####
# OUTPUT
# list float distances      list of distances found which are smaller than cut
########################################################################################################################
def radial_single(snap, id1, id2, cut, names=None):
    """
    Collect distances between all atoms of type :data:`id1` and type :data:`id2`.
    If :data:`names` is given, those atoms are used as centers instead of :data:`id1`.

    Note:
        Not in use. Replaced by C++ routines.

    Args:
        snap (:class:`.Snap`): single snapshot containing the atomic information
        id1 (str): identifier for atoms used as center (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for radial calculation
        names (list[str], optional): names of atoms to use as centers (e.g. 'O\_43', 'H\_23')

    Returns:
        list[float]: list of distances found which are smaller than :data:`cut`
    """
    # create 3x3 unit cell to account for periodic boundary conditions
    pbc_atoms = pbc.pbc_apply3x3(snap, id=[id2])
    distances = []
    if names is None:
        # loop through atoms with id1
        for index, row in snap.atoms.iterrows():
            if row['id'] == id1:
                dist = radial_distance(row, pbc_atoms, cut)
                # store distances
                dist = dist.tolist()
                distances += dist
    else:
        # loop through atoms in names
        for index, row in snap.atoms.iterrows():
            if row['name'] in names:
                dist = radial_distance(row, pbc_atoms, cut)
                # store distances
                dist = dist.tolist()
                distances += dist
    return distances


def radial_single_c(snap, id1, id2, cut, names=None):
    """
    Binding of C++ routines for distance calculation of a single snapshot.

    Args:
        snap (:class:`.Snap`): single snapshot containing the atomic information
        id1 (str): identifier for atoms used as center (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for radial calculation
        names (list[str], optional): names of atoms to use as centers (e.g. 'O\_43', 'H\_23')

    Returns:
        list[float]: list of distances found which are smaller than :data:`cut`

    """
    if names is None:
        # transform atomic coordinates into necessary shape
        atoms1 = snap.atoms[snap.atoms['id'] == id1]['pos'].values
        atoms1 = atoms1.reshape(len(atoms1) * 3)
        atoms2 = snap.atoms[snap.atoms['id'] == id2]['pos'].values
        atoms2 = atoms2.reshape(len(atoms2) * 3)
        cell = snap.cell.reshape(9)
        dist = radial_c.radial(atoms1, atoms2, cut, cell)
    else:
        # transform atomic coordinates into necessary shape
        atoms1 = snap.atoms[snap.atoms['name'].isin(names)]['pos'].values
        atoms1 = atoms1.reshape(len(atoms1) * 3)
        atoms2 = snap.atoms[snap.atoms['id'] == id2]['pos'].values
        atoms2 = atoms2.reshape(len(atoms2) * 3)
        cell = snap.cell.reshape(9)
        dist = radial_c.radial(atoms1, atoms2, cut, cell)
    return dist


########################################################################################################################
# ROUTINE TO CALCULATE RADIAL DISTRIBUTION FUNCTION
# WARNING: USAGE OF names IS NOT IMPLEMENTED YET
########################################################################################################################
# INPUT
# list class Snap snapshots     list with all information about atoms
# str id1                       identifier for atoms used as center (e.g. 'MN', 'H_' or 'O_')
# str id2                       identifier for atoms used as potential neighbors
# float cut                     cutoff distance for search
# int nbins                     number of bins used to sort the data into a histogram
# list str names (optional)     use names (e.g. 'O_43', 'H_23') of atoms as center instead of identifiers (replaces id1)
#####
# OUTPUT
# ndarray float radius          different radii from radial distribution function calculation
# ndarray float rdf             radial distribution function corresponding to radii
# float rho                     overall density of atom type id2 (needed for later integration)
########################################################################################################################
def radial_calculate(snapshots, id1, id2, cut, nbins, names=None):
    """
    Calculate the radial distribution function (rdf) including multiple snapshots.

    Args:
        snapshots (list[:class:`.Snap`]): list of snapshots containing the atomic information
        id1 (str): identifier for atoms used as centers (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for radial calculation
        nbins (int): number of radius intervals; influences resolutions together with :data:`cut`
        names (list[str], optional): NOT IN USE; names of atoms to use as centers (e.g. 'O\_43', 'H\_23')

    Returns:
        (tuple): tuple containing:

            - ndarray[float]: radii used for rdf calculation
            - ndarray[float]: value of rdf corresponding to these radii
            - ndarray[float]: value of coordination number corresponding to these radii
            - float: average atom density of type :data:`id2`

    Todo:
        Implement usage of :data:`names`.
        Make single snapshot possible.
    """
    print("RDF CALCULATION IN PROGRESS")

    # calculate distances

    # Python code
    # multi_one = partial(radial_single, id1=id1, id2=id2, cut=cut, names=names)
    # C++ code
    multi_one = partial(radial_single_c, id1=id1, id2=id2, cut=cut, names=names)
    radial_dist = progress.parallel_progbar(multi_one, snapshots)

    # combine the list of lists into a flat array
    radial_dist = np.array([y for x in radial_dist for y in x])
    # TODO: only works if N > 1
    # sort data in a histogram
    hist = np.histogram(radial_dist, bins=nbins, range=(0.0, cut), normed=False)
    # extract radius and radial distribution function
    rdf = hist[0]
    radius = hist[1][1:]
    # account for multiple reference centers and multiple snapshots
    if names is None:
        rdf = rdf / len(snapshots) / len(snapshots[0].atoms[snapshots[0].atoms['id'] == id1])
    else:
        rdf = rdf / len(snapshots) / len(snapshots[0].atoms[snapshots[0].atoms['name'].isin(names)])
    # volume of unit cell
    v_unit = np.linalg.det(snapshots[0].cell)  # not sure if correct for non orthogonal vectors
    # density of neighbor atoms (id2)
    rho = len(snapshots[0].atoms[snapshots[0].atoms['id'] == id2]) / v_unit
    volume = np.linspace(0.0, cut, nbins + 1)  # array of radii
    volume = 4.0 / 3.0 * np.pi * volume * volume * volume  # volume for each radius
    volume = np.diff(volume)  # difference of volumes to the previous radius
    rdf = rdf / volume / rho  # normalize rdf
    coord = radial_integrate(radius, rdf, rho)
    print("RDF CALCULATION FINISHED")
    return radius, rdf, coord, rho


########################################################################################################################
# INTEGRATION OF RADIAL DISTRIBUTION FUNCTION TO OBTAIN COORDINATION NUMBER
########################################################################################################################
# INPUT
# ndarray float radius          different radii from radial distribution function calculation
# ndarray float rdf             radial distribution function corresponding to radii
# float rho                     overall density of atom type id2 (needed for later integration)
#####
# OUTPUT
# ndarray float integration     coordination number for different radii
########################################################################################################################
def radial_integrate(radius, rdf, rho):
    """
    Integration of radial distribution function (rdf).

    Uses :py:func:`scipy.cumtrapz` for numerical integration.

    XXX REFERENCE TO COORDINATION NUMBER CALCULATION XXX

    Args:
        radius (ndarray[float]): radii used for rdf calculation
        rdf (ndarray[float]): value of rdf corresponding to these radii
        rho (float): average atom density of type :data:`id2`

    Returns:
        ndarray[float]: value of integration corresponding to the radii
    """
    int_count = rdf * radius * radius
    integration = si.cumtrapz(int_count, x=radius, initial=0.0)
    integration = 4.0 * np.pi * rho * integration
    return integration


########################################################################################################################
# PLOT RADIAL DISTRIBUTION FUNCTION (AND INTEGRATION IF WANTED)
########################################################################################################################
# INPUT
# ndarray float radius          different radii from radial distribution function calculation
# ndarray float rdf             radial distribution function corresponding to radii
# ndarray float integration     coordination number for different radii
########################################################################################################################
def radial_plot(radius, rdf, integration=None):
    """
    Plot the radial distribution function (rdf) and the coordination number integration if selected.

    Args:
        radius (ndarray[float]): radii used for rdf calculation
        rdf (ndarray[float]): value of rdf corresponding to these radii
        integration (ndarray[float], optional): coordination number for different radii

    Todo:
        Implement better display of plot. Spawn subprocess to let the core program finish?
    """
    matplotlib.rcParams.update({'font.size': 14})
    plt.figure()
    plt.plot(radius, rdf)
    if integration is not None:
        plt.plot(radius, integration)
    plt.grid()
    plt.xlabel("r [A]")
    plt.ylabel("g(r)")
    plt.show()
    return


########################################################################################################################
# SAVE RADIAL DISTRIBUTION FUNCTION
########################################################################################################################
# INPUT
# str root                      root name for saving file
# ndarray float radius          different radii from radial distribution function calculation
# ndarray float rdf             radial distribution function corresponding to radii
# ndarray float coord           coordination number corresponding to radii
# str id1                       identifier for atoms used as center (e.g. 'MN', 'H_' or 'O_')
# str id2                       identifier for atoms used as potential neighbors
# float cut                     cutoff distance for search
# int nbins                     number of bins used to sort the data into a histogram
# float rho                     overall density of atom type id2 (needed for later integration)
# str ext (optional)            extension for the saved file: name = root + ext
########################################################################################################################
def radial_save(root, radius, rdf, coord, snapshots, id1, id2, cut, nbins, rho, ext='.radial'):
    """
    Save results to file :ref:`Output_radial`.

    XXX REFERENCE TO EXPLANATION OF .radial FILE FORMAT

    Args:
        root (str): root name for saving file
        radius (ndarray[float]): radii used for rdf calculation
        rdf (ndarray[float]): value of rdf corresponding to these radii
        coord (ndarray[float]): coordination number obtained from integration of rdf
        snapshots (list[:class:`.Snap`]): list of snapshots containing the water complexes
        id1 (str): identifier for atoms used as centers (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for radial calculation
        nbins (int): number of radius intervals; influences resolutions together with :data:`cut`
        rho (float): average atom density of type :data:`id2`
        ext (str, optional): default ".radial" - extension for the saved file: name = root + ext
    """
    # open file
    path = root + ext
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('radial_save', path)
    # write header
    f.write("RADIAL DISTRIBUTION FUNCTION\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
    f.write("%-14s%14s\n" % ("ID1", id1))
    f.write("%-14s%14s\n" % ("ID2", id2))
    f.write("%-14s%14.8f\n" % ("CUT", cut))
    f.write("%-14s%14d\n" % ("NBINS", nbins))
    f.write("%-14s%14.8f\n" % ("RHO", rho))
    f.write("%-14s\n" % "UNIT CELL")
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    f.write("\n%14s%14s%14s\n" % ("RADIUS", "RDF", "COORDINATION"))
    data = np.vstack((radius, rdf, coord))
    np.savetxt(f, data.T, fmt="%14.8f")
    f.close()
    return


########################################################################################################################
# LOAD INFORMATION PREVIOUSLY SAVED BY radial_save()
########################################################################################################################
# INPUT
# str root              root name for the file to be loaded
# str ext (optional)    extension for the file to be loaded: name = root + ext
#####
# OUTPUT
# ndarray 2d data       array containing radii and radial distribution function
# float rho             overall density of atom type id2 (needed for later integration)
########################################################################################################################
def radial_load(root, ext='.radial'):
    """
    Load information previously saved by :func:`.radial_save`.

    Args:
        root (str): root name for the file to be loaded
        ext (str, optional): default ".radial" - extension for the file to be loaded: name = root + ext

    Returns:
        (tuple): touple containing:

            - ndarray(float): 2D array containing radii, values of rdf and coordination number
            - float: average atom density of type :data:`id2`
    """
    # open file
    path = root + ext
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('radial_load', path)
    text = f.readlines()  # read text as lines
    for i in range(len(text)):
        text[i] = text[i].split()  # split each line into list with strings as elements
    rho = 0
    for i in range(len(text)):
        if len(text[i]) > 1:
            # find density rho
            if text[i][0] == 'RHO':
                rho = float(text[i][1])
            # find beginning beginning of data
            if text[i] == ['RADIUS', 'RDF', 'COORDINATION']:
                data = np.array(text[i+1:], dtype=float)
                break
    return data, rho
