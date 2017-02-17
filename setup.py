#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
import sys
import os

# try to use setuptools if installed
from setuptools import setup, find_packages
from setuputils import read, find_version


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

setup(
    name='scikit-hep',
    version=find_version('skhep/__init__.py'),
    description='Particle Physics python package',
    long_description=read('README.rst'),
    license='new BSD',
    packages=find_packages(exclude=['tests']),
    test_suite="tests",
    py_modules=['setuputils'],
    install_requires=[
        'PyPDT>=0.7.0'
    ],
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
        'Programming Language :: C++',
        'Programming Language :: Cython',
        'Development Status :: 1 - Planning',
    ]
)
