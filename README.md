<img src="/doc/_static/logo_stacked.png" width="200"/><br>

-----------------

**Geographic visualizations for HoloViews.**

|    |    |
| --- | --- |
| Build Status | [![Linux/MacOS Build Status](https://travis-ci.org/holoviz/geoviews.svg?branch=master&logo=travis)](https://travis-ci.org/holoviz/geoviews) [![Windows Build status](https://img.shields.io/appveyor/ci/holoviz-developers/geoviews/master.svg?logo=appveyor)](https://ci.appveyor.com/project/holoviz-developers/geoviews/branch/master) |
| Coverage | [![codecov](https://codecov.io/gh/holoviz/geoviews/branch/master/graph/badge.svg)](https://codecov.io/gh/holoviz/geoviews) |
| Latest dev release | [![Github tag](https://img.shields.io/github/tag/holoviz/geoviews.svg?label=tag&colorB=11ccbb)](https://github.com/holoviz/geoviews/tags) |
| Latest release | [![Github release](https://img.shields.io/github/release/holoviz/geoviews.svg?label=tag&colorB=11ccbb)](https://github.com/holoviz/geoviews/releases) [![PyPI version](https://img.shields.io/pypi/v/geoviews.svg?colorB=cc77dd)](https://pypi.python.org/pypi/geoviews) [![geoviews version](https://img.shields.io/conda/v/pyviz/geoviews.svg?colorB=4488ff&style=flat)](https://anaconda.org/pyviz/geoviews) [![conda-forge version](https://img.shields.io/conda/v/conda-forge/geoviews.svg?label=conda%7Cconda-forge&colorB=4488ff)](https://anaconda.org/conda-forge/geoviews) [![defaults version](https://img.shields.io/conda/v/anaconda/geoviews.svg?label=conda%7Cdefaults&style=flat&colorB=4488ff)](https://anaconda.org/anaconda/geoviews) |
| Docs | [![gh-pages](https://img.shields.io/github/last-commit/holoviz/geoviews/gh-pages.svg)](https://github.com/holoviz/geoviews/tree/gh-pages) [![site](https://img.shields.io/website-up-down-green-red/http/geoviews.pyviz.org.svg)](http://geoviews.pyviz.org) |


## What is it?

GeoViews is a Python library that makes it easy to explore and
visualize any data that includes geographic locations.  It has
particularly powerful support for multidimensional meteorological
and oceanographic datasets, such as those used in weather, climate,
and remote sensing research, but is useful for almost anything
that you would want to plot on a map!  You can see lots of example
notebooks at [geoviews.org](https://geoviews.org), and a good
overview is in our [blog post announcement](https://www.continuum.io/blog/developer-blog/introducing-geoviews).

GeoViews is built on the [HoloViews](https://holoviews.org) library for
building flexible visualizations of multidimensional data.  GeoViews
adds a family of geographic plot types based on the
[Cartopy](http://scitools.org.uk/cartopy) library, plotted using
either the [Matplotlib](http://matplotlib.org) or
[Bokeh](https://bokeh.org) packages.

Each of the new GeoElement plot types is a new HoloViews Element that
has an associated geographic projection based on ``cartopy.crs``. The
GeoElements currently include ``Feature``, ``WMTS``, ``Tiles``,
``Points``, ``Contours``, ``Image``, ``QuadMesh``, ``TriMesh``,
``RGB``, ``HSV``, ``Labels``, ``Graph``, ``HexTiles``, ``VectorField``
and ``Text`` objects, each of which can easily be overlaid in the same
plots. E.g. an object with temperature data can be overlaid with
coastline data using an expression like ``gv.Image(temperature) *
gv.Feature(cartopy.feature.COASTLINE)``. Each GeoElement can also be
freely combined in layouts with any other HoloViews Element , making
it simple to make even complex multi-figure layouts of overlaid
objects.

## Installation

You can install GeoViews and its dependencies using conda:

```
conda install -c pyviz geoviews
```

Alternatively you can also install the geoviews-core package, which
only installs the minimal dependencies required to run geoviews:

```
conda install -c pyviz geoviews-core
```

Once installed you can copy the examples into the current directory
using the ``geoviews`` command and run them using the Jupyter
notebook:

```
geoviews examples
cd geoviews-examples
jupyter notebook
```

(Here `geoviews examples` is a shorthand for `geoviews copy-examples
--path geoviews-examples && geoviews fetch-data --path
geoviews-examples`.)

To work with JupyterLab you will also need the PyViz JupyterLab
extension:

```
conda install -c conda-forge jupyterlab
jupyter labextension install @pyviz/jupyterlab_pyviz
```

Once you have installed JupyterLab and the extension launch it with:

```
jupyter-lab
```

If you want to try out the latest features between releases, you can
get the latest dev release by specifying `-c pyviz/label/dev` in place
of `-c pyviz`.

### Additional dependencies

If you need to install libraries only available from conda-forge, such
as Iris (to use data stored in Iris cubes) or xesmf, you should
install from conda-forge:

```
conda create -n env-name -c pyviz -c conda-forge geoviews iris xesmf
conda activate env-name
```

-----

GeoViews itself is also installable using `pip`, but to do that you
will first need to have installed the [dependencies of cartopy](http://scitools.org.uk/cartopy/docs/latest/installing.html#requirements),
or else have set up your system to be able to build them.


## About HoloViz

GeoViews is part of the HoloViz ecosystem, which strives to make browser-based data
visualization in Python easier to use, easier to learn, and more powerful.
See [holoviz.org](http://holoviz.org) for related packages that you can use with GeoViews and
[status.pyviz.org](http://status.pyviz.org) for the current status of projects.
