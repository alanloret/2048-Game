#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:52:53 2019

@author: alanloret
"""

from fonctions_jeu_2048 import jeu2048
import unittest


class Test(unittest.TestCase):
    
    """On test si les mouvements qu'on effectue sont bien conformes aux règles
           du jeu et qu'on lève une erreur lorsque la direction n'existe pas
           Cela pour les 4 directions """
    
    def test_case_vide(self):
        """ On teste la fonction actualise qui un 2 ou un 4 à la grille, 
        ce qui permet aussi de tester le bon fonctionnement de la fonction 
        case_vide qui actualise la liste des cases vides """
        
        grille = jeu2048()
        grille.matrice = [[2,2,0,0],
                          [2,0,2,0],
                          [2,0,0,2],
                          [0,2,8,0]]
        
        correction = len(grille.case_vide()) 
        
        grille.actualise()
        #On a complété une case vide de la grille donc on en a 8-1 = 7
        self.assertEqual(len(grille.case_vide()),correction -1)
        self.assertEqual(7,correction -1)
    
    
    def test_mouvement_gauche(self):
        grille = jeu2048()
        grille.matrice = [[2,2,2,0],
                          [2,0,2,0],
                          [2,0,2,2],
                          [0,2,8,0]]
        
        grille.coup_suivant("gauche")
        
        correction = [[4,2,0,0],
                      [4,0,0,0],
                      [4,2,0,0],
                      [2,8,0,0]]
        self.assertEqual(grille.matrice,correction)
        
        #On test si une autre chaine de caractère  renvoie bien une erreur
        with self.assertRaises(ValueError):
            grille.coup_suivant("bhtbh")
    
            
    def test_mouvement_droite(self):
        grille = jeu2048()
        grille.matrice = [[2,2,0,0],
                          [2,0,2,0],
                          [8,0,0,2],
                          [2,2,2,2]]
        grille.coup_suivant("droite")
        
        correction = [[0,0,0,4],
                      [0,0,0,4],
                      [0,0,8,2],
                      [0,0,4,4]]
        self.assertEqual(grille.matrice,correction)
        
            
    def test_mouvement_haut(self):
        grille = jeu2048()
        grille.matrice = [[2,2,0,0],
                          [4,0,2,0],
                          [2,0,0,2],
                          [2,2,2,0]]
        grille.coup_suivant("haut")
        
        correction = [[2,4,4,2],
                      [4,0,0,0],
                      [4,0,0,0],
                      [0,0,0,0]]
        self.assertEqual(grille.matrice,correction)
        
        
    def test_mouvement_bas(self):
        grille = jeu2048()
        grille.matrice = [[2,2,0,0],
                          [4,0,2,0],
                          [2,0,0,2],
                          [2,2,2,0]]
        grille.coup_suivant("bas")
        
        correction = [[0,0,0,0],
                      [2,0,0,0],
                      [4,0,0,0],
                      [4,4,4,2]]
        self.assertEqual(grille.matrice,correction)
        
            
    def test_fin_jeu(self):
        """ Test de la fonction fin_jeu qui indique les coups possibles
        qui modifient la grille """
        
        grille = jeu2048()
        grille.matrice = [[8,2,0,0],
                          [4,4,0,0],
                          [8,2,0,0],
                          [2,0,0,0]]
        
        self.assertEqual(set(grille.fin_jeu()),set(['droite', 'gauche', 'bas']))
        
        grille.matrice = [[8,2,8,2],
                          [16,64,4,32],
                          [4,2,16,4],
                          [2,8,4,2]]
        
        self.assertEqual(set(grille.fin_jeu()),set([]))
        
        
    def test_score(self):
        """ On teste le bon fonctionnement de coup_suivant en tant qu'elle
            actualise bien le score de la grille """
            
        grille = jeu2048()
        grille.matrice = [[8,2,0,0],
                          [8,2,0,0],
                          [4,2,0,0],
                          [2,0,0,0]]
        grille.coup_suivant("haut")
        
        #On forme un 16 et un 4 donc on gagne 16+4 = 20 points
        self.assertEqual(grille.score,20)


"""On teste nos fonctions"""
unittest.main()
