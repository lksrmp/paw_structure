"""
paw_structure.hbonds
--------------------
Hydrogen bond detection.

Main routine is :func:`.hbonds_find_parallel`.

.. _pybind11: https://pybind11.readthedocs.io/en/stable/

Utilizes C++ code connected by pybind11_ in :mod:`.hbonds_c`.

Dependencies:
    :py:mod:`functools`
    :py:mod:`matplotlib`
    :py:mod:`miniutils`
    :py:mod:`numpy`
    :py:mod:`seaborn`
    :py:mod:`sys`
    :mod:`.utility`
    :mod:`.hbonds_c`

.. autosummary::

    hbonds_find_parallel
    hbonds_load_c
    hbonds_plot_c
    hbonds_save_c
    hbonds_single_c

XXX REFERENCE TO ALGORITHM EXPLANATION XXX
"""
from functools import partial
import matplotlib
import matplotlib.pyplot as plt
import miniutils.progress_bar as progress
import numpy as np
import seaborn as sns
import sys

from . import utility
from . import hbonds_c




def hbonds_single_c(snap, id1, id2, cut1, cut2, angle):
    """
    Binding of C++ routines in :mod:`.hbonds_c` for couting of hydrogen bonds in a single snapshot.

    Args:
        snap (:class:`.Snap`): single snapshot containing the atomic information
        id1 (str): identifier for oxygen atoms (e.g. 'O\_')
        id2 (str): identifier for hydrogen atoms (e.g. 'H\_')
        cut1 (float): maximum distance between two oxygen atoms
        cut2 (float): maximum distance between an oxygen and a hydrogen atom
        angle (float): minimum O-H-O angle in degree

    Returns:
        float: number of hydrogen bonds found for this snapshot
    """
    atoms1 = snap.atoms[snap.atoms['id'] == id1]['pos'].values
    atoms1 = atoms1.reshape(len(atoms1) * 3)
    atoms2 = snap.atoms[snap.atoms['id'] == id2]['pos'].values
    atoms2 = atoms2.reshape(len(atoms2) * 3)
    cell = snap.cell.reshape(9)
    number = hbonds_c.hbonds(atoms1, atoms2, cut1, cut2, angle, cell)
    return number


def hbonds_plot_c(args):
    """
    Plot hydrogen bond number per oxygen atom as a function of time.

    Args:
        args (:py:mod:`argparse` object): command line arguments
    """
    if args.latex:
        plt.rcParams.update(utility.tex_fonts)
        plt.figure(figsize=utility.set_size(args.latex[0], fraction=args.latex[1]))
        sns.set_theme()
        sns.color_palette(n_colors=8)
    else:
        matplotlib.rcParams.update({'font.size': 14})
        plt.figure()
    for name in args.hbonds:
        root = utility.argcheck([sys.argv[0], name], '.hbonds_c')
        data = hbonds_load_c(root)
        if args.latex:
            label = root.replace("_", "\_")
        else:
            label = root
        plt.scatter(data[:, 0], data[:, 1], s=1, label=label)
    plt.grid(b=True)
    if args.key:
        plt.legend(frameon=True)
    if args.xlim:
        plt.xlim(args.xlim)
    if args.ylim:
        plt.ylim(args.ylim)
    if args.latex:
        plt.xlabel(r'time [ps]')
        plt.ylabel(r'HB / molecule')
        fig_name = root + "_hbonds.pdf"
        plt.savefig(fig_name, format='pdf', bbox_inches='tight')
    else:
        plt.xlabel("time [ps]")
        plt.ylabel("HB / molecule")
        fig_name = root + "_hbonds.png"
        plt.savefig(fig_name, dpi=300.0)
    print('SAVING OF %s SUCCESSFUL' % fig_name)
    if args.plot:
        plt.show()
    return


def hbonds_save_c(root, time, n_hbonds, snapshots, id1, id2, cut1, cut2, angle, ext='.hbonds_c'):
    """
    Save results to file :ref:`Output_hbonds_c`.

    Args:
        root (str): root name of the files
        time (ndarray[float]): simulation times of snapshots
        n_hbonds (ndarray[float]): number of average hydrogen bonds per oxygen atom of snapshots
        snapshots (list[:class:`.Snap`]): list of snapshots containing the atomic information
        id1 (str): identifier for oxygen atoms (e.g. 'O\_')
        id2 (str): identifier for hydrogen atoms (e.g. 'H\_')
        cut1 (float): maximum distance between two oxygen atoms
        cut2 (float): maximum distance between an oxygen and a hydrogen atom
        angle (float): minimum O-H-O angle in degree
        ext (str, optional): default ".hbonds_c" - extension for the saved file: name = root + ext
    """
    path = root + ext
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('radial_save', path)
    # write header
    f.write("HYDROGEN BONDS PER MOLECULE\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
    f.write("%-14s%14s\n" % ("ID1", id1))
    f.write("%-14s%14s\n" % ("ID2", id2))
    f.write("%-14s%14s\n" % ("CUT1", cut1))
    f.write("%-14s%14s\n" % ("CUT2", cut2))
    f.write("%-14s%14s\n" % ("ANGLE", angle))
    f.write("%-14s\n" % "UNIT CELL")
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    f.write("\n%14s%14s\n" % ("TIME", "HB / MOLECULE"))
    data = np.vstack((time, n_hbonds))
    np.savetxt(f, data.T, fmt="%14.8f")
    f.close()
    return


def hbonds_load_c(root, ext='.hbonds_c'):
    """
    Load information previously saved by :func:`.hbonds_save_c`.

    Args:
        root (str): root name for the file to be loaded
        ext (str, optional): default ".hbonds_c" - extension for the file to be loaded: name = root + ext

    Returns:
        ndarray: 2D array containing time and number of hydrogen bonds per molecule
    """
    path = root + ext
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('hbonds_load_c', path)
    text = f.readlines()
    for i in range(len(text)):
        text[i] = text[i].split()
    for i in range(len(text)):
        if len(text[i]) > 1:
            if text[i] == ['TIME', 'HB', '/', 'MOLECULE']:
                data = np.array(text[i+1:], dtype=float)
                break
    return data


def hbonds_find_parallel(root, snapshots, id1, id2, cut1, cut2, angle):
    """
    Calculate the average number of hydrogen bonds per oxygen atom for all snapshots.

    Args:
        root (str): root name of files
        snapshots (list[:class:`.Snap`]): list of snapshots containing the atomic information
        id1 (str): identifier for oxygen atoms (e.g. 'O\_')
        id2 (str): identifier for hydrogen atoms (e.g. 'H\_')
        cut1 (float): maximum distance between two oxygen atoms
        cut2 (float): maximum distance between an oxygen and a hydrogen atom
        angle (float): minimum O-H-O angle in degree

    Todo:
        Implement atom selection by name.
    """
    print("HYDROGEN BOND DETECTION IN PROGRESS")
    multi = partial(hbonds_single_c, id1=id1, id2=id2, cut1=cut1, cut2=cut2, angle=angle)
    save = progress.parallel_progbar(multi, snapshots)
    save = np.array(save) / len(snapshots[0].atoms[snapshots[0].atoms['id'] == id1])
    time = np.array([snap.time for snap in snapshots])
    hbonds_save_c(root, time, save, snapshots, id1, id2, cut1, cut2, angle)
    print("HYDROGEN BOND DETECTION FINISHED")
    return


##### THE FOLLOWING FUNCTIONS ARE EITHER PART OF AN OLD AND MORE COMPLICATE CRITERION OR A DIFFERENT APPROACH OF
##### SAVING THE NAMES OF ATOMS PARTICIPATING IN A HYDROGEN BOND
##### THIS APPROACH WAS REPLACED BY JUST COUNTING THEM IN A C++ ROUTINE INSTEAD OF KEEPING THE NAME INFORMATION

# OUT OF USE; FOR OLD CRITERION
# EVALUATE FIRST FUNCTION FOR HB CRITERION
# def f_eval(dist_oo, oo_min, oo_max):
#     if dist_oo < oo_min:
#         return 1
#     elif dist_oo > oo_max:
#         return 0
#     else:
#         return 1 - (dist_oo - oo_min) / (oo_max - oo_min)


# OUT OF USE; FOR OLD CRITERION
# EVALUATE SECOND FUNCTION FOR HB CRITERION
# def g_eval(dist_oh, dist_ho, dist_oo, g_factor):
#     diff = dist_oh + dist_ho - dist_oo
#     diff[diff > g_factor] = 0.0
#     diff[diff > 0.0] = 1. - diff[diff > 0.0] / g_factor
#     return diff

# OUT OF USE; FOR OLD CRITERION
# CHECK IF o1 - h - o2 FORM A HYDROGEN BOND
# RETURN OF 1 MEANS HYDROGEN BOND, RETURN OF 0 MEANS NO HYDROGEN BOND
# SOURCE: "Correlations among Hydrogen Bonds in Liquid Water" - Raiteri et al. (2004)
# def hbonds_eval(o1, h, o2, args):
#     dist_oh = np.linalg.norm(o1['pos'].values - h['pos'].values, axis=1)
#     dist_ho = np.linalg.norm(h['pos'].values - o2['pos'].to_numpy(dtype=np.float64).reshape(1, 3), axis=1)
#     dist_oo = np.linalg.norm(o1['pos'].values - o2['pos'].to_numpy(dtype=np.float64).reshape(1, 3), axis=1)
#     val = f_eval(dist_oo, args[0], args[1]) * g_eval(dist_oh, dist_ho, dist_oo, args[2])
#     val[val <= args[3]] = 0
#     val[val > args[3]] = 1
#     val = np.array(val, dtype=bool)
#     return val


# OUT OF USE; REPLACED BY FASTER C++ ROUTINE
# def hbonds_geometry(center, hydrogen, next, args):
#     check = False
#     ba = center['pos'].values - hydrogen['pos'].values
#     bc = next['pos'].values - hydrogen['pos'].values
#     for i in range(len(hydrogen)):
#         cosine_angle = np.dot(ba[i].reshape(3), bc[i].reshape(3)) / (np.linalg.norm(ba[i]) * np.linalg.norm(bc[i]))
#         angle = np.arccos(cosine_angle)
#         if np.degrees(angle) > 140:
#             check = True
#             break
#     return check


# OUT OF USE; REPLACED BY FASTER C++ ROUTINE
# DETECT HYDROGEN BONDS IN A SINGLE SNAPSHOT
# SAVES NAMES OF HYDROGEN BOND CONNECTIONS INSTEAD OF JUST COUNTING THEM
# def hbonds_single(snap, id1, id2, cut1, cut2, args):
#     # id1-id1 neighbors
#     next1 = neighbor.neighbor_find(snap, id1, id1, cut1)
#     # id1-id2 neighbors
#     next2 = neighbor.neighbor_find(snap, id1, id2, cut2)
#     # dictionary to store connections
#     h_bonds = {key: [] for key in next1.keys()}
#     for key in next1.keys():
#         # define center atom
#         center = snap.atoms[snap.atoms['name'] == key]
#         for index, next_o in next1[key].iterrows():
#             # find common id2 atoms
#             id2_list = [*(set(next2[key]['name'].values) & set(next2[next_o['name']]['name'].values))]
#             id2_list = next2[key][next2[key]['name'].isin(id2_list)]
#
#             # check for hydrogen bond criterion
#             # check = hbonds_eval(center, id2_list, next_o, args)
#             # if check.any():
#             #     h_bonds[key].append(next_o['name'])
#             #     h_bonds[next_o['name']].append(key)
#             #     ind = next1[next_o['name']][next1[next_o['name']]['name'] == key].index.values
#             #     next1[next_o['name']] = next1[next_o['name']].drop(ind)
#
#             check = hbonds_geometry(center, id2_list, next_o, args)
#             if check:
#                 h_bonds[key].append(next_o['name'])
#                 h_bonds[next_o['name']].append(key)
#                 ind = next1[next_o['name']][next1[next_o['name']]['name'] == key].index.values
#                 next1[next_o['name']] = next1[next_o['name']].drop(ind)
#
#     return h_bonds


# OUT OF USE; REPLACED BY FASTER C++ ROUTINE
# SAVE INFORMATION FROM hbonds_find TO FILE root.hbonds FOR LATER ANALYSIS
# def hbonds_save(root, snapshots, id1, id2, cut1, cut2, args, ext='.hbonds'):
#     # open file
#     path = root + ext
#     try:
#         f = open(path, 'w')
#     except IOError:
#         utility.err_file('hbonds_save', path)
#     f.write("HYDROGEN BONDS\n")
#     f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
#     f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
#     f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
#     f.write("%-14s%14s\n" % ("ID1", id1))
#     f.write("%-14s%14s\n" % ("ID2", id2))
#     f.write("%-14s%14.8f\n" % ("CUT1", cut1))
#     f.write("%-14s%14.8f\n" % ("CUT2", cut2))
#     f.write("%-14s%14.8f\n" % ("MIN O-O", args[0]))
#     f.write("%-14s%14.8f\n" % ("MAX O-O", args[1]))
#     f.write("%-14s%14.8f\n" % ("G_FACTOR", args[2]))
#     f.write("%-14s%14.8f\n" % ("THRESHOLD", args[3]))
#     f.write("%-14s%14d\n" % (id1 + "-ATOMS", len(snapshots[0].hbonds)))
#     f.write("%-14s\n" % "UNIT CELL")
#     np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
#     form = "{:14}"
#     for i in range(len(snapshots)):
#         f.write("-" * 72 + "\n")
#         f.write("%-14s%-14.8f%-14s%-14d\n" %
#                 ("TIME", snapshots[i].time, "ITERATION", snapshots[i].iter))
#         f.write("{:14}{:14}{:14}\n".format("CENTER", "NUMBER", "BONDS"))
#         total = 0
#         for key, values in snapshots[i].hbonds.items():
#             total += len(values)
#             f.write("{:14}{:<14d}".format(key, len(values)))
#             a = form*len(values)
#             f.write(a.format(*values))
#             f.write("\n")
#         f.write("{:14}{:<14f}\n".format("AVERAGE", total / len(snapshots[0].hbonds)))
#     f.close()


# OUT OF USE; REPLACED BY FASTER C++ ROUTINE
# LOAD INFORMATION FROM <root>.ext PREVIOUSLY SAVED BY hbonds_save()
# TODO: remove line sensitivity
# def hbonds_load(root, use_tra=False, ext='.hbonds'):
#     path = root + ext
#     try:
#         f = open(path, 'r')
#     except IOError:
#         utility.err_file('hbonds_load', path)
#     text = f.readlines()  # read text as lines
#     for i in range(len(text)):
#         text[i] = text[i].split()  # split each line into list with strings as elements
#     n_atoms = int(text[12][1])
#     time = []
#     iteration = []
#     h_bonds = []
#     start = -2
#     end = -1
#     for i in range(len(text)):
#         if text[i][0] == "TIME":
#             time.append(float(text[i][1]))
#             iteration.append(int(text[i][3]))
#             start = i + 2
#             end = i + 2 + n_atoms
#             h_dict = {}
#         if i in range(start, end):
#             h_dict[text[i][0]] = text[i][2:]
#             if i == end - 1:
#                 h_bonds.append(h_dict)
#
#     # load information about snapshots
#     if use_tra:
#         snapshots = tra.tra_load(root)
#         if len(snapshots) != len(h_bonds):
#             utility.err('hbonds_load', 0, [len(h_bonds), path, len(snapshots), root + ".snap"])
#         for i in range(len(snapshots)):
#             if snapshots[i].iter != iteration[i]:
#                 utility.err('hbonds_load', 1, [path, root + ".snap"])
#             snapshots[i].hbonds = h_bonds[i]
#         # return list of snapshots with hbond dictionaries included
#         return snapshots
#     # return lists of information
#     return iteration, time, h_bonds


# OUT OF USE; REPLACED BY FASTER C++ ROUTINE
# def hbonds_find(root, snapshots, id1, id2, cut1=3.5, cut2=3.1, args=[2.75, 3.5, 0.5, 0.5]):
#     save = []
#     for snap in snapshots:
#         h_bonds = hbonds_single(snap, id1, id2, cut1, cut2, args)
#         snap.hbonds = h_bonds
#     hbonds_save(root, save, id1, id2, cut1, cut2, args)
#     return h_bonds


# OUT OF USE; REPLACED BY FASTER C++ ROUTINE
# WRAPPER FOR PARALLEL COMPUTING
# def hbonds_find_wrapper(snap, id1, id2, cut1, cut2, args):
#     h_bonds = hbonds_single(snap, id1, id2, cut1, cut2, args)
#     snap.hbonds = h_bonds
#     return snap





