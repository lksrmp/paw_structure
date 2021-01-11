"""
paw_structure.structure_gap
------------------------------
Plotting of energy gap and HOMO/LUMO energy as function of time.

For usage in command line see :ref:`Usage_paw_structure_gap`.

Dependencies:
    :py:mod:`matplotlib`
    :py:mod:`seaborn`
    :py:mod:`sys`
    :mod:`.utility`


.. autosummary::

    main
"""
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import sys

from . import utility

def main():
    """
    Entry point for :mod:`.structure_gap`.

    Todo:
        Clean up code!
    """
    print("PLOTTING OF ENERGY GAP AND HOMO/LUMO ENERGY")
    args = utility.structure_gap_input()

    root = utility.argcheck([sys.argv[0], args.prot], '.prot')

    try:
        f = open(args.prot, 'r')
    except IOError:
        utility.err_file('structure_gap', args.prot)
    # initialize data storage
    time = 0.0
    gap = []
    homo = []
    lumo = []
    iteration = []
    line = f.readline()
    line_strip = line.split()
    if len(line_strip) > 0:
        # if line_strip[0] == "DETAILED":
        #     increment = int(line_strip[4])
        if line_strip[0] == "!>": # no split if iteration >=100000
            time = float(line_strip[2])
        if line_strip[0] == "ABSOLUTE":
            gap.append(float(line_strip[2]))
        if "HOMO-ENERGY" in line_strip[0]:
            homo.append(float(line_strip[1]))
        if "LUMO-ENERGY" in line_strip[0]:
            lumo.append(float(line_strip[1]))
    while line:
        line = f.readline()
        if len(line) > 2:
            if line[0:2] == "!>":
                line_strip = line[2:].split()
                time = float(line_strip[1])
            if line.split()[0] == "ABSOLUTE":
                gap.append(float(line.split()[2]))
                iteration.append(time)
            if "HOMO-ENERGY" in line.split()[0]:
                homo.append(float(line.split()[1]))
            if "LUMO-ENERGY" in line.split()[0]:
                lumo.append(float(line.split()[1]))
    f.close()

    # remove first entry as this is often very large and wrong
    iteration = iteration[1:]
    gap = gap[1:]
    homo = homo[1:]
    lumo = lumo[1:]

    if args.latex:
        plt.rcParams.update(utility.tex_fonts)
        plt.figure(figsize=utility.set_size(args.latex[0], fraction=args.latex[1]))
        sns.set_theme()
        sns.set_style("whitegrid")
    else:
        matplotlib.rcParams.update({'font.size': 14})
        fig, ax1 = plt.subplots()
    color1 = 'tab:red'
    ax1.scatter(iteration, gap, s=1, color=color1, label="gap")
    ax1.tick_params(axis='y', labelcolor=color1)
    if args.xlim:
        ax1.set_xlim(args.xlim)
    if args.ylim1:
        ax1.set_ylim(args.ylim1)
    ax1.grid(b=True, axis='x')
    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.scatter(iteration, homo, s=1, label="HOMO", color=color2)
    ax2.scatter(iteration, lumo, s=1, label="LUMO", color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)
    if args.ylim2:
        ax2.set_ylim(args.ylim2)
    if args.latex:
        ax1.set_xlabel(r'time [ps]')
        ax1.set_ylabel(r"energy gap [eV]", color=color1)
        ax2.set_ylabel(r"HOMO/LUMO energy [eV]", color=color2)
        fig_name = root + "_gap.png"
        plt.savefig(fig_name, format='pdf', bbox_inches='tight')
    else:
        ax1.set_xlabel("time [ps]")
        ax1.set_ylabel("energy gap [eV]", color=color1)
        ax2.set_ylabel("HOMO/LUMO energy [eV]", color=color2)
        plt.tight_layout()
        fig_name = root + "_gap.png"
        plt.savefig(fig_name, dpi=300.0)
    if args.plot:
        plt.show()