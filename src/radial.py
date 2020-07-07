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
:mod:`paw_structure.pbc`
:mod:`paw_structure.utility`

.. autosummary::
   :toctree: _generate

      radial_distance_single
      radial_distance
      radial_distance_wrapper
      radial_distance_parallel
      radial_calculate
      radial_integrate
      radial_plot
      radial_save
      radial_load
"""

import numpy as np
from functools import partial
import miniutils.progress_bar as progress
import matplotlib.pyplot as plt
import matplotlib
from scipy.ndimage.interpolation import shift
import scipy.integrate as si

from . import utility
from . import pbc




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
def radial_distance_single(center, pbc_atoms, cut):
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
def radial_distance(snap, id1, id2, cut, names=None):
    # create 3x3 unit cell to account for periodic boundary conditions
    pbc_atoms = pbc.pbc_apply3x3(snap, id=[id2])
    distances = []
    if names is None:
        # loop through atoms with id1
        for index, row in snap.atoms.iterrows():
            if row['id'] == id1:
                dist = radial_distance_single(row, pbc_atoms, cut)
                # store distances
                dist = dist.tolist()
                distances += dist
    else:
        # loop through atoms in names
        for index, row in snap.atoms.iterrows():
            if row['name'] in names:
                dist = radial_distance_single(row, pbc_atoms, cut)
                # store distances
                dist = dist.tolist()
                distances += dist
    return distances


########################################################################################################################
# WRAPPER FOR PARALLEL DISTANCE SEARCH
# HELPER FUNCTION TO FIND DISTANCES FOR SINGLE SNAPSHOT (NECESSARY FOR PARALLEL COMPUTING)
########################################################################################################################
# INPUT
# class Snap snap           snapshot with all information
# str id1                   identifier for atoms used as center (e.g. 'MN', 'H_' or 'O_')
# str id2                   identifier for atoms used as potential neighbors
# float cut                 cutoff distance for search
# list str names (optional) use names (e.g. 'O_43', 'H_23') of atoms as center instead of identifiers (replaces id1)
#####
# OUTPUT
# list float dist           list of distances found which are smaller than cut
########################################################################################################################
def radial_distance_wrapper(snap, id1, id2, cut, names=None):
    dist = radial_distance(snap, id1, id2, cut, names=names)
    return dist


########################################################################################################################
# FIND DISTANCES FOR MULTIPLE SNAPSHOTS FOR RADIAL DISTRIBUTION FUNCTION COMPUTATION
########################################################################################################################
# INPUT
# list class Snap snapshots     list with all information about atoms
# str id1                       identifier for atoms used as center (e.g. 'MN', 'H_' or 'O_')
# str id2                       identifier for atoms used as potential neighbors
# float cut                     cutoff distance for search
# list str names (optional)     use names (e.g. 'O_43', 'H_23') of atoms as center instead of identifiers (replaces id1)
#####
# OUTPUT
# list list float radial_dist   list contains lists of distances found which are smaller than cut
#                                   (one for each snapshot)
########################################################################################################################
def radial_distance_parallel(snapshots, id1, id2, cut, names=None):
    # set other arguments (necessary for parallel computing)
    multi_one = partial(radial_distance, id1=id1, id2=id2, cut=cut, names=names)
    # run data extraction
    radial_dist = progress.parallel_progbar(multi_one, snapshots)
    return radial_dist


########################################################################################################################
# ROUTINE TO CALCULATE RADIAL DISTRIBUTION FUNCTION
# WARNING: USAGE OF names IS NOT IMPLEMENTED YET
# TODO: implement usage of names
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
    print("RDF CALCULATION IN PROGRESS")
    # calculate distances
    radial_dist = radial_distance_parallel(snapshots, id1, id2, cut, names=names)
    # combine the list of lists into a flat array
    radial_dist = np.array([y for x in radial_dist for y in x])
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
    print("RDF CALCULATION FINISHED")
    return radius, rdf, rho


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
    int_count = rdf * radius * radius
    integration = si.cumtrapz(int_count, x=radius)
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
    matplotlib.rcParams.update({'font.size': 14})
    plt.figure()
    plt.plot(radius, rdf)
    if integration is not None:
        plt.plot(radius[1:], integration)
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
# str id1                       identifier for atoms used as center (e.g. 'MN', 'H_' or 'O_')
# str id2                       identifier for atoms used as potential neighbors
# float cut                     cutoff distance for search
# int nbins                     number of bins used to sort the data into a histogram
# float rho                     overall density of atom type id2 (needed for later integration)
# str ext (optional)            extension for the saved file: name = root + ext
########################################################################################################################
def radial_save(root, radius, rdf, snapshots, id1, id2, cut, nbins, rho, ext='.radial'):
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
    f.write("\n%14s%14s\n" % ("RADIUS", "RDF"))
    data = np.vstack((radius, rdf))
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
            if text[i] == ['RADIUS', 'RDF']:
                data = np.array(text[i+1:], dtype=float)
                break
    return data, rho
