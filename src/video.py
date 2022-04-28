"""
paw_structure.video
-------------------
Save information of selected snapshots to xyz video file. Only usable after import to Python.

Dependencies:
    :py:mod:`collections`
    :py:mod:`numpy`
    :py:mod:`re`
    :mod:`.utility`

.. autosummary::

    video_save_xyz

.. Todo::
    create command line access to tool
"""
import numpy as np
import re
from collections import Counter

from . import utility


def video_save_xyz(root, snapshots, cell=False):
    """
    Save information of selected snapshots to file XXX xyz movie file XXX.
    Args:
        root (str): root name for file
        snapshots (list[:class:`.Snap`]): snapshots to be saved
    Note:
        Takes atom ID and removes "\_" (e.g. "H\_" -> "H"). !SPECIES:NAME in structure file needs to fit the atom name in Avogadro.
    """
    path = root + '_movie.xyz'
    try:
        f = open(path, 'w')
    except IOError:
        utility.err_file('tra_save_xyz', path)
    max_atoms = np.max([len(snap.atoms) for snap in snapshots])
    names = set()
    for snap in snapshots:
        names = names.union(set(snap.atoms['name'].values))
    ID = []
    regex = re.compile('[^a-zA-Z]')
    for name in names:
        ID.append(regex.sub("", name))
    counter = Counter(ID)
    #placeholder = np.array(['X', '100.0', '100.0', '100.0'], dtype='<U32')
    # write information for different time steps
    for snap in snapshots:
        f.write("%d\n" % len(ID))
        if(cell):
            f.write('Lattice=" ')
            f.write(" ".join(map(str, snap.cell.ravel())))
            f.write(' "\n')
        else:
            # time and iteration of snapshot
            f.write("%-14s%-14.8f%-14s%-14d\n" % ("TIME", snap.time, "ITERATION", snap.iter))
        data = snap.atoms[['id', 'pos']].copy()
        data['id'] = data['id'].str.replace("_", "")
        data['id'] = data['id'].str.capitalize()
        # TODO: deal with fluctuation of atoms in viewbox
        # current_counter = Counter(data[:, 0])
        # for k in counter.keys():
        #     for i in range(counter[k] - current_counter[k]):
        #         data = np.vstack((data, np.array([k, '100.0', '100.0', '100.0'])))
        np.savetxt(f, data.values, fmt="%-14.10s%14.8f%14.8f%14.8f")
    f.close()
