"""
paw_structure.structure_hbonds
------------------------------
Plotting of hydrogen bond number per molecule as function of time.

For usage in command line see :ref:`Usage_paw_structure_hbonds`.

Dependencies:


.. autosummary::

    main
"""
import sys

from . import utility
from . import hbonds

def main():
    print("PLOTTING OF HYDROGEN BOND NUMBER")
    args = utility.structure_hbonds_input()
    root = utility.argcheck([sys.argv[0], args.hbonds], '.hbonds_c')
    data = hbonds.hbonds_load_c(root)
    hbonds.hbonds_plot_c(root, data[:, 0], data[:, 1], args)
