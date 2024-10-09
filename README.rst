
``scikit-hep``: metapackage for Scikit-HEP
==========================================

.. image:: https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
   :target: https://scikit-hep.org

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/Scikit-HEP/community

.. image:: https://img.shields.io/pypi/v/scikit-hep.svg
  :target: https://pypi.python.org/pypi/scikit-hep

.. image:: https://img.shields.io/conda/vn/conda-forge/scikit-hep.svg
  :target: https://github.com/conda-forge/scikit-hep-feedstock

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1043949.svg
  :target: https://doi.org/10.5281/zenodo.1043949

.. image:: https://github.com/scikit-hep/scikit-hep/workflows/CI/badge.svg
   :target: https://github.com/scikit-hep/scikit-hep/actions?query=workflow%3ACI+branch%3Amain

.. image:: https://codecov.io/gh/scikit-hep/scikit-hep/graph/badge.svg?branch=main
   :target: https://codecov.io/gh/scikit-hep/scikit-hep?branch=main

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
`get in touch <https://scikit-hep.org/getting-in-touch.html>`_
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

Please check the ``setup.cfg`` and ``requirements.txt`` files for the list
of Python versions supported and the list of Scikit-HEP project packages
and dependencies included, respectively.

For any installed ``scikit-hep`` the following displays the actual versions
of all Scikit-HEP dependent packages installed, for example:

.. code-block:: python

    >>> import skhep
    >>> skhep.show_versions()

    System:
        python: 3.10.10 | packaged by conda-forge | (main, Mar 24 2023, 20:08:06) [GCC 11.3.0]
    executable: /srv/conda/envs/notebook/bin/python
       machine: Linux-5.15.0-72-generic-x86_64-with-glibc2.27

    Python dependencies:
           pip: 23.1.2
         numpy: 1.24.3
         scipy: 1.10.1
        pandas: 2.0.2
    matplotlib: 3.7.1

    Scikit-HEP package version and dependencies:
            awkward: 2.2.2
    boost_histogram: 1.3.2
      decaylanguage: 0.15.3
           hepstats: 0.6.1
           hepunits: 2.3.2
               hist: 2.6.3
         histoprint: 2.4.0
            iminuit: 2.21.3
             mplhep: 0.3.28
           particle: 0.22.0
              pylhe: 0.6.0
           resample: 1.6.0
              skhep: 2023.06.09
             uproot: 5.0.8
             vector: 1.0.0

**Note on the versioning system:**

This package uses `Calendar Versioning <https://calver.org/>`_ (CalVer).
