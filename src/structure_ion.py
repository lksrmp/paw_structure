import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# MODULES WITHIN PROJECT
from . import ion
from . import utility


########################################################################################################################
# COLLECT INFORMATION ABOUT ATOM NUMBER, TIME AND ITERATION FOR PLOTTING
########################################################################################################################
# INPUT
# list class Snap snapshots     contains all snapshots
#####
# OUTPUT
# list int atoms                number of atoms in ion complex for each snapshot
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
# MAIN PROGRAM FOR ION COMPLEX ANALYSIS
########################################################################################################################
# USAGE
# python3 structure_ion.py [-p] <root>.ion
# <root>.ion        DATA FILE CREATED BY structure_fast.py CONTAINING ION COMPLEX INFORMATION
# -p (optional)     FLAG FOR SHOWING THE PLOT
# TODO: make file ending variable
#####
# OUTPUT
# <root>.ion_out    ONLY LIST SNAPSHOTS BETWEEN WHICH CHANGES IN THE ION COMPLEX OCCUR
#                   IF NO CHANGES OCCUR, FILE IS NOT PRODUCED
# <root>_ion.png    GRAPH SHOWING THE NUMBER OF ATOMS IN THE ION COMPLEX AS FUNCTION OF TIME
########################################################################################################################
def main():
    print("ANALYSIS OF ION COMPLEX IN PROGRESS")
    # get command line arguments
    args = utility.structure_ion_input()
    # check for correct file ending
    root = utility.argcheck([sys.argv[0], args.ion], '.ion')
    # load snapshots from *.ion save file
    snapshots = ion.ion_load(root)
    # find indices of changing atom number
    idx_change = detect_change(snapshots)
    # get information for plotting
    atoms, times, iterations = number_atoms(snapshots)
    # select corresponding snapshots
    export = [snapshots[i] for i in idx_change]
    # write snapshots with changes to file
    if len(export) < 2:
        print('NO CHANGES IN FILE %s' % (root + '.ion'))
    else:
        ref = 'SEE ORIGINAL OUTPUT'
        ion.ion_save(root, export, ref, ref, ref, 0, 0, ext='.ion_out')
        print("WRITING OF %s SUCCESSFUL" % (root + '.ion_out'))
    # plot atom number as function of time
    matplotlib.rcParams.update({'font.size': 14})
    plt.figure()
    plt.plot(times, atoms)
    plt.plot(times, atoms, 'ro', markersize=1)
    ticks = range(np.min(atoms) - 1, np.max(atoms) + 2)
    plt.yticks(ticks)
    plt.xlabel('time [ps]')
    plt.ylabel('number of atoms')
    plt.title('ION COMPLEX')
    plt.grid()
    fig_name = root + '_ion.png'
    plt.savefig(fig_name)
    print('SAVING OF %s SUCCESSFUL' % fig_name)
    if args.plot:
        plt.show()
    print('ANALYSIS OF ION COMPLEX FINISHED')