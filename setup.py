#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    entry_points={'console_scripts': ['smart_rm = smart_rm.core:main']},
    name='smart_rm',
    version='0.2',
    author="Alex Alebovich",
    author_email="ximik.87.alex@gmail.com",
    packages=find_packages(),
)
