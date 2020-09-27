# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:12:39 2020

@author: alanloret
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    name='game',
    ext_modules=cythonize("game.pyx"),
)
