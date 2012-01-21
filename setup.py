#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
import os.path as p

VERSION = open(p.join(p.dirname(p.abspath(__file__)), 'VERSION')).read().strip()

setup(
    name='relations',
    version=VERSION,
    description='A simple relational algebra engine in Python.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/relations',
    packages=find_packages(where='lib'),
    package_dir={'': 'lib'},
    install_requires=[
        'urecord>=0.0.4',
    ],
)
