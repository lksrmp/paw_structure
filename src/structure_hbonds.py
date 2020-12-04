"""
paw_structure.structure_hbonds
------------------------------
Plotting of hydrogen bond number per molecule as function of time.

For usage in command line see :ref:`Usage_paw_structure_hbonds`.

Dependencies:
    :mod:`.hbonds`
    :mod:`.utility`


.. autosummary::

    main
"""
from . import utility
from . import hbonds

def main():
    print("PLOTTING OF HYDROGEN BOND NUMBER")
    args = utility.structure_hbonds_input()
    hbonds.hbonds_plot_c(args)
