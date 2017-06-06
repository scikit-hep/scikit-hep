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
  | Student: Deepanshu Thakur. |Miscellaneous_ongoing|

* | `Visualization tools for Scikit-HEP <http://hepsoftwarefoundation.org/gsoc/proposal_ScikitHEPviz.html>`_.
  | Student: Chetan Malhotra. |Visualization_ongoing|


Simulation
----------

* Creation of a decay generator base class. A concrete class using ROOT's
  ``TGenPhaseSpace`` should be an immediate example.
  Contact `Eduardo` if you want to get involved. |Simulation_ongoing|


ROOT-Pandas
-----------

* Include the `root_pandas <https://github.com/ibab/root_pandas>`_ project into scikit-hep and see how it fits together with the rest of the framework. It is an excellent candidate for an affiliated package.
* Define which parts are still missing and find developers for this part of the project.
* See if users of this project may want to use scikit-hep as their starting point instead of installing `root_pandas`, to increase the awareness of this project. |AffiliatedPackages_open|


Analysis Development
--------------------

* Give users as early as possible an idea on how the project may contribute to and/or help with their analysis, 
  e.g. by giving a small example analysis using the project toolchain.
* Think about including "framework" tools for an analysis, e.g. workflow managers (for example luigi).


.. |AffiliatedPackages_open| image:: images/AffiliatedPackages-open-orange.png
.. |Miscellaneous_open| image:: images/Miscellaneous-open-orange.png
.. |Miscellaneous_ongoing| image:: images/Miscellaneous-ongoing-yellowgreen.png
.. |Simulation_ongoing| image:: images/Simulation-ongoing-yellowgreen.png
.. |Visualization_open| image:: images/Visualization-open-orange.png
.. |Visualization_ongoing| image:: images/Visualization-ongoing-yellowgreen.png

