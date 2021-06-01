# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Utility methods to print system info and org packages info, for debugging.

Heavily inspired from :func:`sklearn.show_versions`.
"""

import platform
import sys
import importlib


scipy_deps = ["pip", "setuptools", "numpy", "scipy", "pandas", "matplotlib"]


skhep_deps = [
    "awkward0",
    "awkward",
    "boost_histogram",
    "decaylanguage",
    "hepstats",
    "hepunits",
    "hist",
    "histoprint",
    "iminuit",
    "mplhep",
    "particle",
    "skhep",
    "uproot",
    "uproot3",
    "uproot3_methods",
    "vector",
]


def _get_sys_info():
    """
    Get system information.

    Return
    ------
    sys_info : dict
        System and Python version information.
    """
    python = sys.version.replace("\n", " ")

    blob = [
        ("python", python),
        ("executable", sys.executable),
        ("machine", platform.platform()),
    ]

    return dict(blob)


def _get_deps_info(pkgs_list):
    """
    Get the installed versions of a list of packages.

    Returns
    -------
    deps_info: dict
        Version information on the input list of libraries.

    """
    deps_info = {}

    for modname in pkgs_list:
        try:
            if modname in sys.modules:
                mod = sys.modules[modname]
            else:
                mod = importlib.import_module(modname)
            ver = mod.__version__
            deps_info[modname] = ver
        except ImportError:
            deps_info[modname] = None

    return deps_info


def show_versions():
    """
    Overview of the installed versions of main dependencies on the
    Python scientific ecosystem packages and on the Scikit-HEP packages.
    """

    sys_info = _get_sys_info()
    deps_info = _get_deps_info(scipy_deps)
    skhep_deps_info = _get_deps_info(skhep_deps)

    print("\nSystem:")
    for k, stat in sys_info.items():
        print("{k:>10}: {stat}".format(k=k, stat=stat))

    print("\nPython dependencies:")
    for k, stat in deps_info.items():
        print("{k:>10}: {stat}".format(k=k, stat=stat))

    print("\nScikit-HEP package version and dependencies:")
    for k, stat in skhep_deps_info.items():
        print("{k:>15}: {stat}".format(k=k, stat=stat))
