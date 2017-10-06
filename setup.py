#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.
import sys
import os

# try to use setuptools if installed
from setuptools import setup, find_packages
from setuputils import read, find_version


# Specification of minimal versions of required dependencies
PYPDT_MIN_VERSION = '0.7.3'
NUMPY_MIN_VERSION = '1.11.0'

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

install_requires = [
    'PyPDT>={0}'.format(PYPDT_MIN_VERSION),
    'numpy>=1.11.0,<1.12.0;python_version<"2.7"',
    'numpy>={0};python_version>="2.7"'.format(NUMPY_MIN_VERSION),
    'pandas==0.16.2;python_version<"2.7"',
    'pandas;python_version>="2.7"',
    'matplotlib<1.5;python_version<"2.7"',
    'matplotlib>2.0.0,<2.1;python_version>="2.7"',
]

test_requires = [
    'pytest>=3.0'
]

setup_requires = [
    'pytest-runner'
]

setup(
    name='scikit-hep',
    version=find_version('skhep/__init__.py'),
    description='Particle Physics python package',
    long_description=read('README.rst'),
    license='new BSD',
    packages=find_packages(exclude=['tests']),
    package_data={'skhep': ['data/*.*']},
    py_modules=['setuputils'],
    install_requires=install_requires,
    test_requires=test_requires,
    setup_requires=setup_requires,
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: C++',
        'Programming Language :: Cython',
        'Development Status :: 1 - Planning',
    ]
)
