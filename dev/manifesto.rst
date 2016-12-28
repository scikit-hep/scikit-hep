****************************
Scikit-HEP Project Manifesto
****************************

.. NOTE::
   Work in progress Manifesto ! Contains material under active discussion and design.

.. |date| date::
.. |time| date:: %Hh%M

Version as of |date|, |time|.


.. contents:: Table of Contents

The project
===========

The idea, in just one sentence
------------------------------

The Scikit-HEP project (http://scikit-hep.org/) is a community-driven and community-oriented project
with the aim of providing Particle Physics at large with a Python package containing core and common tools.

General info
------------

The project started in Autumn 2016 and is actively being defined.

The project homepage is http://scikit-hep.org/. The (future) releases are `registered on PyPI <http://pypi.python.org/pypi/scikit-hep>`_.
The development is occurring at the `project's GitHub page <http://github.com/scikit-hep/scikit-hep>`_.

The project is licensed under a 3-clause BSD style license.

Core team
---------

Project started with:

* Vanya Belyaev (LHCb)
* Noel Dawe (ATLAS)
* David Lange (CMS, DIANA)
* Sasha Mazurov (LHCb)
* Jim Pivarski (CMS, DIANA)
* Eduardo Rodrigues (DIANA, LHCb)

Package pillars
---------------

* Simulation: wrappers for Monte Carlo engines and other generators of simulated data.
* Datasets: data in various sources, such as ROOT, Numpy/Pandas, databases, wrapped in a common interface.
* Aggregations: e.g. histograms that summarize or project a dataset.
* Modeling: data models and fitting utilities.
* Visualization: interface to graphics engines, from ROOT and Matplotlib to maybe even d3 or plot.ly.

Core requirements
-----------------

* Community effort coordinated by a few people, to be identified in due time (set will grow with the project).
* Provide core and common tools rather than try and do everything.  **JP:** What's needed most is a set of gateways between existing tools to normalize their different choices of conventions and automatically convert data among them. These are the barriers that currently exist and need to be broken down.
* Exploit Astropy's idea of *affiliated packages*.  **JP:** And the Numpy/Scipy ecosystem, which I'm more familiar with than Astropy. Numpy had the advantage of _predating_ the scientific Python world, so they could establish the conventions used everywhere else. We have a situtation in which many tools exist with different conventions. Was that true of Astropy?
* Python package supporting Python 2.6, 2.7 and 3.4.
* Strict requirements for well-documented code, with a test suite.
* Code should be as generic as possible and various backends should be considered, be it for plotting or I/O. Obvious examples are ROOT and matplotlib.  **JP:** And Keras, TensorFlow, Scikit-Learn, PySpark.

Proposal for initial project and package coordination
-----------------------------------------------------

First stab from ER. Feel free to edit ...:

=========================  ==================
Package and/or topic       Name
=========================  ==================
Continuous integration     ~~Jim & Sasha~~ done?
Data aggregation           Jim ~~& Noel~~ (Histogrammar)
Documentation              All
Histogramming              Jim & Noel & Vanya
Scripts                    Eduardo & Vanya
Simulation                 Eduardo & Noel
~~Tuples~~ Datasets        Noel & Vanya
Units & constants          Eduardo
Visualization              Dave & Noel
Outreach                   Eduardo & Jim & ?
=========================  ==================


Packaging
=========

Distribution/deployment
-----------------------

Possibilities to discuss:  **JP:** In order of priority!

1. Standard PIP installation.
2. PIP installation with wrapped ROOT.
3. CVMFS at CERN.
4. CONDA installation/channel.
5. Spack installation.

There are advantages, disadvantages and issues in all cases. Needs discussion in due time.


Documentation and code layout
=============================

Documentation
-------------

The usual delicate point: not much fun, but very important.

Use *reStructuredText* format for all documentation in .py files.

Question (ER): code is documented by construction. Fine.
But where to add usage documentation? Next to the functions, methods,etc.?
Or at the top of the files, in what becomes the __doc__?

One also needs to think about a living and self-generated (?) document such as the one at https://github.com/rootpy/rootpy/tree/master/docs/.

**JP:** Where documentation should go:

* Python doc strings: top of each module, top of each class, top of each method. See [PEP 257](https://www.python.org/dev/peps/pep-0257/) on writing _brief, to the point_ docstrings.
* I'm going to argue that comments are usually not necessary and often misleading, since they get out of date easily. We'll see if docstrings are wrong when reading the generated Sphinx docs, but we'll only see comments if we're actively reading the code. Assertions or assertion plus comment are much better than comments.
* Sphinx documentation on [scikit-hep.org](http://scikit-hep.org). This is where most newcomers will start. Not only should the text here be introductory (unlike the docstrings), but it should also be clear _that_ this is the introduction. I've had the problem of users finding the fine-details documentation before finding the introduction and thinking it didn't have an introduction.
* Complete examples should be presented as [Gists](https://gist.github.com/). If we put complete examples on [scikit-hep.org](http://scikit-hep.org) or in the repository, we'll be expected to keep them up-to-date, and the maintainance cost accretes. Gists have no social expectation of up-to-dateness, with a comments section for users to ~~complain~~ suggest updates. Users can also make their own Gists (most physicists have GitHub accounts) that are discoverable via the same search. See [Histogrammar documentation](http://histogrammar.org/docs/) for how this can work: search buttons for Gists and StackOverflow embedded in our own documentation.
* A StackOverflow tag, and we should subscribe to it to hear user's problems. Gists and StackOverflow are a track toward developing a self-sustaining community. A mailing list like RootTalk leads to constant maintainance by the core group.


Layout
------

We need to agree on common conventions for the code, not just on the meta-language to use.
Is the layout of https://github.com/scikit-hep/scikit-hep/blob/master/skhep/units/__init__.py
and https://github.com/scikit-hep/scikit-hep/blob/master/skhep/units/prefixes.py suitable?


Continuous integration
======================

Clearly another very important aspect of the project, to have it up and running "at all times".

HEP code drags old code so we need to support at least for now Python 2.6, 2.7 and 3.4.


Outreach and tutorials
======================

The way to reach to the community, train and explain. To be discussed and prepared in due time.


Community feedback
==================

We need to make it easy for the community to get in touch, provide feedback, and, of course, contribute.

In the medium term we will need 2 mailing lists, probably:

- One list for communication among developers and active users of Scikit-HEP.
- Maybe another list for getting in touch with the core team in case privacy is needed?

ER: the first use case cries for a Google groups list. As for the second maybe our 
scikit-hep.org site provides already the possibility of a mailing list such as
feedback@scikit-hep.org?


scikit-hep package structure
============================

First proposal from ER. Not complete nor final! Work very much in progress ...

.. raw:: html
   :file: structure.html

A detailed discussion follows below.


Design and discussion of scikit-hep package
===========================================

Miscellaneous
-------------

**licenses/**
  Probably a handy directory to hold not only this package's license but also licenses for anything we decide to ship with it.
  Suggest ``LICENSE.rst`` for the package license and ``LICENSE_<PackageOrModuleName>.rst`` for license of a package/module shipped with scikit-hep.

**ci/**
  We may well need in the near future a place to add scripts and material for continuous integration.

Configuration and requirement files
-----------------------------------

Most software packages we use have (.)XXXrc files, e.g. ROOT, IPython, Emacs, matplotlib.
They are widespread and it is highly likely that scikit-hep will need one.

ER: suggestion to prepare a directory **rc/** for these *run commands* files. Examples are:

* A template file for scikit-hep.
* A default rc file for scikit-hep to make it trivial for the user to know what are the defaults ;-).
* A template file for ROOT, taken from the standard ROOT installation. And similarly for other packages.

ER: do we also want a separate **requirements/** directory to specify installation/package dependencies similarly to what ``rootpy`` does?
Seems reasonable to me.

Documentation
-------------

Subpackage **docs/** for the user guide, the API and command/scripts references.

Place also to add scikit-hep logos, under **logos/**.

Tutorials
---------

Subpackage **tutorials/** for:

* **examples/**: simple self-contained scripts.
* **notebooks/**: for more advanced (per topic) tutorials, nicely prepared as Jupyter notebooks.

Tests
-----

ER: shall these be in a directory *tests/* at the top level, or rather under **skhep/<module>/tests/** or ... ?

In any case we are almost sure to need a subdirectory **data/** to hold data (e.g. ROOT files) for tests.

Scripts
-------

Scripts are extremely handy fo well-defined and simple tasks. They avoid the need to write
code snippets for common tasks.

Example of useful scripts could be:

* Convertion from a backend to another. Possibility is::

   skhep-convert --from file.root --to file.hdf5 --ignore-errors

  (The ``--ignore-errors`` option would be a real option whereas ``--from`` and ``--to`` would be required arguments.)

* Print the basic units  in HEP and defined in the package::

   skhep-print-units

Aggregation and datasets
------------------------

For now separated into 2 different subpackages **skhep/aggregation/** and **skhep/datasets/**.
Unclear whether this separation is needed ... probably.

Datasets should be seen as ntuples in the sense of ROOT.

ER: idea for histograms, maybe too naive/unrealistic/...:
implementation of a base class with the ability to convert among various backends and read/write from the same backends.
The module should have a natural pythonic interface for the representation of histograms
and a straightforward conversion to specific histogram classes in wide-spread packages such as ROOT, etc.

Requirements:

* Core functionality required/expected for/from a histogram, of course.
* Needs to implement ``to()`` and ``from()`` methods.
* Handy methods of checking possible backends, e.g. ``print_backends()``.
* Read and write methods that will be dealt with in the ``io`` module,
  so something like ``write( filename, backend=None )``
  (the backend option is only necessary for backends such as databases storing serialised objects.).

Possible syntax - basic usage and conversions::

   # Basic usage
   from skhep import aggregation

   h = aggregation.Histo(...)    # Histo would be the scikit-hep generic histogram class
   h_root  = h.to( 'ROOT' )

   h = aggregation.ROOTHisto( <THx instance> )
   
   h = aggregation.XxxHisto( <THx instance> )

   # Conversions
   h_skhep = aggregation.Histo(...)
   h_root  = h_skhep.to( 'ROOT' )
   h_TH1D  = h_skhep.to( ROOT.TH1D )
   h_TH1D  = h_skhep.to( 'TH1D' )

These ``.to(...)`` methods would call behind the scenes the relevant modules
``io.root``, ``io.numpy``, etc., implementing the ``read`` and ``write`` methods
of each backend.

Python configurations
---------------------

Subpackage **skhep/config/*** to collect python configuration-related code.
The astropy project, for example, puts here code to deal with affiliated packages.

Units and constants
-------------------

Subpackages **skhep/units/** and **skhep/constants/**.

A first version of the units module is ready. It containts the basic units. Derived units will follow shortly.

The definition of common physical constants will also be added shortly.

Data files
----------

Possible candidates for data files under **skhep/data/**:

* CODATA_<year>.py.
* mass_width_<year>.mcd that is the PDG particle data table (see comment on the PyPDT project under "Affiliated projects").

Exceptions
----------

ER: do we want/need a dedicated suite for exception handling? Most probably.
The exceptions should also take care of non-implemented features.

Obvious place is **skhep/exceptions/**.

External packages
-----------------

Looking around there are various handy packages and modules that make it as external modules, see for example *rootpy*.
They are distributed along to avoid an extra dependency.

We can simply prepare the usecase with a subpackage **skhep/extern/**.

Input/output
------------

Likely to be a very important subpackage, **skhep/io/**, to deal with the I/O from/to the various backends the project will consider.

Logging
-------

Do we want/need extra code for logging purposes? Most probably.

Package logging code can go in **skhep/logger/**.

Mathematics and statistics
--------------------------

ER: need for both **skhep/math/** and **skhep/stats/** directories?

Modeling
--------

A central part of the functionality scikit-hep will offer.
Unclear at this stage whether to collect everything under a single **skhep/modeling/** subpackage
or rather split into **skhep/models/** and  **skhep/fit/** for example.

Simulation
----------

ER: suggest a **skhep/simulation/** rather than **skhep/generators/** as originally suggested, since more general.

General utilities
-----------------

Subpackage **skhep/utils/** as a placeholder for what does not fit elsewhere.

Visualization
-------------

Subpackage **skhep/visualization/** for all matters concerning visualization.
This is far from a little subpackage since the code to develop will have to deal with the various backends we want to consider.


Affiliated packages
===================

More advanced topic to be discussed with lower priority for now.

ER: ideas for affiliated packages:

* hep_ml for reweighting of distributions (https://github.com/arogozhnikov/hep_ml).
* A Python API for Hydra, a C++ header-only library designed for data analysis (https://github.com/MultithreadCorner/Hydra).

ER: note that in some cases it might be useful to promote a package from affiliated to part of the core of scikit-hep.
The package PyPDT (https://pypi.python.org/pypi/PyPDT) seems like a very good candidate here. It would sit for example
as  **skhep/simulation/pdt.py**.


Project planning
================

Towards first public release(s)
-------------------------------

ER suggests to prepare a first public release v0.1 with just the ``units`` and ``constants`` module,
as soon as ready, so likely in early Janauary.
The functionality will clearly be very minimalistic at such a stsge. Still, the release would have several benefits:

* First module(s) implemented and documented.
* Expose the package looks and documentation layout.
* Test the integration in PyPI, namely the preparation of a release
  and the smooth (hopefully) download and installation on a laptop.

Releases v0.x would then be incremental, following new additions.

For these v0.x releases ER would suggest not to go full blast with a Scikit-HEP
universal suite for histograms and tuples, which are central concepts in HEP.
One could aim at releasing the API but using as a temporary Scikit-HEP implementation
the ROOT backend. When moving to the real Scikit-HEP implementation the user
would not have to adapt much code, if any.
Even better, the first version of the histograms and ntuples could exploit the enhanced
ROOT objects as implemented in Ostap.

There are all sorts of variations to the above. The important point is that the v0.x releases are seen as milestones
towards a first release v1.0 to a wider audience. Versions v0.x would serve as examples when presenting the project
to a smaller community and getting feedback; and this during the first months of the development phase.


Expanding the team
------------------

We look forward to contributions from the community at large and need to dress a team with complementary expertise.
This is not for the immediate future, but soon-ish once we reached a conclusion on most of the above.

In fact the presentation of the project at the DIANA topical meeting of February 20th will be a good opportunity to get a feeling for who might be interested in joining the effort ...

In particular we should welcome contacts from:

* The ROOT team.
* All LHC experiments.
* Neutrino experiments, ongoing and planned.
* Dark matter experiments.
* The FCC community.
* The simulation community be it Geant4 or MC generator experts.
* The Belle II experiment.
* The SHiP experiment under design.
