
``scikit-hep``: metapackage for Scikit-HEP
==========================================

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
   :target: https://scikit-hep.org

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/Scikit-HEP/community

.. image:: https://img.shields.io/pypi/v/scikit-hep.svg
  :target: https://pypi.python.org/pypi/scikit-hep

.. image:: https://img.shields.io/conda/vn/conda-forge/scikit-hep.svg
  :target: https://anaconda.org/conda-forge/scikit-hep

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1043949.svg
  :target: https://doi.org/10.5281/zenodo.1043949

.. image:: https://github.com/scikit-hep/scikit-hep/workflows/CI/badge.svg
   :target: https://github.com/scikit-hep/scikit-hep/actions?query=workflow%3ACI+branch%3Amaster

.. image:: https://coveralls.io/repos/github/scikit-hep/scikit-hep/badge.svg?branch=master
   :target: https://coveralls.io/github/scikit-hep/scikit-hep?branch=master


Project info
------------

The `Scikit-HEP project <http://scikit-hep.org/>`_ is a community-driven and community-oriented project
with the aim of providing Particle Physics at large with an ecosystem for data analysis in Python
embracing all major topics involved in a physicist's work.
The project started in Autumn 2016 and its packages are actively developed and maintained.

It is not just about providing core and common tools for the community.
It is also about improving the interoperability between HEP tools and the Big Data scientific ecosystem in Python,
and about improving on discoverability of utility packages and projects.

For what concerns the project grand structure, it should be seen as a *toolset* rather than a toolkit.

**Getting in touch**

There are various ways to
`get in touch <http://scikit-hep.org/get-in-touch.html>`_
with project admins and/or users and developers.

scikit-hep package
------------------

``scikit-hep`` is a metapackage for the Scikit-HEP project.

Installation
.............

You can install this metapackage from PyPI with `pip`:

.. code-block:: bash

   python -m pip install scikit-hep

or you can use Conda through conda-forge:

.. code-block:: bash

   conda install -c conda-forge scikit-hep

All the normal best-practices for Python apply; you should be in a virtual environment, etc.

Package version and dependencies
................................

Please check the ``setup.py`` and ``requirements.txt`` files for the list
of Python versions supported and the list of Scikit-HEP project packages
and dependencies included, respectively.

For any installed `scikit-hep` the following displays the actual versions
of all Scikit-HEP dependent packages installed, for example:

.. code-block:: python

    >>> import skhep
    >>> skhep.show_versions()

    System:
        python: 3.8.6 (default, Sep 24 2020, 21:45:12)  [GCC 8.3.0]
    executable: /usr/local/bin/python
       machine: Linux-4.19.104-microsoft-standard-x86_64-with-glibc2.2.5

    Python dependencies:
           pip: 21.0.1
    setuptools: 54.1.2
         numpy: 1.20.1
         scipy: 1.6.1
        pandas: 1.2.3
    matplotlib: 3.3.4

    Scikit-HEP package version and dependencies:
           awkward0: 0.15.5
            awkward: 1.1.2
    boost_histogram: 1.0.0
      decaylanguage: 0.10.2
           hepstats: 0.3.1
           hepunits: 2.1.0
               hist: 2.2.0
         histoprint: 2.0.0
            iminuit: 2.4.0+ROOT-v6-23-01-RF-binSampling-685-ga642cc22e3
             mplhep: 0.2.17
           particle: 0.14.0
              skhep: 3.0.0
    uproot3_methods: 0.10.0
            uproot3: 3.14.4
             uproot: 4.0.6

**Note on the versioning system:**

- A version ```scikit-hep x.y`` is compatible with the releases of all package dependents
  versions ```a.b.c`` for all ``c``.
- Major version updates are prepared every time (at least) a "package component" does the same.
- Typical updates go with a minor version, so when (at least) a package goes from version ``a.b`` to ```x.(y+1)``.
- Patch version updates are only done if there is some reason on the side of the metapackage itself.
