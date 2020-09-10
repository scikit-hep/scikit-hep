#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

import sys
import os

# try to use setuptools if installed
from setuptools import setup, find_packages
from setuputils import read, find_version


# General information on the project
PROJECT_NAME = 'scikit-hep'
AUTHOR = 'the scikit-hep developers'
AUTHOR_EMAIL = 'scikit-hep-admins@googlegroups.com'
DESCRIPTION = 'Metapackage of Scikit-HEP project tools for Particle Physics.'
URL = 'https://github.com/scikit-hep/scikit-hep/'
LICENSE = 'new BSD'
VERSION = find_version('skhep/__init__.py')

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

PYTHON_REQUIRES = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*"

with open(os.path.join(LOCAL_PATH, 'requirements.txt')) as requirements_file:
    INSTALL_REQUIRES = requirements_file.read().splitlines()

TESTS_REQUIRE = [
    'pytest>3.0;python_version>="2.7"'
]

setup(
    name=PROJECT_NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.rst'),
    url=URL,
    license=LICENSE,
    packages=find_packages(),
    py_modules=['setuputils'],
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    tests_require=TESTS_REQUIRE,
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'License :: OSI Approved',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: C++',
        'Programming Language :: Cython',
        'Development Status :: 4 - Beta',
    ]
)
