"""
paw_structure.structure_hbonds
------------------------------
Plotting of hydrogen bond number per molecule as function of time.

**Usage in command line:**

    ::

        paw_structure_hbonds filename

    :data:`filename` is the name of the hydrogen bond file :ref:`Output_hbonds_c`.

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
    data = hbonds.hbonds_c_load(root)
    hbonds.hbonds_c_plot(root, data[:, 0], data[:, 1], show=args.plot)
