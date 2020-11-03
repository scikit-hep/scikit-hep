
``scikit-hep``: metapackage for Scikit-HEP
==========================================

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
   :target: https://scikit-hep.org

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/Scikit-HEP/community

.. image:: https://img.shields.io/pypi/v/scikit-hep.svg
  :target: https://pypi.python.org/pypi/scikit-hep

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
It is also about improving the interoperability between HEP tools and the scientific ecosystem in Python,
and about improving on discoverability of utility packages and projects.

For what concerns the project grand structure, it should be seen as a *toolset* rather than a toolkit.

**Getting in touch**

There are various ways to
`get in touch <http://scikit-hep.org/get-in-touch.html>`_
with project admins and/or users and developers.

scikit-hep package
------------------

This ``scikit-hep package`` is under redesign, in order to become a metapackage for the project.

Installation
.............

Install ``scikit-hep`` like any other Python package:

.. code-block:: bash

   python -m pip install scikit-hep

or similar (use ``venv``, etc. if you wish).

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
           pip: 20.2.4
    setuptools: 50.3.2
         numpy: 1.19.2
         scipy: 1.5.3
        pandas: 1.1.3
    matplotlib: 3.3.2

    Scikit-HEP package version and dependencies:
            awkward: 0.13.0
    boost_histogram: 0.11.0
      decaylanguage: 0.8.0
           hepstats: 0.3.0
           hepunits: 2.0.0
               hist: 2.0.1
         histoprint: 1.5.2
            iminuit: 1.5.2
             mplhep: 0.2.2
           particle: 0.12.0
              skhep: 1.1.0
     uproot_methods: 0.7.4
             uproot: 3.12.0
