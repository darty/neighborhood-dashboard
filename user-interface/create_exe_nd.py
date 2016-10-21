from distutils.core import setup
import py2exe
import os
import skimage
import numpy
import geopy
import sys

# After building, manually copy the following files:
# from C:\Users\<usename>\Anaconda2\Library\bin
# libiomp5md.dll
# mkl_*.dll

sys.setrecursionlimit(5000)

dll_excludes = []

includes = ['distutils', 'scipy.sparse.csgraph._validation', 'scipy.special._ufuncs_cxx', 'scipy.linalg.cython_blas',
            'scipy.linalg.cython_lapack', 'skimage._shared.geometry', 'skimage.filters.rank.core_cy',
            'sklearn.svm', 'sklearn.utils.lgamma', 'sklearn.utils.weight_vector', 'geopy']

excludes = ['pkg_resources', 'doctest', 'pdb', 'calendar', 'optparse', 'jsonschema', 'tornado', 'setuptools',
            'distutils', 'matplotlib', 'Tkconstants', 'Tkinter']

orb_descriptor = os.path.join(skimage.data_dir, 'orb_descriptor_positions.txt')
# datafiles = [(os.path.join('skimage', 'data'), [orb_descriptor])]
# datafiles.extend(matplotlib.get_py2exe_datafiles())

setup(
    console=['create_nd.py'],
    # data_files = datafiles,
    zipfile=None,
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'optimize': 2,
            'includes': includes,
            "dll_excludes": dll_excludes,
            'excludes': excludes
        }
    }
)
