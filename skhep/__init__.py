# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
A community-driven and oriented Python software project for High Energy Physics.
"""

from __future__ import absolute_import

from .utils._show_versions import show_versions

from ._version import __version__


__all__ = [
    "banner",
    "project_url",
    "project_url_GitHub",
    "project_url_PyPI" "show_versions",
    "__version__",
]


# -----------------------------------------------------------------------------
# Project and package info
# -----------------------------------------------------------------------------

project_url = "http://scikit-hep.org"
project_url_GitHub = "https://github.com/scikit-hep/scikit-hep"
project_url_PyPI = "https://pypi.python.org/pypi/scikit-hep"

__doc__ = __doc__.format(__version__)

banner = __doc__
