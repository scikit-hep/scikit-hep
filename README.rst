.. image:: https://zenodo.org/badge/73710584.svg
   :target: https://zenodo.org/badge/latestdoi/73710584

==========
Scikit-HEP
==========

The Scikit-HEP project (http://scikit-hep.org/) is a community-driven and community-oriented project
with the aim of providing Particle Physics at large with a Python package containing core and common tools.

Project info
------------

The project started in Autumn 2016 and its core is actively being defined.

The project and releases are `registered on PyPI <http://pypi.python.org/pypi/scikit-hep>`_.

.. image:: https://badge.fury.io/py/scikit-hep.svg
    :target: https://badge.fury.io/py/scikit-hep

The development is occurring at the
`project's GitHub page <http://github.com/scikit-hep/scikit-hep>`_.

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

License
-------
The scikit-hep project is licensed under a 3-clause BSD style license - see the
``LICENSE`` file.
