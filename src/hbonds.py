import numpy as np
from functools import partial
import miniutils.progress_bar as progress

import matplotlib
import matplotlib.pyplot as plt

from . import neighbor
from . import utility
from . import tra
from . import hbonds_c


# EVALUATE FIRST FUNCTION FOR HB CRITERION
def f_eval(dist_oo, oo_min, oo_max):
    if dist_oo < oo_min:
        return 1
    elif dist_oo > oo_max:
        return 0
    else:
        return 1 - (dist_oo - oo_min) / (oo_max - oo_min)


# EVALUATE SECOND FUNCTION FOR HB CRITERION
def g_eval(dist_oh, dist_ho, dist_oo, g_factor):
    diff = dist_oh + dist_ho - dist_oo
    diff[diff > g_factor] = 0.0
    diff[diff > 0.0] = 1. - diff[diff > 0.0] / g_factor
    return diff


# CHECK IF o1 - h - o2 FORM A HYDROGEN BOND
# RETURN OF 1 MEANS HYDROGEN BOND, RETURN OF 0 MEANS NO HYDROGEN BOND
# SOURCE: "Correlations among Hydrogen Bonds in Liquid Water" - Raiteri et al. (2004)
def hbonds_eval(o1, h, o2, args):
    dist_oh = np.linalg.norm(o1['pos'].values - h['pos'].values, axis=1)
    dist_ho = np.linalg.norm(h['pos'].values - o2['pos'].to_numpy(dtype=np.float64).reshape(1, 3), axis=1)
    dist_oo = np.linalg.norm(o1['pos'].values - o2['pos'].to_numpy(dtype=np.float64).reshape(1, 3), axis=1)
    val = f_eval(dist_oo, args[0], args[1]) * g_eval(dist_oh, dist_ho, dist_oo, args[2])
    val[val <= args[3]] = 0
    val[val > args[3]] = 1
    val = np.array(val, dtype=bool)
    return val


def hbonds_geometry(center, hydrogen, next, args):
    check = False
    ba = center['pos'].values - hydrogen['pos'].values
    bc = next['pos'].values - hydrogen['pos'].values
    for i in range(len(hydrogen)):
        cosine_angle = np.dot(ba[i].reshape(3), bc[i].reshape(3)) / (np.linalg.norm(ba[i]) * np.linalg.norm(bc[i]))
        angle = np.arccos(cosine_angle)
        if np.degrees(angle) > 140:
            check = True
            break
    return check


# DETECT HYDROGEN BONDS IN A SINGLE SNAPSHOT
def hbonds_single(snap, id1, id2, cut1, cut2, args):
    # id1-id1 neighbors
    next1 = neighbor.neighbor_find(snap, id1, id1, cut1)
    # id1-id2 neighbors
    next2 = neighbor.neighbor_find(snap, id1, id2, cut2)
    # dictionary to store connections
    h_bonds = {key: [] for key in next1.keys()}
    for key in next1.keys():
        # define center atom
        center = snap.atoms[snap.atoms['name'] == key]
        for index, next_o in next1[key].iterrows():
            # find common id2 atoms
            id2_list = [*(set(next2[key]['name'].values) & set(next2[next_o['name']]['name'].values))]
            id2_list = next2[key][next2[key]['name'].isin(id2_list)]

            # check for hydrogen bond criterion
            # check = hbonds_eval(center, id2_list, next_o, args)
            # if check.any():
            #     h_bonds[key].append(next_o['name'])
            #     h_bonds[next_o['name']].append(key)
            #     ind = next1[next_o['name']][next1[next_o['name']]['name'] == key].index.values
            #     next1[next_o['name']] = next1[next_o['name']].drop(ind)

            check = hbonds_geometry(center, id2_list, next_o, args)
            if check:
                h_bonds[key].append(next_o['name'])
                h_bonds[next_o['name']].append(key)
                ind = next1[next_o['name']][next1[next_o['name']]['name'] == key].index.values
                next1[next_o['name']] = next1[next_o['name']].drop(ind)

    return h_bonds


# SAVE INFORMATION FROM hbonds_find TO FILE root.hbonds FOR LATER ANALYSIS
def hbonds_save(root, snapshots, id1, id2, cut1, cut2, args, ext='.hbonds'):
    # open file
    path = root + ext
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('hbonds_save', path)
    f.write("HYDROGEN BONDS\n")
    f.write("%-14s%14.8f\n" % ("T1", snapshots[0].time))
    f.write("%-14s%14.8f\n" % ("T2", snapshots[-1].time))
    f.write("%-14s%14d\n" % ("SNAPSHOTS", len(snapshots)))
    f.write("%-14s%14s\n" % ("ID1", id1))
    f.write("%-14s%14s\n" % ("ID2", id2))
    f.write("%-14s%14.8f\n" % ("CUT1", cut1))
    f.write("%-14s%14.8f\n" % ("CUT2", cut2))
    f.write("%-14s%14.8f\n" % ("MIN O-O", args[0]))
    f.write("%-14s%14.8f\n" % ("MAX O-O", args[1]))
    f.write("%-14s%14.8f\n" % ("G_FACTOR", args[2]))
    f.write("%-14s%14.8f\n" % ("THRESHOLD", args[3]))
    f.write("%-14s%14d\n" % (id1 + "-ATOMS", len(snapshots[0].hbonds)))
    f.write("%-14s\n" % "UNIT CELL")
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    form = "{:14}"
    for i in range(len(snapshots)):
        f.write("-" * 72 + "\n")
        f.write("%-14s%-14.8f%-14s%-14d\n" %
                ("TIME", snapshots[i].time, "ITERATION", snapshots[i].iter))
        f.write("{:14}{:14}{:14}\n".format("CENTER", "NUMBER", "BONDS"))
        total = 0
        for key, values in snapshots[i].hbonds.items():
            total += len(values)
            f.write("{:14}{:<14d}".format(key, len(values)))
            a = form*len(values)
            f.write(a.format(*values))
            f.write("\n")
        f.write("{:14}{:<14f}\n".format("AVERAGE", total / len(snapshots[0].hbonds)))
    f.close()


# LOAD INFORMATION FROM <root>.ext PREVIOUSLY SAVED BY hbonds_save()
# TODO: remove line sensitivity
def hbonds_load(root, use_tra=False, ext='.hbonds'):
    path = root + ext
    try:
        f = open(path, 'r')
    except IOError:
        utility.err_file('hbonds_load', path)
    text = f.readlines()  # read text as lines
    for i in range(len(text)):
        text[i] = text[i].split()  # split each line into list with strings as elements
    n_atoms = int(text[12][1])
    time = []
    iteration = []
    h_bonds = []
    start = -2
    end = -1
    for i in range(len(text)):
        if text[i][0] == "TIME":
            time.append(float(text[i][1]))
            iteration.append(int(text[i][3]))
            start = i + 2
            end = i + 2 + n_atoms
            h_dict = {}
        if i in range(start, end):
            h_dict[text[i][0]] = text[i][2:]
            if i == end - 1:
                h_bonds.append(h_dict)

    # load information about snapshots
    if use_tra:
        snapshots = tra.tra_load(root)
        if len(snapshots) != len(h_bonds):
            utility.err('hbonds_load', 0, [len(h_bonds), path, len(snapshots), root + ".snap"])
        for i in range(len(snapshots)):
            if snapshots[i].iter != iteration[i]:
                utility.err('hbonds_load', 1, [path, root + ".snap"])
            snapshots[i].hbonds = h_bonds[i]
        # return list of snapshots with hbond dictionaries included
        return snapshots
    # return lists of information
    return iteration, time, h_bonds
            

# def hbonds_find(root, snapshots, id1, id2, cut1=3.5, cut2=3.1, args=[2.75, 3.5, 0.5, 0.5]):
#     save = []
#     for snap in snapshots:
#         h_bonds = hbonds_single(snap, id1, id2, cut1, cut2, args)
#         snap.hbonds = h_bonds
#     hbonds_save(root, save, id1, id2, cut1, cut2, args)
#     return h_bonds


# WRAPPER FOR PARALLEL COMPUTING
def hbonds_find_wrapper(snap, id1, id2, cut1, cut2, args):
    h_bonds = hbonds_single(snap, id1, id2, cut1, cut2, args)
    snap.hbonds = h_bonds
    return snap





# C++
def hbonds_number_wrapper(snap, id1, id2, cut1, cut2, angle):
    atoms1 = snap.atoms[snap.atoms['id'] == id1]['pos'].values
    atoms1 = atoms1.reshape(len(atoms1) * 3)
    atoms2 = snap.atoms[snap.atoms['id'] == id2]['pos'].values
    atoms2 = atoms2.reshape(len(atoms2) * 3)
    number = hbonds_c.hbonds(atoms1, atoms2, cut1, cut2, angle, snap.cell[0][0])
    return number


def hbonds_c_plot(time, n_hbonds):
    matplotlib.rcParams.update({'font.size': 14})
    plt.figure()
    plt.scatter(time, n_hbonds, s=1)
    plt.grid()
    plt.xlabel("time [ps]")
    plt.ylabel("HB / molecule")
    plt.show()
    return


def hbonds_c_save(root, time, n_hbonds, snapshots, id1, id2, ext='.hbonds_c'):
    # open file
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
    f.write("%-14s\n" % "UNIT CELL")
    np.savetxt(f, snapshots[0].cell, fmt="%14.8f")
    f.write("\n%14s%14s\n" % ("TIME", "HB / MOLECULE"))
    data = np.vstack((time, n_hbonds))
    np.savetxt(f, data.T, fmt="%14.8f")
    f.close()
    return





# MAIN ROUTINE
def hbonds_find_parallel(root, snapshots, id1, id2, cut1=3.5, cut2=3.1, args=[2.75, 3.5, 0.5, 0.5]):
    print("HYDROGEN BOND DETECTION IN PROGRESS")


    # initialize other parameters (necessary for parallelization
    # multi_one = partial(hbonds_find_wrapper, id1=id1, id2=id2, cut1=cut1, cut2=cut2, args=args)

    # hydrogen bonds number search C++
    multi_two = partial(hbonds_number_wrapper, id1=id1, id2=id2, cut1=cut1, cut2=cut2, angle=140.0)
    save_two = progress.parallel_progbar(multi_two, snapshots)
    save_two = np.array(save_two) / len(snapshots[0].atoms[snapshots[0].atoms['id'] == id1])
    time = np.array([snap.time for snap in snapshots])
    hbonds_c_save(root, time, save_two, snapshots, id1, id2)
    hbonds_c_plot(time, save_two)
    
    
    # run hbonds search
    # save = progress.parallel_progbar(multi_one, snapshots)

    # save results to file
    # hbonds_save(root, save, id1, id2, cut1, cut2, args)
    print("HYDROGEN BOND DETECTION FINISHED")

    return save_two
