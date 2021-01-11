"""
paw_structure.structure_ion
---------------------------
Analysis of ion complex output created by :mod:`.structure_fast`.

For usage in command line see :ref:`Usage_paw_structure_ion`.

Dependencies:
    :py:mod:`matplotlib`
    :py:mod:`numpy`
    :py:mod:`seaborn`
    :py:mod:`sys`
    :mod:`.ion`
    :mod:`.tra`
    :mod:`.utility`

.. autosummary::

    main
"""
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# MODULES WITHIN PROJECT
from . import ion
from . import tra
from . import utility


def main():
    """
    Entry point for :mod:`.structure_ion`.
    """
    print("ANALYSIS OF ION COMPLEX IN PROGRESS")
    # get command line arguments
    args = utility.structure_ion_input()
    # check for correct file ending
    root = utility.argcheck([sys.argv[0], args.ion], '.ion')
    # load snapshots from *.ion save file
    snapshots = ion.ion_load(root)
    # find indices of changing atom number
    idx_change = tra.tra_detect_change(snapshots)
    # get information for plotting
    atoms, times, iterations = tra.tra_number_atoms(snapshots)
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

    if args.latex:
        plt.rcParams.update(utility.tex_fonts)
        plt.figure(figsize=utility.set_size(args.latex[0], fraction=args.latex[1]))
        sns.set_theme()
        sns.set_style("whitegridS")
        sns.color_palette(n_colors=8)
    else:
        matplotlib.rcParams.update({'font.size': 14})
        plt.figure()
    plt.plot(times, atoms, color='black')
    plt.plot(times, atoms, 'ro', markersize=1)
    ticks = range(np.min(atoms) - 1, np.max(atoms) + 2)
    plt.yticks(ticks)
    plt.grid(b=True)
    if args.xlim:
        plt.xlim(args.xlim)
    if args.ylim:
        plt.ylim(args.ylim)
    if args.latex:
        plt.xlabel(r'time [ps]')
        plt.ylabel(r'number of atoms')
        fig_name = root + "_ion.pdf"
        plt.savefig(fig_name, format='pdf', bbox_inches='tight')
    else:
        plt.xlabel('time [ps]')
        plt.ylabel('number of atoms')
        fig_name = root + '_ion.png'
        plt.savefig(fig_name, dpi=300.0)
    print('SAVING OF %s SUCCESSFUL' % fig_name)
    if args.plot:
        plt.show()
    print('ANALYSIS OF ION COMPLEX FINISHED')