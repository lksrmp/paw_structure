"""
paw_structure.utility
---------------------
Error and input handling.

Dependencies:
    :py:mod:`argparse`
    :py:mod:`datetime`
    :py:mod:`sys`
    :py:mod:`time`

.. autosummary::

    argcheck
    err
    err_file
    set_size
    structure_fast_input
    structure_gap_input
    structure_hbonds_input
    structure_ion_input
    structure_radial_input
    structure_water_input
    timing
    write_header
"""
import sys
import argparse
import time
from datetime import datetime, timezone

from . import _info


tex_fonts = {
    # Use LaTeX to write all text
    "text.usetex": True,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": 12,
    "font.size": 12,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
}


def timing(f):
    """
    Time of execution for a function.

    Use as decorator::

        @timing
        def function():
            #code
    """
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print("%s function took %f s" % (f.__name__, (time2 - time1)))
        return ret
    return wrap


########################################################################################################################
# RAISE ERROR FOR OPENING FILE
########################################################################################################################
# INPUT
# str func              function name in which error has occurred
# str path              path of file that could not be opened
########################################################################################################################
def err_file(func, path):
    """
    Terminate program if error during file opening.

    Args:
        func (str): name of function in which error occured
        path (str): path of file where opening failed

    Returns:
        :py:func:`sys.exit()` displaying an error message::

            PROGRAM TERMINATED
            ERROR IN FUNCTION: <func>

            COULD NOT OPEN FILE
            <path>

    """
    sys.exit("PROGRAM TERMINATED\nERROR IN FUNCTION: %s\n\nCOULD NOT OPEN FILE\n%s" % (func, path))


########################################################################################################################
# RAISE SPECIFIC ERRORS
########################################################################################################################
# INPUT
# str func              function name in which error has occurred (has to be key in dictionary)
# int id                identifier of error for a specific function
# list arg              arguments needed for the error message (variates for different funtions and errors)
# str info (optional)   additional message
########################################################################################################################
def err(func, id, arg, info=''):
    """
    Raise specific errors for internal checks.

    With :py:data:`func` and :py:data:`id` a dictionary of error functions is accessed.

    Args:
        func (str): name of function in which error occured
        id (int): number of dictionary entry for function :py:data:`func`
        arg (list): list of arguments specific for each error (can vary in length and type)
        info (str, optional): text displayed in error message

    Returns:
        :py:func:`sys.exit()` displaying an error message
    """
    # define functions returning the right error message
    def _err_tra_index_1(args):
        return ("INVALID NUMBER OF SNAPSHOTS\n%-24s%d\n%-24s%d"
                % ("SELECTED NUMBER N:", args[0], "TOTAL STEPS:", args[1]))

    def _err_tra_index_2(args):
        return ("T2 NEEDS TO BE LARGER THAN T1\n%-24s%.8f\n%-24s%.8f\n"
                % ("SELECTED TIME T1:", args[0], "SELECTED TIME T2:", args[1]))

    def _err_tra_index_3(args):
        return ("INVALID INTERVAL SELECTION\n%-24s%.8f\n%-24s%.8f\n%-24s%.8f\n%-24s%.8f"
                % ("SELECTED TIME T1:", args[0], "SELECTED TIME T2:",
                    args[1], "FIRST TIME STEP:", args[2], "LAST TIME STEP:", args[3]))

    def _err_tra_index_4(args):
        return ("INVALID NUMBER OF SNAPSHOTS FOR INTERVAL\n%-24s%d\n%-24s%d"
                % ("SELECTED NUMBER N:", args[0], "STEPS IN INTERVAL:", args[1]))

    def _err_pbc_apply3x3(args):
        return "INVALID ARGUMENTS\nEITHER SELECTION BY ID OR NAME, NOT BOTH"

    def _err_ion_single1(args):
        return "%s\n%-24s%d" % ("ONLY ONE ION ALLOWED", "IONS SELECTED:", args[0])

    def _err_ion_single2(args):
        return ("%s\n%-24s%-6s%-6s%-6s"
                % ("THREE DIFFERENT SPECIES NEEDED", "SELECTED SPECIES:", args[0], args[1], args[2]))

    def _err_water_single(args):
        return "%s\n%-24s%-6s%-6s" % ("TWO DIFFERENT SPECIES NEEDED", "SELECTED SPECIES:", args[0], args[1])

    def _err_hbonds_load1(args):
        return ("%s\n%-6d%s\n%-6d%s"
                % ("NUMBER OF SNAPSHOTS DOES NOT MATCH IN FILES:", args[0], args[1], args[2], args[3]))

    def _err_hbonds_load2(args):
        return "%s\n%s\n%s\n%s" % ("DATA OF FILES DOES NOT MATCH", "ITERATION VALUES NOT COMPATIBLE", args[0], args[1])

    def _err_scntl_text1(args):
        return "MORE BRACKETS CLOSED THAN OPENED"

    def _err_scntl_text2(args):
        return "%s\n%d %s" % ("MORE BRACKETS OPENED THAN CLOSED", args[0], "STILL OPEN")

    def _err_scntl_read1(args):
        return "MISSING PARAMETER IN %s\nPLEASE PROVIDE PARAMETER" % args[0]

    def _err_scntl_read2(args):
        return "PLEASE PROVIDE BLOCK !TRA IN %s.scntl" % args[0]

    def _err_argcheck1(args):
        return "WRONG NUMBER OF ARGUMENTS GIVEN\n%-12s%d\n%-12s%d" % ("EXPECTED:", 1, "GIVEN:", args[0])

    def _err_argcheck2(args):
        return "WRONG FILE ENDING\nPLEASE USE %s" % args[0]

    # store functions in dictionary (function name = key, id = position in list)
    error = {
        'tra_index': [_err_tra_index_1, _err_tra_index_2, _err_tra_index_3, _err_tra_index_4],
        'pbc_apply3x3': [_err_pbc_apply3x3],
        'ion_single': [_err_ion_single1, _err_ion_single2],
        'water_single': [_err_water_single],
        'hbonds_load': [_err_hbonds_load1, _err_hbonds_load2],
        'scntl_text': [_err_scntl_text1, _err_scntl_text2],
        'scntl_read': [_err_scntl_read1, _err_scntl_read2],
        'argcheck': [_err_argcheck1, _err_argcheck2],
        'structure_water': [_err_hbonds_load1, _err_hbonds_load2]
    }
    try:
        sys.exit("\nPROGRAM TERMINATED\nERROR IN FUNCTION: %s\n\n%s\n%s" % (func, error[func][id](arg), info))
    except KeyError and IndexError:  # catch wrong parameters while raising errors
        sys.exit("WRONG INTERNAL ERROR HANDLING\nNO ERROR MESSAGE FOR FUNCTION %s WITH ID %d AND ARGUMENTS %s"
                 % (func, id, str(arg)))


########################################################################################################################
# WRITE STRUCTURE DATA TO FILE WITHOUT HEADER
# WARNING: NO USED BECAUSE INFORMATION FOR UNIT CELL IS IMPORTANT FOR VIEWING IN AVOGADRO
########################################################################################################################
# INPUT
# str root                      root name for save file
# list class Snap snapshots     information to be saved
# str ext                       extension for file: name = root + ext
########################################################################################################################
# def snaptofile(root, snapshots, ext):
#     # open file
#     path = root + ext
#     try:
#         f = open(path, 'w')
#     except IOError:
#         sys.exit("COULD NOT OPEN FILE: %s" % path)
#     for i in range(len(snapshots)):
#         f.write("-" * 84 + "\n")
#         f.write("%-14s%-14.8f%-14s%-14d%-14s%-14d\n" %
#                 ("TIME", snapshots[i].time, "ITERATION", snapshots[i].iter, "ATOMS", len(snapshots[i].atoms)))
#         f.write("%-14s%-14s%-14s%14s%14s%14s\n" % ('NAME', 'ID', 'INDEX', 'X', 'Y', 'Z'))
#         np.savetxt(f, snapshots[i].atoms, fmt="%-14s%-14s%-14d%14.8f%14.8f%14.8f")
#     f.close()
#     return


########################################################################################################################
# CHECKS CONSOLE INPUT AND ARGUMENTS GIVEN BY USER
# WARNING: CAN ONLY HANDLE argv WITH TWO ARGUMENTS, CHECKING THE SECOND ONE FOR CORRECT EXTENSION
#          IF MORE ARGUMENTS NEEDED, DO MULTIPLE CHECKS AND HAND OVER CORRECT ARGUMENT
# TODO: allow for varying number and order of arguments
########################################################################################################################
# INPUT
# list str argv     two element list with arguments being extracted with sys.argv
# str extension     expected extension of second argument (e.g. '.ion', '.water', '.hbonds'
#####
# OUTPUT
# str               root name with extension removed
########################################################################################################################
def argcheck(argv, extension):
    """
    Checks console input and arguments.

    Args:
        argv (list[str]):  two element list with arguments being extracted with :py:func:`sys.argv`
        extension (str):  expected extension of second argument (e.g. '.ion', '.water', '.hbonds')

    Returns:
        str: name with extension removed

    Calls :func:`.utility.err` in case of wrong input.
    """
    if len(argv) != 2:
        err('argcheck', 0, [len(argv) - 1], info="PLEASE GIVE PATH OF *%s FILE" % extension)
    if not extension in argv[1]:
        err('argcheck', 1, ['*' + extension])
    return argv[1][:-len(extension)]


def write_header():
    """
    Build header for output files containing information about the paw_structure package like author, version control, installation/running time.

    Returns:
        str: text for the header
    """
    now = datetime.now(timezone.utc)
    now = now.astimezone().strftime("%Y-%m-%d %H:%M:%S%z")
    header = '{}\n{}\n'.format(84*'#', _info.__name__.center(84))
    text = 'developed by {} under Apache license, version 2.0'.format(_info.__author__).center(84)
    text = text + '\nbranch: {}; remotes: {};\n' \
                  'revision: {}; commit: {}\n' \
                  'by {} <{}> on {}\n' \
                  'installed on: {}\n'.format(_info.__branch__, _info.__url__,
                                              _info.__commit_rev__, _info.__commit_hex__,
                                              _info.__commit_author__, _info.__commit_email__, _info.__commit_time__,
                                              _info.__install_time__)
    header = header + text
    text = 'latest release: {} with commit {}\n' \
           'program started: {}\n'.format(_info.__version__, _info.__version_commit__, now)
    header = header + text + 84*'#' +'\n'
    return header

def structure_fast_input():
    """
    Get console input for :mod:`.structure_fast`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_fast`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("scntl", type=str, help="give path of control file '.scntl'")
    args = parser.parse_args()
    return args


def structure_hbonds_input():
    """
    Get console input for :mod:`.structure_hbonds`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_hbonds`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("hbonds", nargs='*', type=str, help="give path of hydrogen bond network file\nproduced by structure_fast.py")
    parser.add_argument("-avg", "--average", type=int, metavar=('average'), help="select length of running average in data points")
    parser.add_argument("-p", "--plot", action="store_true", help="show graph of hydrogen bond number")
    parser.add_argument("-l", "--latex", nargs=2, metavar=('width', 'fraction'), type=str, help="document width in pts and fraction of this width\ndefaults for thesis and beamer")
    parser.add_argument("-x", "--xlim", nargs=2, metavar=('xmin', 'xmax'), type=float, help="select range for x axis")
    parser.add_argument("-y", "--ylim", nargs=2, metavar=('ymin', 'ymax'), type=float, help="select range for y axis")
    parser.add_argument("-k", "--key", action="store_true", help="plot key/legend in the graph")
    args = parser.parse_args()
    return args


def structure_ion_input():
    """
    Get console input for :mod:`.structure_ion`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_ion`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("ion", type=str, help="give path of ion complex file\nproduced by structure_fast.py")
    parser.add_argument("-p", "--plot", action="store_true", help="show graph of atom number in ion complex")
    parser.add_argument("-l", "--latex", nargs=2, metavar=('width', 'fraction'), type=str, help="document width in pts and fraction of this width\ndefaults for thesis and beamer")
    parser.add_argument("-x", "--xlim", nargs=2, metavar=('xmin', 'xmax'), type=float, help="select range for x axis")
    parser.add_argument("-y", "--ylim", nargs=2, metavar=('ymin', 'ymax'), type=float, help="select range for y axis")
    args = parser.parse_args()
    return args


def structure_water_input():
    """
    Get console input for :mod:`.structure_water`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_water`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("water", type=str, help="give path of water complex file\nproduced by structure_fast.py")
    parser.add_argument("-i", "--ion", nargs=1, metavar=('ion'), help="give path of ion complex file\nproduced by structure_fast.py",
                        default=False)
    parser.add_argument("-p", "--plot", action="store_true", help="show graph of atom number in water complex")
    parser.add_argument("-l", "--latex", nargs=2, metavar=('width', 'fraction'), type=str, help="document width in pts and fraction of this width\ndefaults for thesis and beamer")
    parser.add_argument("-k", "--key", action="store_true", help="plot key/legend in the graph\nonly works with ion selected")
    parser.add_argument("-x", "--xlim", nargs=2, metavar=('xmin', 'xmax'), type=float, help="select range for x axis")
    parser.add_argument("-y", "--ylim", nargs=2, metavar=('ymin', 'ymax'), type=float, help="select range for y axis")
    args = parser.parse_args()
    return args


def structure_radial_input():
    """
    Get console input for :mod:`.structure_radial`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_radial`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("radial", nargs='*', type=str, help="give path of radial data file\nproduced by structure_fast.py")
    parser.add_argument("-i", "--integrate", action="store_true", help="obtain coordination number from integration")
    parser.add_argument("-fwhm", "--fwhm", action="store_true", help="peak analysis")
    parser.add_argument("-p", "--plot", action="store_true", help="show graph of radial distribution function")
    parser.add_argument("-k", "--key", action="store_true", help="plot key/legend in the graph")
    parser.add_argument("-x", "--xlim", nargs=2, metavar=('xmin', 'xmax'), type=float, help="select range for x axis")
    parser.add_argument("-y", "--ylim", nargs=2, metavar=('ymin', 'ymax'), type=float, help="select range for y axis")
    parser.add_argument("-l", "--latex", nargs=2, metavar=('width', 'fraction'), type=str, help="document width in pts and fraction of this width\ndefaults for thesis and beamer")
    args = parser.parse_args()
    return args


def structure_angle_input():
    """
    Get console input for :mod:`.structure_angle`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_angle`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("angle", nargs="*", type=str, help="give path of angle data file\nproduced by structure_fast.py")
    parser.add_argument("-fwhm", "--fwhm", action="store_true", help="peak analysis")
    parser.add_argument("-sin", "--sinus", action="store_true", help="multiply angle distribution with sin(angle)")
    parser.add_argument("-p", "--plot", action="store_true", help="show graph of angle distribution function")
    parser.add_argument("-k", "--key", action="store_true", help="plot key/legend in the graph")
    parser.add_argument("-x", "--xlim", nargs=2, metavar=('xmin', 'xmax'), type=float, help="select range for x axis")
    parser.add_argument("-y", "--ylim", nargs=2, metavar=('ymin', 'ymax'), type=float, help="select range for y axis")
    parser.add_argument("-l", "--latex", nargs=2, metavar=('width', 'fraction'), type=str, help="document width in pts and fraction of this width\ndefaults for thesis and beamer")
    args = parser.parse_args()
    return args


def structure_gap_input():
    """
    Get console input for :mod:`.structure_gap`.
    Possible flags can be seen in usage of :ref:`Usage_paw_structure_gap`.

    Returns:
        :py:mod:`argparse` object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("prot", type=str, help="give path of CP-PAW protocol file")
    parser.add_argument("-p", "--plot", action="store_true", help="show graph of energies")
    parser.add_argument("-l", "--latex", nargs=2, metavar=('width', 'fraction'), type=str, help="document width in pts and fraction of this width\ndefaults for thesis and beamer")
    parser.add_argument("-x", "--xlim", nargs=2, type=float, help="select range for x axis (xmin, xmax)")
    parser.add_argument("-y1", "--ylim1", nargs=2, metavar=('ymin1', 'ymax1'), type=float,
                        help="select range for y axis of energy gap")
    parser.add_argument("-y2", "--ylim2", nargs=2, metavar=('ymin2', 'ymax2'), type=float,
                        help="select range for y axis of HOMO/LUMO energy")
    args = parser.parse_args()
    return args


def set_size(width, fraction="1", subplots=(1, 1)):
    """
    Set figure dimensions to avoid scaling in LaTeX.

    Args:
        width (str): document width in points or string of predefined document type
        fraction (str): fraction of the width which you wish the figure to occupy
        subplots (tuple(float), optional): number of rows and columns of subplots; CURRENTLY NOT IN USE

    Returns:
        tuple(float): dimensions of figure in inches
    """
    if width == 'thesis':
        width_pt = 426.79135
    elif width == 'beamer':
        width_pt = 307.28987
    else:
        width_pt = float(width)
    # Width of figure (in pts)
    fig_width_pt = width_pt * float(fraction)
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27
    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2
    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])
    return (fig_width_in, fig_height_in)
