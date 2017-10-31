.. _installation:

Installation
============

Dependencies
------------

The scikit-hep package requires a few packages upon installation.
In striving to keep support for many Python versions in use in HEP, in particular 2.6,
a requirements matrix is needed for specific packages:

+------------------------+-------------------+----------+----------+
| **Python**             | 2.6               | 2.7      | 3.x      |
+========================+===================+==========+==========+
| **PyPDT**              | >= 0.7.4                                |
+------------------------+-------------------+---------------------+
| **NumPy**              | 1.11.0 , <1.12.0  | >= 1.11.0           |
+------------------------+-------------------+---------------------+
| **matplotlib**         | < 1.5             | > 2.0.0 , < 2.1     |
+------------------------+-------------------+---------------------+
| **pandas**             | == 0.16.2         | no requirement      |
+------------------------+-------------------+---------------------+

Basic installation
------------------

The simplest installation is done with just::

    pip install scikit-hep


Testing
-------

The test suite is built atop `pytest <http://docs.pytest.org/>`_ and requires pytest >= 3.0.

After installation, the complete test suite can be run from outside the source directory with the command::

    pytest tests/ -v -r a
