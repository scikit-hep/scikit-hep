Scikit-HEP project - welcome!
=============================

The `Scikit-HEP project` is a community-driven and community-oriented project
with the aim of providing Particle Physics at large with a Python package
containing core and common tools. The project started in Autumn 2016 and is under active development.

It is not just about providing common tools for the community. It is also about improving on discoverability of utility packages
and projects.

Scikit-HEP should be seen as a toolset of Python packages.
The project defines a set of five *pillars*, which are seen to embrace
all major topics involved in a physicist's work. These are:

  * **Datasets**: data in various sources, such as ROOT, Numpy/Pandas, databases, wrapped in a common interface.
  * **Aggregations**: e.g. histograms that summarize or project a dataset.
  * **Modeling**: data models and fitting utilities.
  * **Simulation**: wrappers for Monte Carlo engines and other generators of simulated data.
  * **Visualization**: interface to graphics engines, from ROOT and Matplotlib to maybe even d3 or plot.ly.

.. _index_toolset_packages:

Toolset packages
----------------

To get started, have a look at our `GitHub repository`_.

The list of presently available packages follows, together with a very short description of their goals:

**Interoperability and data manipulation:**

* `awkward-array <https://github.com/scikit-hep/awkward-array>`_: manipulate arrays of complex data structures as easily as Numpy.
* `uproot <https://github.com/scikit-hep/uproot>`_: minimalist ROOT I/O in pure Python and Numpy.
* `uproot-methods <https://github.com/scikit-hep/uproot-methods>`_: Pythonic behaviours for non-I/O related ROOT classes.
* `root_numpy <https://github.com/scikit-hep/root_numpy>`_: interface between ROOT and NumPy.
* `root_pandas <https://github.com/scikit-hep/root_pandas>`_: module for conveniently loading/saving ROOT files as pandas DataFrames.

**Particles and decays:**

* `Particle <https://github.com/scikit-hep/particle>`_: PDG particle data and identification codes.
* `DecayLanguage <https://github.com/scikit-hep/decaylanguage>`_: describe and convert particle decays between digital representations.

**Histogramming:**

* `boost-histogram <https://github.com/scikit-hep/boost-histogram>`_: Python bindings for the C++14 Boost::Histogram library.
* `histbook <https://github.com/scikit-hep/histbook>`_: versatile, high-performance histogram toolkit for Numpy.

**Fitting:**

* `iminuit <https://github.com/scikit-hep/iminuit>`_: MINUIT from Python - Fitting like a boss.
* `probfit <https://github.com/scikit-hep/probfit>`_: Cost function builder. For fitting distributions.

**Simulation:**

* `pyhepmc <https://github.com/scikit-hep/pyhepmc>`_: next generation Python bindings for HepMC3.

**Machine Learning:**

* `NNDrone <https://github.com/scikit-hep/NNDrone>`_: collection of tools and algorithms to enable conversion of HEP ML to mass usage model.

**Visualisation:**

* `vegascope <https://github.com/scikit-hep/vegascope>`_: view Vega/Vega-Lite plots in your web browser from local or remote Python processes.

**Miscellaneous:**

* `formulate <https://github.com/scikit-hep/formulate>`_: easy conversions between different styles of expressions.
* `hepunits <https://github.com/scikit-hep/hepunits>`_: units and constants in the HEP system of units.
* `numpythia <https://github.com/scikit-hep/numpythia>`_: interface between Pythia and NumPy.
* `pyjet <https://github.com/scikit-hep/pyjet>`_: interface between FastJet and NumPy.
* `scikit-hep <https://github.com/scikit-hep/scikit-hep>`_: toolset of interfaces and tools for Particle Physics.
* `scikit-hep-testdata <https://github.com/scikit-hep/scikit-hep-testdata>`_: common package to provide example files (e.g., ROOT) for testing and developing packages against.

In some cases, the packages have to do with bridging between different technologies and/or popular packages
from the Python scientific software stack.

.. toctree::
   :hidden:
   :maxdepth: 2

   index.rst
   faq.rst
   get-in-touch.rst
   documentation.rst
   resources.rst

..   contributing.rst

.. _GitHub repository : https://github.com/scikit-hep/
