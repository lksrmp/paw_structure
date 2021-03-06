"""
paw_structure.angle
-------------------
Angle probability distribution calculation according to :ref:`selection<Control_ANGLE>`.

Main routine is :func:`.angle_calculate`.

.. _pybind11: https://pybind11.readthedocs.io/en/stable/

Utilizes C++ code connected by pybind11_ in :mod:`.angle_c`.

Dependencies:
    :py:mod:`cycler`
    :py:mod:`functools`
    :py:mod:`matplotlib`
    :py:mod:`miniutils`
    :py:mod:`numpy`
    :py:mod:`pandas`
    :py:mod:`scipy`
    :py:mod:`seaborn`
    :py:mod:`sys`
    :mod:`.utility`
    :mod:`.angle_c`

.. autosummary::

    angle_calculate
    angle_load
    angle_peak
    angle_plot
    angle_save
    angle_single_c
"""
from cycler import cycler
import numpy as np
from functools import partial
import miniutils.progress_bar as progress
import matplotlib.pyplot as plt
import matplotlib
import scipy.signal as signal
import seaborn as sns
import sys

from . import utility
from . import angle_c


def angle_single_c(snap, id1, id2, cut, names=None):
    """
    Binding of C++ routines in :mod:`.angle_c` for angle calculation of a single snapshot.

    Args:
        snap (:class:`.Snap`): single snapshot containing the atomic information
        id1 (str): identifier for atoms used as center (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for angle calculation
        names (list[str], optional): names of atoms to use as centers (e.g. 'O\_43', 'H\_23')

    Returns:
        list[float]: list of angles found between atoms closer than :data:`cut`

    """
    if names is None:
        # transform atomic coordinates into necessary shape
        atoms1 = snap.atoms[snap.atoms['id'] == id1]['pos'].values
        atoms1 = atoms1.reshape(len(atoms1) * 3)
        atoms2 = snap.atoms[snap.atoms['id'] == id2]['pos'].values
        atoms2 = atoms2.reshape(len(atoms2) * 3)
        cell = snap.cell.reshape(9)
        ang = angle_c.angle(atoms1, atoms2, cut, cell)
    else:
        # transform atomic coordinates into necessary shape
        atoms1 = snap.atoms[snap.atoms['name'].isin(names)]['pos'].values
        atoms1 = atoms1.reshape(len(atoms1) * 3)
        atoms2 = snap.atoms[snap.atoms['id'] == id2]['pos'].values
        atoms2 = atoms2.reshape(len(atoms2) * 3)
        cell = snap.cell.reshape(9)
        ang = angle_c.angle(atoms1, atoms2, cut, cell)
    return ang


def angle_calculate(snapshots, id1, id2, cut, nbins, names=None):
    """
    Calculate the angle distribution function (adf) including multiple snapshots.

    Args:
        snapshots (list[:class:`.Snap`]): list of snapshots containing the atomic information
        id1 (str): identifier for atoms used as centers (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for possible neighbors in angle calculation
        nbins (int): number of degree intervals; influences resolutions
        names (list[str], optional): NOT IN USE; names of atoms to use as centers (e.g. 'O\_43', 'H\_23')

    Returns:
        (tuple): tuple containing:

            - ndarray[float]: degree values corresponding to adf
            - ndarray[float]: value of adf corresponding to these degree values

    Todo:
        Implement usage of :data:`names`.
        Make single snapshot possible.
    """
    print("ADF CALCULATION IN PROGRESS")
    multi_one = partial(angle_single_c, id1=id1, id2=id2, cut=cut, names=names)
    angles = progress.parallel_progbar(multi_one, snapshots)
    # combine the list of lists into a flat array
    angles = np.array([y for x in angles for y in x])
    # TODO: only works if N > 1
    # sort data in a histogram
    hist = np.histogram(angles, bins=nbins, range=(0.0, 180.0), density=True)
    # extract radius and radial distribution function
    adf = hist[0]
    degree = hist[1][1:]
    # account for multiple reference centers and multiple snapshots
    #if names is None:
    #    adf = adf / len(snapshots) / len(snapshots[0].atoms[snapshots[0].atoms['id'] == id1])
    #else:
    #    adf = adf / len(snapshots) / len(snapshots[0].atoms[snapshots[0].atoms['name'].isin(names)])
    print("ADF CALCULATION FINISHED")
    return degree, adf


def angle_plot(args):
    """
    Plot the angle distribution function (adf).

    Args:
        args (:py:mod:`argparse` object): command line arguments
    """
    if args.latex:
        plt.rcParams.update(utility.tex_fonts)
        plt.figure(figsize=utility.set_size(args.latex[0], fraction=args.latex[1]))
        sns.set_theme()
        sns.set_style("whitegrid")
        sns.color_palette(palette='colorblind', n_colors=8)
        prop_cycle = plt.rcParams['axes.prop_cycle']
        prop_cycle = (prop_cycle + cycler(linestyle=['-', '--', ':', '-.', '-', '--', ':', '-.', '-', '--']))
        plt.rc('axes', prop_cycle=prop_cycle)
    else:
        matplotlib.rcParams.update({'font.size': 14})
        plt.figure()
    for name in args.angle:
        root = utility.argcheck([sys.argv[0], name], '.angle')
        data = angle_load(root)
        if args.latex:
            #label = root.replace("_", "\_")
            label = root
        else:
            label = root
        if args.sinus:
            data[:, 1] = data[:, 1] * np.sin(data[:, 0] / 180. * np.pi)
            data[:, 1] = data[:, 1] / np.trapz(data[:, 1], x=data[:, 0])
            plt.plot(data[:, 0], data[:, 1] , label=label)
        else:
            plt.plot(data[:, 0], data[:, 1], label=label)
        if args.fwhm:
            step = data[:, 0][1] - data[:, 0][0]
            peaks, fwhm = angle_peak(data[:, 0], data[:, 1])
            plt.plot(data[:, 0][peaks], data[:, 1][peaks], 'x', color='green')
            plt.hlines(fwhm[1], fwhm[2] * step, fwhm[3] * step)
    plt.grid(b=True)
    if args.key:
        plt.legend(frameon=True)
    if args.xlim:
        plt.xlim(args.xlim)
    if args.ylim:
        plt.ylim(args.ylim)
    else:
        plt.ylim(bottom=0.0)
    if args.latex:
        plt.xlabel(r'$\theta\;$[$^\circ$]')
        if args.sinus:
            plt.ylabel(r'$P(\theta)\sin(\theta)$')
        else:
            plt.ylabel(r'$P(\theta)$')
        fig_name = root + "_angle.pdf"
        plt.savefig(fig_name, format='pdf', bbox_inches='tight')
    else:
        plt.xlabel("angle [°]")
        plt.ylabel("ADF * sin [a.u.]")
        fig_name = root + "_angle.png"
        plt.savefig(fig_name, dpi=300.0)
    print('SAVING OF %s SUCCESSFUL' % fig_name)
    if args.plot:
        plt.show()
    return


def angle_peak(degree, adf):
    """
    Find peaks in angle distribution function.

    Uses :py:func:`scipy.signal.find_peaks` with :data:`distance=20` and :data:`prominence=1.0` to find the peaks.

    Uses :py:func:`scipy.signal.peak_width` to obtain :data:`FWHM`.

    Args:
        degree (ndarray[float]): degree used for adf calculation
        adf (ndarray[float]): value of adf corresponding to these degrees

    Returns:
        (tuple): tuple containing:

            - ndarray[float]: indices of peaks in rdf that satisfy given conditions
            - ndarray[float]: widths for each peak in samples
            - ndarray[float]: height of the contour lines at which the widths where evaluated
            - ndarray[float]: interpolated positions of left and right intersection points of a horizontal line at the respective evaluation height

    Todo:
        Find good parameters for peak detection.
    """
    print("PEAK DETECTION ANGLE DISTRIBUTION FUNCTION")
    print("%12s%12s%12s%12s" % ("POSITION", "HEIGHT", "FWHM", "CENTER"))
    peaks, _ = signal.find_peaks(adf, distance=20)
    results = signal.peak_widths(adf, peaks, rel_height=0.5)
    step = degree[1] - degree[0]
    for i in range(len(peaks)):
        print("%12f%12f%12f%12f" % (degree[peaks[i]], adf[peaks[i]], results[0][i] * step,
                                    results[2][i] * step + results[0][i] / 2.0 * step))
    return peaks, results


def angle_save(root, degree, adf, snapshots, id1, id2, cut, nbins, ext='.angle'):
    """
    Save results to file :ref:`Output_angle`.

    Args:
        root (str): root name for saving file
        degree (ndarray[float]): degree used for adf calculation
        adf (ndarray[float]): value of adf corresponding to these degrees
        snapshots (list[:class:`.Snap`]): list of snapshots containing the water complexes
        id1 (str): identifier for atoms used as centers (e.g. 'MN', 'O\_')
        id2 (str): identifier for atoms as possible neighbors (e.g. 'O\_', 'H\_')
        cut (float): cutoff distance for radial calculation
        nbins (int): number of radius intervals; influences resolutions together with :data:`cut`
        ext (str, optional): default ".radial" - extension for the saved file: name = root + ext
    """
    # open file
    path = root + ext
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('angle_save', path)
    # write header
    f.write(utility.write_header())
    f.write("ANGLE DISTRIBUTION FUNCTION\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
    f.write("%-14s%14s\n" % ("ID1", id1))
    f.write("%-14s%14s\n" % ("ID2", id2))
    f.write("%-14s%14.8f\n" % ("CUT", cut))
    f.write("%-14s%14d\n" % ("NBINS", nbins))
    f.write("%-14s\n" % "UNIT CELL")
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    f.write("\n%14s%14s\n" % ("DEGREE", "ADF"))
    data = np.vstack((degree, adf))
    np.savetxt(f, data.T, fmt="%14.8f")
    f.close()
    return


def angle_load(root, ext='.angle'):
    """
    Load information from the :ref:`Output_angle` file previously created by :func:`.angle_save`.

    Args:
        root (str): root name for the file to be loaded
        ext (str, optional): default ".angle" - extension for the file to be loaded: name = root + ext

    Returns:
        (tuple): tuple containing:

            - ndarray(float): 2D array containing degrees and corresponding values of adf
    """
    # open file
    path = root + ext
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('angle_load', path)
    text = f.readlines()  # read text as lines
    for i in range(len(text)):
        text[i] = text[i].split()  # split each line into list with strings as elements
    for i in range(len(text)):
        if len(text[i]) > 1:
            # find beginning beginning of data
            if text[i] == ['DEGREE', 'ADF']:
                data = np.array(text[i+1:], dtype=float)
                break
    return data
