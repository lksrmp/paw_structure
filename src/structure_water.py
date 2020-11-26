"""
paw_structure.structure_water
-----------------------------
Analysis of water complexes output created by :mod:`.structure_fast`.

For usage in command line see :ref:`Usage_paw_structure_water`.

Dependencies:
    :py:mod:`matplotlib`
    :py:mod:`numpy`
    :py:mod:`pandas`
    :py:mod:`sys`
    :mod:`.ion`
    :mod:`.tra`
    :mod:`.utility`
    :mod:`.water`

.. autosummary::

    main
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
# MODULES WITHIN PROJECT
from . import ion
from . import tra
from . import utility
from . import water


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
    """
    Entry point for :mod:`.structure_water`.
    """
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
    idx_change = tra.tra_detect_change(snapshots)
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
    atoms, times, iterations = tra.tra_number_atoms(snapshots)
    # plotting
    matplotlib.rcParams.update({'font.size': 12})
    plt.figure()
    plt.plot(times, atoms, color='black')
    plt.plot(times, atoms, 'ro', markersize=1, label='all complexes')
    ticks = [np.min(atoms), np.max(atoms)]
    if ion_root is not None:
        atoms_ion, times_ion, iterations_ion = tra.tra_number_atoms(snapshots_ion)
        atoms_water = np.array(atoms, dtype=int) - np.array(atoms_ion, dtype=int)
        plt.plot(times, atoms_water, color='black')
        plt.plot(times, atoms_water, 'go', markersize=1, label='water complexes')
        ticks = [np.min([np.min(atoms_water), ticks[0]]), np.max([np.max(atoms_water), ticks[1]])]
        plt.legend()
    ticks = range(ticks[0], ticks[1], 2)
    plt.yticks(ticks)
    plt.xlabel('time [ps]')
    plt.ylabel('number of atoms')
    # plt.title('WATER COMPLEX')
    if args.xlim:
        plt.xlim(args.xlim)
    if args.ylim:
        plt.ylim(args.ylim)
    plt.grid()
    fig_name = root + '_water.png'
    # save plot
    plt.savefig(fig_name, dpi=300.0)
    print('SAVING OF %s SUCCESSFUL' % fig_name)
    if args.plot:
        plt.show()
    print('ANALYSIS OF WATER COMPLEX FINISHED')