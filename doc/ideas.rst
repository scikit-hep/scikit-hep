.. _ideas:

Forum on project ideas
======================

This page collects project ideas coming from either the Scikit-HEP team
or more broadly from anyone from the Scikit-HEP community.
Do get in touch if you would like to add an idea to this forum.
It will be the best way to raise awareness about your idea and
attract contributors!

Google Summer of Code 2017
--------------------------

Scikit-HEP is participating in the
`Google Summer of Code 2017 <https://developers.google.com/open-source/gsoc/>`_
program with CERN as an organization, and under the umbrella of the
`HEP Software Foundation <http://hepsoftwarefoundation.org/>`_,
see the direct `link <http://hepsoftwarefoundation.org/activities/gsoc.html>`_.

We have put forward
`2 successful proposals <http://hepsoftwarefoundation.org/gsoc/project_SciKit-HEP.html>`_!
The direct links to the project proposals are the following:

* | `Python bindings for the Hydra C++ library for analysis on massively multi-threaded platforms <http://hepsoftwarefoundation.org/gsoc/proposal_ScikitHEP.html>`_.
  | Student: Deepanshu Thakur. |Miscellaneous_done|

* | `Visualization tools for Scikit-HEP <http://hepsoftwarefoundation.org/gsoc/proposal_ScikitHEPviz.html>`_. |Visualization_open|


Data aggregation
----------------
* Data aggregation largely means histogramming. An interesting idea would be to exploit
  the `Histogrammar <http://histogrammar.org/>`_ package implementation in Python
  as a powerful way of dealing with data aggregation in Scikit-HEP. |Aggregations_open|


Datasets
--------
* Datasets are central in HEP and Scikit-HEP too. This important package needs further development and lack parts of the implementation.
  Get in touch with `Jim` and `Eduardo` if the topic is of interest to you. |Datasets_open|


Math modules
------------
* The 3D and Lorentz vector classes need to be improved to exploit NumPy arrays.
  There is also functionality to be implemented.
  | Contact `Eduardo` if such a development is of interest to you. |Math_ongoing|

* Now that 3D and Lorentz vector classes are available, though in development, it would be handy to build on them.
  Needed are a 3D point class and then a set of mathematical functions implementing handy geometry-related calculations commonly used in HEP.
  Contact `Vanya` and `Eduardo` if such a development is of interest to you. |Math_ongoing|


Modeling
--------
Means "data models and fitting utilities" at large. |Modeling_open|
Ideas?


Simulation
----------

* Creation of a decay generator base class. A concrete class using ROOT's
  ``TGenPhaseSpace`` should be an immediate example.
  Contact `Eduardo` if you want to get involved. |Simulation_ongoing|


ROOT-Pandas
-----------

* Include the `root_pandas <https://github.com/ibab/root_pandas>`_ project into Scikit-HEP and see how it fits together with the rest of the framework.
  It is an excellent candidate for an affiliated package. |AffiliatedPackages_done|
* Define which parts are still missing and find developers for this part of the project. |AffiliatedPackages_ongoing|
* See if users of this project may want to use scikit-hep as their starting point instead of installing `root_pandas`, to increase the awareness of this project. |AffiliatedPackages_ongoing|


Analysis Development
--------------------

* Give users as early as possible an idea on how the project may contribute to and/or help with their analysis,
  e.g. by giving a small example analysis using the project toolchain.
* Think about including "framework" tools for an analysis, e.g. workflow managers (for example luigi).

Continuous integration, testing, code health, etc.
--------------------------------------------------

* Add CI on Windows for as long as possible - nice since a totally different plaform compared to Linux. |Miscellaneous_open|
* How do `coveralls.io <https://coveralls.io>`_ and `codecov.io <https://codecov.io>`_ compare? Worth having both? That would mean adding codecov.
* Look at `landscape.io <https://landscape.io>`_ and decide if worth having CI runs there.


.. |AffiliatedPackages_open| image:: images/AffiliatedPackages-open-orange.png
.. |AffiliatedPackages_ongoing| image:: images/AffiliatedPackages-ongoing-yellowgreen.png
.. |AffiliatedPackages_done| image:: images/AffiliatedPackages-done-lightgrey.png
.. |Aggregations_open| image:: images/Aggregations-open-orange.png
.. |Datasets_open| image:: images/Datasets-open-orange.png
.. |Math_open| image:: images/Math-open-orange.png
.. |Math_ongoing| image:: images/Math-ongoing-yellowgreen.png
.. |Miscellaneous_open| image:: images/Miscellaneous-open-orange.png
.. |Miscellaneous_ongoing| image:: images/Miscellaneous-ongoing-yellowgreen.png
.. |Miscellaneous_done| image:: images/Miscellaneous-done-lightgrey.png
.. |Modeling_open| image:: images/Modeling-open-orange.png
.. |Simulation_ongoing| image:: images/Simulation-ongoing-yellowgreen.png
.. |Visualization_open| image:: images/Visualization-open-orange.png
.. |Visualization_ongoing| image:: images/Visualization-ongoing-yellowgreen.png
