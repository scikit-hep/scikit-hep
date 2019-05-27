
Scikit-HEP
==========

.. image:: https://img.shields.io/pypi/v/scikit-hep.svg
  :alt: PyPI
  :target: https://pypi.python.org/pypi/scikit-hep

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1043949.svg
  :target: https://doi.org/10.5281/zenodo.1043949

Project info
------------

The Scikit-HEP project (http://scikit-hep.org/) is a community-driven and community-oriented project
with the aim of providing Particle Physics at large with a Python package containing core and common tools.

The project started in Autumn 2016 and its packages are actively developed and maintained.

This scikit-hep package is under redesign, in order to become a metapackage for the project.

Python versions supported:

.. image:: https://img.shields.io/badge/python-2.7-blue.svg
   :target: https://badge.fury.io/py/scikit-hep

.. image:: https://img.shields.io/badge/python-3.4-blue.svg
   :target: https://badge.fury.io/py/scikit-hep

.. image:: https://img.shields.io/badge/python-3.5-blue.svg
   :target: https://badge.fury.io/py/scikit-hep

.. image:: https://img.shields.io/badge/python-3.6-blue.svg
   :target: https://badge.fury.io/py/scikit-hep

Project status
--------------

.. image:: https://travis-ci.org/scikit-hep/scikit-hep.svg
   :target: https://travis-ci.org/scikit-hep/scikit-hep

.. image:: https://coveralls.io/repos/github/scikit-hep/scikit-hep/badge.svg?branch=master
   :target: https://coveralls.io/github/scikit-hep/scikit-hep?branch=master


   Installation
   ------------

   Install ``scikit-hep`` like any other Python package:

   .. code-block:: bash

       pip install scikit-hep

   or similar (use ``--user``, ``virtualenv``, etc. if you wish).


Strict dependencies
-------------------

+------------------------+----------+----------+
| **Python**             | 2.7      | 3.x      |
+========================+==========+==========+
+------------------------+---------------------+
| **NumPy**              | >= 1.11.0           |
+------------------------+---------------------+
| **matplotlib**         | > 2.0.0 , < 2.1     |
+------------------------+---------------------+
| **pandas**             | no requirement      |
+------------------------+---------------------+


Documentation
-------------

The documentation is hosted on the `Scikit-HEP website`_, and the source code
is in the ``doc/`` folder. `Sphinx`_ is required for building the HTML pages.
Also `Pandoc`_ is needed so that the Jupyter notebooks providing numerous examples
are nicely embedded in the documentation. The documentation is built with the command:

 .. code-block:: bash

     $ make -C doc html

.. _Scikit-HEP website: http://scikit-hep.org/
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _Pandoc : http://pandoc.org/


Getting in touch
----------------
Mailing list to ping all admins at once: `scikit-hep-admins`_.

Forum for general matters, announcements and discussions concerning the Scikit-HEP project : `scikit-hep-forum`_.

.. _scikit-hep-admins: scikit-hep-admins@googlegroups.com
.. _scikit-hep-forum: scikit-hep-forum@googlegroups.com
