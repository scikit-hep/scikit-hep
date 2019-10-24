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
DESCRIPTION = 'Toolset of interfaces and tools for Particle Physics.'
URL = 'https://github.com/scikit-hep/scikit-hep/'
LICENSE = 'new BSD'
VERSION = find_version('skhep/__init__.py')

# Prevent setup from trying to create hard links
# which are not allowed on AFS between directories.
# This is a hack to force copying.
try:
    del os.link
except AttributeError:
    pass

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
# setup.py can be called from outside the scikit-hep directory
os.chdir(LOCAL_PATH)
sys.path.insert(0, LOCAL_PATH)

PYTHON_REQUIRES = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"

with open(os.path.join(LOCAL_PATH, 'requirements.txt')) as requirements_file:
    INSTALL_REQUIRES = requirements_file.read().splitlines()

TESTS_REQUIRE = [
    'pytest>3.0;python_version>="2.7"'
]

SETUP_REQUIRES = [
    'pytest-runner'
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
    setup_requires=SETUP_REQUIRES,
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: C++',
        'Programming Language :: Cython',
        'Development Status :: 4 - Beta',
    ]
)
