# SOURCE: https://github.com/pybind/python_example (6.07.2020)

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import sys
import setuptools
import pathlib
import os

#TODO: adapt file
#TODO: write MANIFEST.in for including documentation


__version__ = '1.0.1'

here = pathlib.Path(__file__).parent.resolve()

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path

    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __str__(self):
        import pybind11
        return pybind11.get_include()


ext_modules = [
    Extension(
        'paw_structure.hbonds_c',
        # Sort input source files to ensure bit-for-bit reproducible builds
        # (https://github.com/pybind/python_example/pull/53)
        sorted(['src/calc_c.cpp', 'src/pbc_c.cpp', 'src/hbonds_c.cpp']),
        language='c++',
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
        ],
    ),
    Extension(
        'paw_structure.radial_c',
        # Sort input source files to ensure bit-for-bit reproducible builds
        # (https://github.com/pybind/python_example/pull/53)
        sorted(['src/calc_c.cpp', 'src/pbc_c.cpp', 'src/radial_c.cpp']),
        language='c++',
        include_dirs=[
            # Path to pybind11 headers
            get_pybind_include(),
        ],
    ),
]


# cf http://bugs.python.org/issue26689
def has_flag(compiler, flagname):
    """Return a boolean indicating whether a flag name is supported on
    the specified compiler.
    """
    import tempfile
    import os
    with tempfile.NamedTemporaryFile('w', suffix='.cpp', delete=False) as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        fname = f.name
    try:
        compiler.compile([fname], extra_postargs=[flagname])
    except setuptools.distutils.errors.CompileError:
        return False
    finally:
        try:
            os.remove(fname)
        except OSError:
            pass
    return True


def cpp_flag(compiler):
    """Return the -std=c++[11/14/17] compiler flag.

    The newer version is prefered over c++11 (when it is available).
    """
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']

    for flag in flags:
        if has_flag(compiler, flag):
            return flag

    raise RuntimeError('Unsupported compiler -- at least C++11 support '
                       'is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc'],
        'unix': [],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')

        for ext in self.extensions:
            ext.define_macros = [('VERSION_INFO', '"{}"'.format(self.distribution.get_version()))]
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


setup(
    name='paw_structure',
    version=__version__,
    author='Lukas Rump',
    author_email='lukas.rump@stud.uni-goettingen.de',
    url='https://github.com/lksrmp/paw_structure',
    description='CP-PAW structure analysis',
    long_description='Structural analysis of trajectory output by CP-PAW code with focus on water and ion in water analysis.',
    package_dir={'paw_structure': 'src'},
    packages=['paw_structure'],# find_packages(where='src'),
    ext_modules=ext_modules,
    setup_requires=['pybind11>=2.5.0'],
    install_requires=['pybind11>=2.5.0',
                      'numpy>=1.17.0',
                      'miniutils',
                      'pandas',
                      'matplotlib',
                      'argparse',
                      'scipy',
                      'Sphinx',
                      'sphinx_rtd_theme',
                      'autodocsumm',],
    cmdclass={'build_ext': BuildExt},
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "paw_structure_fast = paw_structure.structure_fast:main",
            "paw_structure_ion = paw_structure.structure_ion:main",
            "paw_structure_water = paw_structure.structure_water:main",
            "paw_structure_radial = paw_structure.structure_radial:main"
            ]
    }
)
