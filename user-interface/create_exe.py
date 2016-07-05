from distutils.core import setup
import py2exe
import os
import skimage
import numpy

dll_excludes = []
dll_excludes_b = ["api-ms-win-core-registry-l1-1-0.dll",
                "api-ms-win-core-string-l2-1-0.dll",
                "api-ms-win-core-processthreads-l1-1-2.dll",
                "api-ms-win-core-libraryloader-l1-2-1.dll",
                "api-ms-win-core-file-l1-2-1.dll",
                "api-ms-win-security-base-l1-2-0.dll",
                "api-ms-win-core-heap-l2-1-0.dll",
                "api-ms-win-core-rtlsupport-l1-2-0.dll",
                "api-ms-win-core-libraryloader-l1-2-0.dll",
                "api-ms-win-core-localization-l1-2-1.dll",
                "api-ms-win-core-sysinfo-l1-2-1.dll",
                "api-ms-win-core-errorhandling-l1-1-1.dll",
                "api-ms-win-core-heap-l1-2-0.dll",
                "api-ms-win-core-io-l1-1-1.dll",
                "api-ms-win-core-com-l1-1-1.dll",
                "api-ms-win-core-memory-l1-1-2.dll",
                "api-ms-win-core-version-l1-1-1.dll",
                "api-ms-win-core-version-l1-1-0.dll",
                "api-ms-win-eventing-provider-l1-1-0.dll"]

includes = ['distutils', 'scipy.sparse.csgraph._validation', 'scipy.special._ufuncs_cxx', 'scipy.linalg.cython_blas', 'scipy.linalg.cython_lapack',
            'skimage._shared.geometry', 'skimage.filters.rank.core_cy',
            'sklearn.svm', 'sklearn.utils.lgamma', 'sklearn.utils.weight_vector',
            'cv2'] #, 'skimage', 'numpy']#['scipy', 'numpy', 'skimage', 'PIL', 'difflib', 'locale', 'inspect', 'skimage._shared', 'skimage._shared.geometry', 'scipy.special._ufuncs_cxx', 'scipy.integrate', 'scipy.sparse.csgraph._validation', 'distutils']
excludes = ['pkg_resources', 'doctest', 'pdb', 'calendar', 'optparse', 'jsonschema', 'tornado', 'setuptools', 'distutils', 'matplotlib', 'Tkconstants', 'Tkinter']

orb_descriptor = os.path.join(skimage.data_dir, 'orb_descriptor_positions.txt')

setup(
    console=['create_ui.py'],
    data_files = [(os.path.join('skimage', 'data'), [orb_descriptor])],
    options = {
                    'py2exe': {
                            'bundle_files': 3,
                              'optimize': 2,
                              'includes': includes,
                              "dll_excludes": dll_excludes,
                              'excludes': excludes
                    }
               }
)