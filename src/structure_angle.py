"""
paw_structure.structure_angle
-----------------------------
Plotting of angle distribution function.

For usage in command line see :ref:`Usage_paw_structure_angle`.

Dependencies:
    :py:mod:`sys`
    :mod:`.angle`
    :mod:`.utility`

.. autosummary::

    main
"""
import sys
# MODULES WITHIN PROJECT
from . import angle
from . import utility

def main():
    """
    Entry point for :mod:`.structure_angle`
    """
    print("PLOTTING OF ANGLE DISTRIBUTION FUNCTION")
    # get command line arguments
    args = utility.structure_angle_input()
    # check for correct file ending
    root = utility.argcheck([sys.argv[0], args.angle], '.angle')
    # load data
    data = angle.angle_load(root)
    angle.angle_plot(root, data[:, 0], data[:, 1], args)