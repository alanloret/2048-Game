#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:05:18 2019

@author: alanloret
"""

from datetime import timedelta
from game import jeu2048
import time

if __name__ == '__main__':

    t1 = time.time()
    res = jeu2048().simulation()
    t2 = time.time()
    print(f"Durée de la partie: {str(timedelta(seconds=int(t2 - t1))):8>0}\n")
