.. _faq:

FAQ
===

What is the exact project name?
-------------------------------
The project is called `Scikit-HEP`. Notice the upper-case "S" and "HEP".
That is distinct from the core package, which is `scikit-hep`.

How to pronounce the project name?
----------------------------------
Like "sy-kit happ"(y), forgetting about the "y" in "happy".
Of course "sci" stands for science.

How to get started contributing?
--------------------------------
Please refer to the link :ref:`contributing to Scikit-HEP <contributing>`
for details on how to get involved.

Is there support for PyPy?
--------------------------
It's a nice idea. Support for `PyPy <http://pypy.org/>`_ could be envisaged in the near future
`but only once` the scientific stack based on `NumPy <http://www.numpy.org/>`_ supports it.

Is there support for GPUs?
--------------------------
Support for GPU-oriented code is not foreseen in the core package `scikit-hep` itself in the near- or even medium-term future.
This would introduce non-trivial dependencies.
This being said, there are already ideas to bring along :ref:`affiliated packages <affiliations>` specifically targetting data-intensive work,
so code running on both CPUs and GPUs.
