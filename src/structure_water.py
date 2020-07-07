import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# MODULES WITHIN PROJECT
from . import water
from . import ion
from . import utility


########################################################################################################################
# COLLECT INFORMATION ABOUT ATOM NUMBER, TIME AND ITERATION FOR PLOTTING
########################################################################################################################
# INPUT
# list class Snap snapshots     contains all snapshots
#####
# OUTPUT
# list int atoms                number of atoms in water complexes for each snapshot
# list float times              simulation times for each snapshot
# list int iterations           simulation iteration for each snapshot
########################################################################################################################
def number_atoms(snapshots):
    atoms = []
    times = []
    iterations = []
    # loop through snapshots and save information to list
    for i in range(len(snapshots)):
        atoms.append(len(snapshots[i].atoms))
        times.append(snapshots[i].time)
        iterations.append(snapshots[i].iter)
    return atoms, times, iterations



########################################################################################################################
# DETECT CHANGES IN ATOM CONFIGURATION AND SAVE INDEX OF SNAPSHOTS BETWEEN WHICH THE CHANGE OCCURS
# CHANGE FROM SNAPSHOT NUMBER 12 TO 13 -> STORE 12 and 13
########################################################################################################################
# INPUT
# list class Snap snapshots     contains all snapshots
#####
# OUTPUT
# ndarray float                 indices of snapshots where changes occur
########################################################################################################################
def detect_change(snapshots):
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



########################################################################################################################
# MAIN PROGRAM FOR WATER COMPLEX ANALYSIS
########################################################################################################################
# USAGE
# python3 structure_water.py [-i ION] [-p] <root>.water
# >root>.water          DATA FILE CREATED BY structure_fast.py CONTAINING WATER COMPLEX INFORMATION
# -i ION (optional)     DATA FILE CREATED BY structure_fast.py CONTAINING ION COMPLEX INFORMATION
# -p (optional)         FLAG FOR SHOWING THE PLOT
# TODO: make file ending variable
#####
# OUTPUT (depends on selected options)
# <root>.water_out  ONLY LIST SNAPSHOTS BETWEEN WHICH CHANGES IN THE ION COMPLEX OCCUR
#                   IF NO CHANGES OCCUR, FILE IS NOT PRODUCED
# <root>_water.png  GRAPH SHOWING THE NUMBER OF ATOMS IN THE WATER COMPLEXES AS FUNCTION OF TIME
# <root>.water_ion  ADDS ATOMS FROM ION COMPLEX AND WATER COMPLEX TOGETHER
########################################################################################################################
def main():
    print("ANALYSIS OF WATER COMPLEX IN PROGRESS")
    args = utility.structure_water_input()
    root = utility.argcheck([sys.argv[0], args.water], '.water')
    if not args.ion:
        ion_root = None
    else:
        ion_root = utility.argcheck([sys.argv[0], args.ion[0]], '.ion')
    # load snapshots from *.water save file
    snapshots = water.water_load(root)
    # detect changes in atom number
    idx_change = detect_change(snapshots)
    # select corresponding snapshots
    export = [snapshots[i] for i in idx_change]
    if len(export) < 2:
        print('NO CHANGES IN FILE %s' % (root + '.water'))
    else:
        ref = 'SEE ORIGINAL OUTPUT'
        water.water_save(root, export, ref, ref, 0, ext='.water_out')
        print("WRITING OF %s SUCCESSFUL" % (root + '.water_out'))

    # if ion complex is present, add those atoms to the snapshots
    if ion_root is not None:
        # load from *.ion save file
        snapshots_ion = ion.ion_load(ion_root)
        # compatibility check
        if len(snapshots) != len(snapshots_ion):
            utility.err('structure_water', 0, [len(snapshots), 'water file', len(snapshots_ion), 'ion file'])
        for i in range(len(snapshots)):
            if snapshots[i].iter != snapshots_ion[i].iter:
                utility.err('structure_water', 1, [root + '.water', ion_root + '.ion'])
            snapshots[i].atoms = pd.concat((snapshots[i].atoms, snapshots_ion[i].atoms))
            snapshots[i].atoms = snapshots[i].atoms.drop_duplicates()  # drop double atoms
        ref = 'SEE ORIGINAL OUTPUT'
        ion.ion_save(root, snapshots, ref, ref, ref, 0, 0, ext='.water_ion')  # save ion + water complex to file
        print("WRITING OF %s SUCCESSFUL" % (root + '.water_ion'))
    # get data for plotting
    atoms, times, iterations = number_atoms(snapshots)
    # plotting
    matplotlib.rcParams.update({'font.size': 12})
    plt.figure()
    plt.plot(times, atoms, label='complex')
    plt.plot(times, atoms, 'ro', markersize=1)
    ticks = [np.min(atoms), np.max(atoms)]
    if ion_root is not None:
        atoms_ion, times_ion, iterations_ion = number_atoms(snapshots_ion)
        atoms_water = np.array(atoms, dtype=int) - np.array(atoms_ion, dtype=int)
        plt.plot(times, atoms_water, label='complex without ion')
        plt.plot(times, atoms_water, 'go', markersize=1)
        ticks = [np.min([np.min(atoms_water), ticks[0]]), np.max([np.max(atoms_water), ticks[1]])]
    ticks = range(ticks[0], ticks[1], 2)
    plt.yticks(ticks)
    plt.xlabel('time [ps]')
    plt.ylabel('number of atoms')
    plt.title('WATER COMPLEX')
    plt.grid()
    plt.legend()
    fig_name = root + '_water.png'
    # save plot
    plt.savefig(fig_name)
    print('SAVING OF %s SUCCESSFUL' % fig_name)
    if args.plot:
        plt.show()
    print('ANALYSIS OF WATER COMPLEX FINISHED')