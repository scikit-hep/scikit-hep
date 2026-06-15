# Licensed under a 3-clause BSD style license, see LICENSE.
"""
Utility methods to print system info and org packages info, for debugging.

Heavily inspired from :func:`sklearn.show_versions`.
"""

import importlib.metadata
import platform
import sys


scipy_deps = ["setuptools", "pip", "numpy", "scipy", "pandas", "matplotlib"]


skhep_deps = [
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
    "pylhe",
    "resample",
    "scikit-hep",
    "uproot",
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

    return {
        "python": python,
        "executable": sys.executable,
        "machine": platform.platform(),
    }


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
            deps_info[modname] = importlib.metadata.version(modname)
        except importlib.metadata.PackageNotFoundError:
            deps_info[modname] = None

    return deps_info


def _print_section(title, info, width):
    print(f"\n{title}:")
    for k, stat in info.items():
        print(f"{k:>{width}}: {stat}")


def show_versions():
    """
    Overview of the installed versions of main dependencies on the
    Python scientific ecosystem packages and on the Scikit-HEP packages.
    """

    sys_info = _get_sys_info()
    deps_info = _get_deps_info(scipy_deps)
    skhep_deps_info = _get_deps_info(skhep_deps)

    _print_section("System", sys_info, 10)
    _print_section("Python dependencies", deps_info, 10)
    _print_section("Scikit-HEP package version and dependencies", skhep_deps_info, 15)
