#!/usr/bin/env python
# Licensed under a 3-clause BSD style license, see LICENSE.

import os

from setuptools import setup

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(LOCAL_PATH, 'requirements.txt')) as requirements_file:
    INSTALL_REQUIRES = requirements_file.read().splitlines()

setup(
    install_requires=INSTALL_REQUIRES,
)
