"""
paw_structure.structure_radial
------------------------------
Plotting of radial distribution function.

**Usage in command line:**

    ::

        paw_structure_radial [-i; --integrate] filename

    :data:`filename` is the name of the radial distribution function file :ref:`Output_radial`.

    :data:`-i` is a flag to include the coordination number obtained from integration

Dependencies:
    :py:mod:`sys`
    :mod:`.radial`
    :mod:`.utility`

.. autosummary::

    main
"""
import sys
# MODULES WITHIN PROJECT
from . import radial
from . import utility


########################################################################################################################
# MAIN PROGRAM FOR RADIAL DISTRIBUTION ANALYSIS
########################################################################################################################
# USAGE
# python3 structure_radial.py [-p] <root>.ion
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
    """
    Entry point for :mod:`structure_radial`
    """
    print("PLOTTING OF RADIAL DISTRIBUTION FUNCTION")
    # get command line arguments
    args = utility.structure_radial_input()
    # check for correct file ending
    root = utility.argcheck([sys.argv[0], args.radial], '.radial')
    # load data
    data, rho = radial.radial_load(root)
    if args.integrate:
        radial.radial_plot(root, data[:, 0], data[:, 1], integration=data[:, 2], show=args.plot)
    else:
        radial.radial_plot(root, data[:, 0], data[:, 1], show=args.plot)