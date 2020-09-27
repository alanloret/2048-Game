#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:35:20 2019

@author: alanloret
"""

from setup import jeu
import time
from datetime import timedelta
import matplotlib.pyplot as plt

""" Notre algorithme suit la méthode de Monte-Carlo
    Il évalue tous les coups qu'on souhaite tester en faisant plusieurs parties
    aléatoires en partant de la grille donnée et on retient le coup qui engendre 
    les meilleurs résultats en moyenne
    
    L'algorithme est donc très lent même si nous avons bien optimisé les fonctions :
     -> si l'on effectue aléatoirement les parties jusqu'à la défaite on a pour 
        200 parties aléatoires : 90% du temps un 2048 et 25% du temps un 4096
        (si l'on augmente encore le nombre de partie aléatoire on ne gagne pas plus souvent
        et la durée d'une partie est de 11min)
     
     -> mais si l'on limite le nombre de coups à 20 pour chaque partie aléatoire et qu'on
        en fait que 100 : 85% du temps un 2048 et 15% du temps un 4096 
        (la durée d'attente dans ce cas est de 5min en moyenne)
     
     -> si l'on diminue encore le nombre de coups ou le nombre de partie aléatoire 
        on perd nettement en performance      
    
    -> si vous voulez tester notre code : le fichier __main__ affiche une simulation coup par coup
       ou bien diminuez le nombre de partie à 10 au lieu de 100 dans la fonction  
       module_jeu/fonctions_jeu_2048/direction_Optimale -> ligne 320
        
    Pour avoir de meilleurs résultats il faudrait combiner notre algorithme en modifiant 
    le score des grilles aussi en fonction de la disposition des cases, comme nous le faisons
    quand on joue au jeu 2048 """
    

resultat = []
nbr_partie = 1


for i in range(nbr_partie):
    print("#", i+1)
    t1 = time.time()
    resultat += jeu()
    t2 = time.time()
    print(f"Durée de la partie: {str(timedelta(seconds=t2 - t1)):8>0}\n")

resultat.sort()
Liste = list()
for i in range(len(resultat)):
    Liste += [i]*resultat[i]
plt.hist(Liste)
plt.show()
