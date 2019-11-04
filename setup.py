#!/usr/bin/env python

import sys,os,json
import shutil
from collections import defaultdict

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.sdist import sdist

###############
### autover ###


def get_setup_version(reponame):
    """
    Helper to get the current version from either git describe or the
    .version file (if available).
    """
    basepath = os.path.split(__file__)[0]
    version_file_path = os.path.join(basepath, reponame, '.version')
    try:
        from param import version
    except:
        version = None
    if version is not None:
        return version.Version.setup_version(basepath, reponame, archive_commit="$Format:%h$")
    else:
        print("WARNING: param>=1.6.0 unavailable. If you are installing a package, this warning can safely be ignored. If you are creating a package or otherwise operating in a git repository, you should install param>=1.6.0.")
        return json.load(open(version_file_path, 'r'))['version_string']


#######################
### bokeh extension ###


def _build_geoviewsjs():
    from bokeh.ext import build
    print("Building custom models:")
    geoviews_dir = os.path.join(os.path.dirname(__file__), "geoviews")
    build(geoviews_dir)


class CustomDevelopCommand(develop):
    """Custom installation for development mode."""

    def run(self):
        _build_geoviewsjs()
        develop.run(self)


class CustomInstallCommand(install):
    """Custom installation for install mode."""

    def run(self):
        _build_geoviewsjs()
        install.run(self)


class CustomSdistCommand(sdist):
    """Custom installation for sdist mode."""

    def run(self):
        _build_geoviewsjs()
        sdist.run(self)


_COMMANDS = {
    'develop': CustomDevelopCommand,
    'install': CustomInstallCommand,
    'sdist':   CustomSdistCommand,
}

try:
    from wheel.bdist_wheel import bdist_wheel

    class CustomBdistWheelCommand(bdist_wheel):
        """Custom bdist_wheel command to force cancelling qiskit-terra wheel
        creation."""

        def run(self):
            """Do nothing so the command intentionally fails."""
            _build_geoviewsjs()
            bdist_wheel.run(self)

    _COMMANDS['bdist_wheel'] = CustomBdistWheelCommand
except:
    pass

################
### examples ###

def check_pseudo_package(path):
    """
    Verifies that a fake subpackage path for assets (notebooks, svgs,
    pngs etc) both exists and is populated with files.
    """
    if not os.path.isdir(path):
        raise Exception("Please make sure pseudo-package %s exists." % path)
    else:
        assets = os.listdir(path)
        if len(assets) == 0:
            raise Exception("Please make sure pseudo-package %s is populated." % path)


excludes = ['DS_Store', '.log', 'ipynb_checkpoints']
packages = []
extensions = defaultdict(list)

def walker(top, names):
    """
    Walks a directory and records all packages and file extensions.
    """
    global packages, extensions
    if any(exc in top for exc in excludes):
        return
    package = top[top.rfind('geoviews'):].replace(os.path.sep, '.')
    packages.append(package)
    for name in names:
        ext = '.'.join(name.split('.')[1:])
        ext_str = '*.%s' % ext
        if ext and ext not in excludes and ext_str not in extensions[package]:
            extensions[package].append(ext_str)


def examples(path='geoviews-examples', verbose=False, force=False, root=__file__):
    """
    Copies the notebooks to the supplied path.
    """
    filepath = os.path.abspath(os.path.dirname(root))
    example_dir = os.path.join(filepath, './examples')
    if not os.path.exists(example_dir):
        example_dir = os.path.join(filepath, '../examples')
    if os.path.exists(path):
        if not force:
            print('%s directory already exists, either delete it or set the force flag' % path)
            return
        shutil.rmtree(path)
    ignore = shutil.ignore_patterns('.ipynb_checkpoints', '*.pyc', '*~')
    tree_root = os.path.abspath(example_dir)
    if os.path.isdir(tree_root):
        shutil.copytree(tree_root, path, ignore=ignore, symlinks=True)
    else:
        print('Cannot find %s' % tree_root)



def package_assets(example_path):
    """
    Generates pseudo-packages for the examples directory.
    """
    examples(example_path, force=True, root=__file__)
    for root, dirs, files in os.walk(example_path):
        walker(root, dirs+files)
    setup_args['packages'] += packages
    for p, exts in extensions.items():
        if exts:
            setup_args['package_data'][p] = exts


####################
### dependencies ###

_required = [
    'bokeh >=1.0.0',
    'cartopy >=0.16.0',  # prevents pip alone (requires external package manager)
    'holoviews >=1.11.1',
    'numpy >=1.0',
    'param >=1.6.1'
]

_recommended = [
    'datashader',
    'geopandas',
    'gdal',
    'netcdf4',
    'jupyter',
    'matplotlib>2.2',
    'pandas',
    'pyct',
    'scipy',
    'shapely',
    'xarray',
]

# can only currently run all examples with packages from conda-forge
_examples_extra = _recommended + [
    'iris',
    'xesmf',
    'filelock',
    'mock'
]

extras_require={
    'recommended': _recommended,
    'examples_extra': _examples_extra,
    'doc': _examples_extra + [
        'nbsite >=0.6.1',
        'sphinx_ioam_theme',
        'selenium',
    ],
    'tests': [
        'coveralls',
        'flake8',
        'nbsmoke >=0.2.0',
        'nose',
        'pytest'
    ],
}

extras_require['all'] = sorted(set(sum(extras_require.values(), [])))

# until pyproject.toml/equivalent is widely supported; meanwhile
# setup_requires doesn't work well with pip. Note: deliberately omitted from all.
extras_require['build'] = [
    'param >=1.9.0',
    'bokeh >=1.4.0',
    'nodejs >=9.11.1',
    'setuptools' # should make this pip now
]


########################
### package metadata ###


setup_args = dict(
    name='geoviews',
    version=get_setup_version("geoviews"),
    python_requires = '>=2.7',
    install_requires = _required,
    extras_require = extras_require,
    tests_require = extras_require['tests'],
    description='GeoViews is a Python library that makes it easy to explore and visualize geographical, meteorological, and oceanographic datasets, such as those used in weather, climate, and remote sensing research.',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    platforms=['Windows', 'Mac OS X', 'Linux'],
    license='BSD 3-Clause',
    url='http://geoviews.org',
    cmdclass=_COMMANDS,
    packages = find_packages() + packages,
    package_data={'geoviews': ['.version']},
    entry_points={
        'console_scripts': [
            'geoviews = geoviews.__main__:main'
        ]
    },
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"]
)

if __name__=="__main__":
    example_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'geoviews','examples')
    if 'develop' not in sys.argv:
        package_assets(example_path)

    setup(**setup_args)

    if os.path.isdir(example_path):
        shutil.rmtree(example_path)
