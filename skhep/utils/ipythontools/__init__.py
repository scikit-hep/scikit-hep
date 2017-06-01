# Licensed under a 3-clause BSD style license, see LICENSE.
"""
IPython Tools
=============
The IPython tools gives you a set of reoccuring tools to solve typical problems when using your software project with
jupyter notebooks. It is built to seamlessly interact with your software framework and give you all the functionality
you want to have in your everyday jupyter usage, e.g.

* Show calculation information with interactive widgets which is the best method to show your content in jupyter
  notebooks.
* Manage your processes with an easy-to use interface, which is suited for the interactive manner of jupyter notebooks.
* Handle multiple processes and grid searches.

"""

from __future__ import absolute_import
from .ipython_handler import IPythonHandler

#: Create a single instance
handler = IPythonHandler()
