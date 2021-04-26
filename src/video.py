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
"""
import numpy as np
import re
from collections import Counter

from . import utility

def video_save_xyz(root, snapshots):
    """
    Save information of selected snapshots to file XXX xyz movie file XXX.
    Args:
        root (str): root name for file
        snapshots (list[:class:`.Snap`]): snapshots to be saved
    Note:
        Takes atom ID and removes "_" (e.g. "H_" -> "H"). !SPECIES:NAME in structure file needs to fit the atom name in Avogadro.
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
        # time and iteration of snapshot
        f.write("%-14s%-14.8f%-14s%-14d\n" % ("TIME", snap.time, "ITERATION", snap.iter))
        data = np.array(snap.atoms[['id', 'pos']].values, dtype='<U32')
        data[:, 0] = np.char.replace(data[:, 0], "_", "")
        current_counter = Counter(data[:, 0])
        for k in counter.keys():
            for i in range(counter[k] - current_counter[k]):
                data = np.vstack((data, np.array([k, '100.0', '100.0', '100.0'], dtype='<U32')))
        np.savetxt(f, data, fmt="%-14s%-14s%-14s%-14s")
    f.close()
