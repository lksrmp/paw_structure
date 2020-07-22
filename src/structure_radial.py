import sys

from . import utility
from . import radial

def main():
    print("PLOTTING OF RADIAL DISTRIBUTION FUNCTION")
    # get command line arguments
    args = utility.structure_radial_input()
    # check for correct file ending
    root = utility.argcheck([sys.argv[0], args.radial], '.radial')
    # load data
    data, rho = radial.radial_load(root)
    if args.integrate:
        radial.radial_plot(data[:, 0], data[:, 1], integration=data[:, 2])
    else:
        radial.radial_plot(data[:, 0], data[:, 1])