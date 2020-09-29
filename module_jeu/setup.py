# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:12:39 2020

@author: alanloret
"""

from setuptools import setup
from Cython.Build import cythonize

""" Nous avons utilisé le module Cython :
    Pour créer ou enregistrer les modifications de notre module 'game' au sein de notre dossier'module_jeu',
    il faut compiler dans le terminale la commande suivante : 'python3 setup.py build_ext -- inplace'
    (si vous êtes toujours sous python v2 mettez : 'python setup.py build_ext -- inplace').
    
    Note : les fichiers 'game.c' et 'game.cpython-38-darwin.so' ainsi que que le dossier 'build' sont 
    créés automatiquement par la commande du terminale pour construire le module 'game'."""


setup(
    name='game',
    ext_modules=cythonize("game.pyx"),
)
