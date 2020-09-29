#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:35:20 2019

@author: alanloret
"""

from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import time

from game import jeu2048

""" Notre algorithme suit la méthode de Monte-Carlo.
    Il évalue tous les coups possibles en faisant plusieurs parties aléatoires en partant de 
    la grille donnée. Nous effectuons ensuite le coup qui engendre les meilleurs scores en moyenne.
    
    L'algorithme est donc assez lent même si nous avons bien optimisé les fonctions et utilisé Cython :
     -> * si on effectue aléatoirement les parties jusqu'à la défaite on a pour 200 parties aléatoires : 
        90% du temps un 2048 et 25% du temps un 4096 pour en moyenne des parties de 2min 30s (si on 
        augmente encore le nombre de partie aléatoire on ne gagne pas significativement plus souvent).
        * si on limite le nombre de coups à 20 pour chaque partie aléatoire on a pour 100 parties aléatoires : 
        85% du temps un 2048 et 15% du temps un 4096, la durée d'attente dans ce cas est de 40s en moyenne.
        * si on diminue encore le nombre de coups ou le nombre de partie aléatoire 
        on perd nettement en performance.      
    
    -> si vous voulez tester notre code : le fichier __main__ affiche une simulation coup par coup
       ou bien lancez le fichier evaluation strategie.py.
       
    Note : Vous pouvez modifier le nombre de partie aléatoire dans la fonction direction_Optimale de ce 
    fichier à la ligne 327.
        
    Pour avoir de meilleurs résultats, il faudrait prendre en compte la disposition des cases dans la grille 
    qui est très importante lorsqu'on commence à avoir des scores importants. Pour ce faire on pourrait 
    pénaliser des coups qui entrainent des dispositions très mauvaises ou bien utiliser un réseau de neurones."""


resultat = []
nbr_partie = 5

for i in range(nbr_partie):
    t1 = time.time()
    resultat.append(jeu2048().partie())
    t2 = time.time()
    print(f"#{i+1}\nDurée de la partie: {str(timedelta(seconds=int(t2 - t1))):8>0}\n")

resultat.sort()
plt.step(resultat, np.linspace(0, 1, len(resultat)))
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.xlabel('Score')
plt.title('Fonction de répartition des scores')
plt.show()
