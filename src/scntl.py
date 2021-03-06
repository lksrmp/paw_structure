"""
paw_structure.scntl
-------------------
Read control input file for :mod:`.structure_fast`.

Main routine is :func:`.scntl_read`.

Dependencies:
    :py:mod:`os`
    :mod:`.utility`


.. autosummary::

      scntl_read
      scntl_read_hbonds
      scntl_read_ion
      scntl_read_radial
      scntl_read_scntl
      scntl_read_tra
      scntl_read_water
      scntl_text

Todo:
    Remove forced line structure.
    If parameter is initialized with **None**, check that first and then compare keywords.
"""

import os
# MODULES WITHIN PROJECT
from . import utility


########################################################################################################################
# OBTAIN TEXT AND BRACKET INDICES (GIVEN BY !KEY ... !END)
# WARNING: METHOD IS LINE SENSITIVE, EACH ARGUMENT MUST HAVE ITS OWN LINE
########################################################################################################################
# INPUT
# str root              root name of the control file
# str ext (optional)    extension for the control file: name = root + ext
#####
# OUTPUT
# list list str text    each element is a list of words in a line
# dict brackets         dictionary to save position of each bracket for later extraction
########################################################################################################################
def scntl_text(root, ext='.scntl'):
    """
    Read text from :ref:`control file ".scntl" <Control>` file and identify different :ref:`control blocks <Control_General>`.

    Args:
        root (str): root name for the control file
        ext (str, optional): Default ".scntl". DO NOT USE!

    Returns:
        list[list[str]]: text from the control file; each line is a list of words within the outer list
        dict: dictionary with control blocks and their position within the text

    Todo:
        Remove forced line structure (flatten text and search for key words).
        Implement variable extension.
    """
    path = root + ext
    # open file
    try:
        f = open(path)
    except IOError:
        utility.err_file('scntl_text', path)
    text = f.readlines()
    f.close()
    for i in range(len(text)):
        text[i] = text[i].split()  # split the lines gives list of the words
    # dictionary to save information about the different blocks
    brackets = {}
    # entry to store unused lines
    brackets['DELETE'] = []
    # list to keep track of open brackets
    current_bracket = []
    for i in range(len(text)):
        if len(text[i]) > 0:
            # check for trigger for beginning / end of a block
            if text[i][0][0] == "!":
                # check for different keywords that can start a block
                if text[i][0].casefold() == '!SCNTL'.casefold():
                    brackets['!SCNTL'] = [i]
                    current_bracket = current_bracket + ['!SCNTL']
                elif text[i][0].casefold() == '!TRA'.casefold():
                    brackets['!TRA'] = [i]
                    current_bracket.append('!TRA')
                elif text[i][0].casefold() == '!ION'.casefold():
                    brackets['!ION'] = [i]
                    current_bracket.append('!ION')
                elif text[i][0].casefold() == '!WATER'.casefold():
                    brackets['!WATER'] = [i]
                    current_bracket.append('!WATER')
                elif text[i][0].casefold() == '!HBONDS'.casefold():
                    brackets['!HBONDS'] = [i]
                    current_bracket.append('!HBONDS')
                elif text[i][0].casefold() == '!RADIAL'.casefold():
                    brackets['!RADIAL'] = [i]
                    current_bracket.append('!RADIAL')
                elif text[i][0].casefold() == '!ANGLE'.casefold():
                    brackets['!ANGLE'] = [i]
                    current_bracket.append('!ANGLE')
                # check if bracket is being closed
                elif text[i][0].casefold() == '!END'.casefold():
                    try:
                        brackets[current_bracket[-1]].append(i)
                        del current_bracket[-1]
                    except IndexError:
                        utility.err('sctnl_read', 0, [])
                # otherwise an unused block starts
                else:
                    brackets['DELETE'].append(i)
                    current_bracket.append('DELETE')
    # check if brackets are still open at end of file
    if len(current_bracket) > 0:
        utility.err('scntl_text', 1, [len(current_bracket)])
    return text, brackets


def scntl_read_tra(text, idx):
    """
    Interpret the control block :ref:`Control_TRA` for :mod:`.tra`.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block

    Returns:
        dict: dictionary containing all information obtained from the control block

    Todo:
        Implement selection of first and last iteration to avoid exact selection.
    """
    text = text[idx[0] + 1:idx[1]]
    tra_dict = {
        'T1': None,
        'T2': None,
        'N': None,
        'SAVE': None,
        'LOAD': None
    }
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(tra_dict.keys())]:
                tra_dict[line[0].upper()] = line[1]
    # check for save of snapshots
    if tra_dict['SAVE'] is None:
        tra_dict['SAVE'] = False
    else:
        if tra_dict['SAVE'].casefold() == 'true':
            tra_dict['SAVE'] = True
        else:
            tra_dict['SAVE'] = False

    # check for load of snapshots, overwrites arguments T1, T2, N
    if tra_dict['LOAD'] is None:
        tra_dict['LOAD'] = False
        if tra_dict['T1'] is None or tra_dict['T2'] is None or tra_dict['N'] is None:
            utility.err('scntl_read', 0, ['!TRA'], info="T1 T2 N")
        if tra_dict['T1'].casefold() == 'start':
            tra_dict['T1'] = "START"
        else:
            tra_dict['T1'] = float(tra_dict['T1'])
        if tra_dict['T2'].casefold() == 'end':
            tra_dict['T2'] = "END"
        else:
            tra_dict['T2'] = float(tra_dict['T2'])
        tra_dict['N'] = int(tra_dict['N'])
    else:
        if tra_dict['LOAD'].casefold() == 'true':
            tra_dict['LOAD'] = True
        else:
            tra_dict['LOAD'] = False
            # check for necessary arguments if snapshots are not loaded
            if tra_dict['T1'] is None or tra_dict['T2'] is None or tra_dict['N'] is None:
                utility.err('scntl_read', 0, ['!TRA'], info="T1 T2 N")
            if tra_dict['T1'].casefold() == 'start':
                tra_dict['T1'] = 'START'
            else:
                tra_dict['T1'] = float(tra_dict['T1'])
            if tra_dict['T2'].casefold() == 'end':
                tra_dict['T2'] = "END"
            else:
                tra_dict['T2'] = float(tra_dict['T2'])
            tra_dict['N'] = int(tra_dict['N'])
    return tra_dict


def scntl_read_ion(text, idx):
    """
    Interpret the control block :ref:`Control_ION` for :mod:`.ion`.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block

    Returns:
        dict: dictionary containing all information obtained from the control block
    """
    text = text[idx[0] + 1:idx[1]]
    ion_dict = {
        'ID1': None,
        'ID2': None,
        'ID3': None,
        'CUT1': None,
        'CUT2': None
    }
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(ion_dict.keys())]:
                ion_dict[line[0].upper()] = line[1]
    if ion_dict['ID1'] is None or ion_dict['ID2'] is None or ion_dict['ID3'] is None:
        utility.err('scntl_read', 0, ['!ION'], info="ID1 ID2 ID3")
    if ion_dict['CUT1'] is None:
        ion_dict['CUT1'] = 3.0
    else:
        ion_dict['CUT1'] = float(ion_dict['CUT1'])
    if ion_dict['CUT2'] is None:
        ion_dict['CUT2'] = 1.4
    else:
        ion_dict['CUT2'] = float(ion_dict['CUT2'])
    return ion_dict


def scntl_read_water(text, idx):
    """
    Interpret the control block :ref:`Control_WATER` for :mod:`.water`.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block

    Returns:
        dict: dictionary containing all information obtained from the control block
    """
    text = text[idx[0] + 1:idx[1]]
    water_dict = {
        'ID1': None,
        'ID2': None,
        'CUT': None
    }
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(water_dict.keys())]:
                water_dict[line[0].upper()] = line[1]
    if water_dict['ID1'] is None or water_dict['ID2'] is None:
        utility.err('scntl_read', 0, ['!WATER'], info="ID1 ID2")
    if water_dict['CUT'] is None:
        water_dict['CUT'] = 1.4
    else:
        water_dict['CUT'] = float(water_dict['CUT'])
    return water_dict


def scntl_read_hbonds(text, idx):
    """
    Interpret the control block :ref:`Control_HBONDS` for :mod:`.hbonds`.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block

    Returns:
        dict: dictionary containing all information obtained from the control block
    """
    text = text[idx[0] + 1:idx[1]]
    hbonds_dict = {
        'ID1': None,
        'ID2': None,
        'CUT1': None,
        'CUT2': None,
        'ANGLE': None,
        'NAMES': None
        # USED FOR OLD CRITERION
        # 'OO_MIN': None,
        # 'OO_MAX': None,
        # 'G_FACTOR': None,
        # 'THRESHOLD': None
    }
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(hbonds_dict.keys())]:
                if line[0].casefold() == 'NAMES'.casefold():
                    hbonds_dict[line[0].upper()] = line[1:]
                else:
                    hbonds_dict[line[0].upper()] = line[1]
    if hbonds_dict['ID1'] is None or hbonds_dict['ID2'] is None:
        utility.err('scntl_read', 0, ['!HBONDS'], info=" ID1 ID2")
    if hbonds_dict['CUT1'] is None:
        hbonds_dict['CUT1'] = 3.5
    else:
        hbonds_dict['CUT1'] = float(hbonds_dict['CUT1'])
    if hbonds_dict['CUT2'] is None:
        hbonds_dict['CUT2'] = 3.1
    else:
        hbonds_dict['CUT2'] = float(hbonds_dict['CUT2'])
    if hbonds_dict['ANGLE'] is None:
        hbonds_dict['ANGLE'] = 30.0
    else:
        hbonds_dict['ANGLE'] = float(hbonds_dict['ANGLE'])

    # USED FOR OLD CRITERION
    # if hbonds_dict['OO_MIN'] is None:
    #     hbonds_dict['OO_MIN'] = 2.75
    # else:
    #     hbonds_dict['OO_MIN'] = float(hbonds_dict['OO_MIN'])
    # if hbonds_dict['OO_MAX'] is None:
    #     hbonds_dict['OO_MAX'] = 3.5
    # else:
    #     hbonds_dict['OO_MAX'] = float(hbonds_dict['OO_MAX'])
    # if hbonds_dict['G_FACTOR'] is None:
    #     hbonds_dict['G_FACTOR'] = 0.5
    # else:
    #     hbonds_dict['G_FACTOR'] = float(hbonds_dict['G_FACTOR'])
    # if hbonds_dict['THRESHOLD'] is None:
    #     hbonds_dict['THRESHOLD'] = 0.5
    # else:
    #     hbonds_dict['THRESHOLD'] = float(hbonds_dict['THRESHOLD'])
    return hbonds_dict


def scntl_read_radial(text, idx):
    """
    Interpret the control block :ref:`Control_RADIAL` for :mod:`.radial`.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block

    Returns:
        dict: dictionary containing all information obtained from the control block


    Todo:
        Implement name identification for central atoms.
    """
    text = text[idx[0] + 1:idx[1]]
    radial_dict = {
        'ID1': None,
        'ID2': None,
        'CUT': None,
        'NBINS': None,
        'T1': None,
        'T2': None,
        'N': None,
        'TRA_EXTRACT': True
    }
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(radial_dict.keys())]:
                radial_dict[line[0].upper()] = line[1]
    if radial_dict['CUT'] is None:
        radial_dict['CUT'] = 5.0
    else:
        radial_dict['CUT'] = float(radial_dict['CUT'])
    if radial_dict['NBINS'] is None:
        radial_dict['NBINS'] = 1000
    else:
        radial_dict['NBINS'] = int(radial_dict['NBINS'])
    if radial_dict['ID1'] is None or radial_dict['ID2'] is None:
        utility.err('scntl_read', 0, ['!RADIAL'], info=" ID1 ID2")
    # check for necessary arguments if snapshots are not loaded
    if radial_dict['T1'] is None or radial_dict['T2'] is None or radial_dict['N'] is None:
        radial_dict['TRA_EXTRACT'] = False
    else:
        radial_dict['TRA_EXTRACT'] = True
        if radial_dict['T1'].casefold() == 'start':
            radial_dict['T1'] = "START"
        else:
            radial_dict['T1'] = float(radial_dict['T1'])
        if radial_dict['T2'].casefold() == 'end':
            radial_dict['T2'] = "END"
        else:
            radial_dict['T2'] = float(radial_dict['T2'])
        radial_dict['N'] = int(radial_dict['N'])
    return radial_dict


def scntl_read_angle(text, idx):
    """
    Interpret the control block :ref:`Control_ANGLE` for :mod:`.angle`.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block

    Returns:
        dict: dictionary containing all information obtained from the control block


    Todo:
        Implement name identification for central atoms.
    """
    text = text[idx[0] + 1:idx[1]]
    angle_dict = {
        'ID1': None,
        'ID2': None,
        'CUT': None,
        'NBINS': None,
        'T1': None,
        'T2': None,
        'N': None,
        'TRA_EXTRACT': True
    }
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(angle_dict.keys())]:
                angle_dict[line[0].upper()] = line[1]
    if angle_dict['CUT'] is None:
        angle_dict['CUT'] = 5.0
    else:
        angle_dict['CUT'] = float(angle_dict['CUT'])
    if angle_dict['NBINS'] is None:
        angle_dict['NBINS'] = 1000
    else:
        angle_dict['NBINS'] = int(angle_dict['NBINS'])
    if angle_dict['ID1'] is None or angle_dict['ID2'] is None:
        utility.err('scntl_read', 0, ['!RADIAL'], info=" ID1 ID2")
    # check for necessary arguments if snapshots are not loaded
    if angle_dict['T1'] is None or angle_dict['T2'] is None or angle_dict['N'] is None:
        angle_dict['TRA_EXTRACT'] = False
    else:
        angle_dict['TRA_EXTRACT'] = True
        if angle_dict['T1'].casefold() == 'start':
            angle_dict['T1'] = "START"
        else:
            angle_dict['T1'] = float(angle_dict['T1'])
        if angle_dict['T2'].casefold() == 'end':
            angle_dict['T2'] = "END"
        else:
            angle_dict['T2'] = float(angle_dict['T2'])
        angle_dict['N'] = int(angle_dict['N'])
    return angle_dict


def scntl_read_scntl(text, idx, delete):
    """
    Interpret the control block :ref:`Control_SCNTL` >for general information.

    Args:
        text (list[list[str]]): text from the control file; each line is a list of words within the outer list
        idx (list[int]): list with two indices marking beginning and end of control block
        delete (list[list[int]]): contains begin and end of each previously read block to avoid double reading

    Returns:
        dict: dictionary containing all information obtained from the control block

    .. Todo::

        Implement better control over different branches and hierarchies.
    """
    idx_set = set(range(idx[0] + 1, idx[1])) - set(delete)
    control_dict = {
        'ROOT': None,
        'PBC_FOLDING': None
    }
    text = [text[i] for i in idx_set]
    for line in text:
        if len(line) > 1:
            if line[0].casefold() in [x.casefold() for x in list(control_dict.keys())]:
                control_dict[line[0].upper()] = line[1]
    if control_dict['PBC_FOLDING'] is not None:
        if control_dict['PBC_FOLDING'].casefold() == 'true':
            control_dict['PBC_FOLDING'] = True
        else:
            control_dict['PBC_FOLDING'] = False
    else:
        control_dict['PBC_FOLDING'] = False
    if control_dict['ROOT'] is None:
        control_dict['ROOT'] = False
    return control_dict


def scntl_read(root):
    """
    Read and interpret the :ref:`control file ".scntl" <Control>`.

    Args:
        root (str): root name for the control file

    Returns:
        dict[dict]: dictionary of all dictionaries obtained from all the control blocks

    Todo:
        Error checking with !TRA and !RADIAL does not work properly.
    """
    scntl_dict = {}
    delete = []
    text, brackets = scntl_text(root)
    # read !TRA control block if present
    if '!TRA' in brackets.keys():
        tra_dict = scntl_read_tra(text, brackets['!TRA'])
        scntl_dict['!TRA'] = tra_dict
        delete = delete + [*range(brackets['!TRA'][0], brackets['!TRA'][1] + 1)]
    # read !ION control block if present
    if '!ION' in brackets.keys():
        ion_dict = scntl_read_ion(text, brackets['!ION'])
        scntl_dict['!ION'] = ion_dict
        delete = delete + [*range(brackets['!ION'][0], brackets['!ION'][1] + 1)]
    # read !WATER control block if present
    if '!WATER' in brackets.keys():
        water_dict = scntl_read_water(text, brackets['!WATER'])
        scntl_dict['!WATER'] = water_dict
        delete = delete + [*range(brackets['!WATER'][0], brackets['!WATER'][1] + 1)]
    # read !HBONDS control block if present
    if '!HBONDS' in brackets.keys():
        hbonds_dict = scntl_read_hbonds(text, brackets['!HBONDS'])
        scntl_dict['!HBONDS'] = hbonds_dict
        delete = delete + [*range(brackets['!HBONDS'][0], brackets['!HBONDS'][1] + 1)]
    # read !RADIAL control block if present
    if '!RADIAL' in brackets.keys():
        radial_dict = scntl_read_radial(text, brackets['!RADIAL'])
        scntl_dict['!RADIAL'] = radial_dict
        delete = delete + [*range(brackets['!RADIAL'][0], brackets['!RADIAL'][1] + 1)]
    # read !ANGLE control block if present
    if '!ANGLE' in brackets.keys():
        angle_dict = scntl_read_angle(text, brackets['!ANGLE'])
        scntl_dict['!ANGLE'] = angle_dict
        delete = delete + [*range(brackets['!ANGLE'][0], brackets['!ANGLE'][1] + 1)]
    # delete unused blocks
    for i in range(int(len(brackets['DELETE']) / 2)):
        delete = delete + [*range(brackets['DELETE'][i*2], brackets['DELETE'][i*2+1] + 1)]
    # read !SCNTL control block
    scntl_dict['GENERAL'] = scntl_read_scntl(text, brackets['!SCNTL'], delete)
    # ensure existence of !TRA except only !RADIAL is given with LOAD or its own data extraction active
    #TODO: error checking does not work properly
    if '!TRA' not in scntl_dict.keys():
        if '!RADIAL' in scntl_dict.keys() and '!ANGLE' in scntl_dict.keys():
            if not (set(['GENERAL', '!RADIAL', '!ANGLE']) == set(scntl_dict.keys())):
                if not (scntl_dict['!RADIAL']['TRA_EXTRACT'] and scntl_dict['!ANGLE']['TRA_EXTRACT']):
                    utility.err('scntl_read', 1, [root], info="IF ONLY !RADIAL AND !ANGLE ARE USED, PROVIDE T1 T2 N")
        elif '!RADIAL' in scntl_dict.keys() and not ('!ANGLE' in scntl_dict.keys()):
            if not (set(['GENERAL', '!RADIAL']) == set(scntl_dict.keys())):
                if not (scntl_dict['!RADIAL']['TRA_EXTRACT']):
                    utility.err('scntl_read', 1, [root], info="IF ONLY !RADIAL IS USED, PROVIDE T1 T2 N")
        elif not ('!RADIAL' in scntl_dict.keys()) and '!ANGLE' in scntl_dict.keys():
            if not (set(['GENERAL', '!ANGLE']) == set(scntl_dict.keys())):
                if not (scntl_dict['!ANGLE']['TRA_EXTRACT']):
                    utility.err('scntl_read', 1, [root], info="IF ONLY !ANGLE IS USED, PROVIDE T1 T2 N")
    return scntl_dict