#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 09 14:40:32 2019

@author: alan Loret, alexandre Taranoff, emma Heyd, lilian Marey, wakil Lassel, benjamin Bransten
"""


import random as rd
import time 
import unittest


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
        
    Pour avoir de meilleurs résultats il faudrait combiner notre algorithme en modifiant 
    le score des grilles aussi en fonction de la disposition des cases, comme nous le faisons
    quand on joue au jeu 2048 """
        

class jeu2048:
    
    
    def __init__(self):
        self.matrice = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        self.score = 0
    
    def __str__(self):
        string = "Le score est de " + str(self.score) + "\n"
        for i in range(4):
            for j in range(3):
                string += str(self.matrice[i][j]) + "|"
            string += str(self.matrice[i][3]) + "\n"
        return string
    
    def copie(self):
        """ Effectue une copie de self dans grille"""
        
        grille = jeu2048()
        for i in range(4):
            for j in range(4):
                grille.matrice[i][j] = self.matrice[i][j]    
        return grille
    
    def case_vide(self):
        """Actualise la liste des cases vides de la grille"""
        
        Liste = []
        for i in range(4):
            for j in range(4):
                if self.matrice[i][j] == 0:
                    Liste.append((i,j))
        return Liste
    
    
    def actualise(self):
        """Actualise la grille en ajoutant un 2 ou 4 aléatoirement dans 
           une case vide de la grille"""
           
        i,j = rd.choice(self.case_vide()) #On en choisit une au hasard
        self.matrice[i][j] = rd.choice([2,2,2,2,2,2,2,4])
        
    
    def decalage_gauche(self):
        """Decale toutes les cases vers la gauche"""
        
        for i in range(4):
            for j in range(1,4):
                if self.matrice[i][j] != 0:
                    q = j-1
                    while q >= 0 and self.matrice[i][q] == 0  :
                        self.matrice[i][q] = self.matrice[i][q+1]
                        self.matrice[i][q+1] = 0
                        q -=1
    
 
    def decalage_droite(self):
        """Decale toutes les cases vers la droite"""
        
        for i in range(4):
            for j in range(2,-1,-1):
                if self.matrice[i][j] != 0:
                    q = j+1
                    while q <= 3 and self.matrice[i][q] == 0  :
                        self.matrice[i][q] = self.matrice[i][q-1]
                        self.matrice[i][q-1] = 0
                        q += 1
                        
    
    def decalage_haut(self):
        """Decale toutes les cases vers le haut"""
        
        for j in range(4):
            for i in range(1,4):
                if self.matrice[i][j] != 0:
                    q = i-1
                    while q >= 0 and self.matrice[q][j] == 0 :
                        self.matrice[q][j] = self.matrice[q+1][j]
                        self.matrice[q+1][j] = 0
                        q -=1
                        

    def decalage_bas(self):
        """Decale toutes les cases vers le bas"""
        
        for j in range(4):
            for i in range(2,-1,-1):
                if self.matrice[i][j] != 0:
                    q = i+1
                    while q <= 3 and self.matrice[q][j] == 0  :
                        self.matrice[q][j] = self.matrice[q-1][j]
                        self.matrice[q-1][j] = 0
                        q += 1
                        
    
    def fusion_gauche(self):
        """Fusionne les cases adjacentes : si la case à droite vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle de droite de la case considérée
           -> on actualise le score de la partie                          """
           
        for i in range(4):
            j = 0
            test = False
            while j <= 2 :
                if self.matrice[i][j+1] == self.matrice[i][j] and self.matrice[i][j] != 0:
                    self.matrice[i][j] *= 2
                    self.matrice[i][j+1] = 0
                    self.score += self.matrice[i][j]
                    test = True
                j += 1
            if test : #Si on a fusionné sur la ligne on décale 
                #On a au plus un décalage à faire par case 
                for j in range(2,4):
                    if self.matrice[i][j] != 0 and self.matrice[i][j-1] == 0:
                        self.matrice[i][j-1] = self.matrice[i][j]
                        self.matrice[i][j] = 0
                
               
    def fusion_droite(self):
        """Fusionne les cases adjacentes : si la case à gauche vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle de gauche de la case considérée
           -> on actualise le score de la partie                          """
           
        for i in range(4):
            j = 3
            test = False
            while j >= 1 :
                if self.matrice[i][j] == self.matrice[i][j-1] and self.matrice[i][j] != 0:
                    self.matrice[i][j] *= 2
                    self.matrice[i][j-1] = 0
                    self.score += self.matrice[i][j]
                    test = True
                j -= 1
            if test :
                for j in range(1,-1,-1):
                    if self.matrice[i][j] != 0 and self.matrice[i][j+1] == 0:
                        self.matrice[i][j+1] = self.matrice[i][j]
                        self.matrice[i][j] = 0
                
    
    def fusion_haut(self):
        """Fusionne les cases adjacentes : si la case en dessous vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle en dessous de la case considérée
           -> on actualise le score de la partie                          """
           
        for j in range(4):
            i = 0
            test = False
            while i <= 2 :
                if self.matrice[i+1][j] == self.matrice[i][j] and self.matrice[i][j] != 0:
                    self.matrice[i][j] *= 2
                    self.matrice[i+1][j] = 0
                    self.score += self.matrice[i][j]
                    test = True
                i += 1
            if test :
                for i in range(2,4):
                    if self.matrice[i][j] != 0 and self.matrice[i-1][j] == 0:
                        self.matrice[i-1][j] = self.matrice[i][j]
                        self.matrice[i][j] = 0
    
    def fusion_bas(self):
        """Fusionne les cases adjacentes : si la case au dessus vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle au dessus de la case considérée
           -> on actualise le score de la partie                          """
           
        for j in range(4):
            i = 3
            test = False
            while i >= 1 :
                if self.matrice[i][j] == self.matrice[i-1][j] and self.matrice[i][j] != 0:
                    self.matrice[i][j] *= 2
                    self.matrice[i-1][j] = 0
                    self.score += self.matrice[i][j]
                    test = True
                i -= 1
            if test :
                for i in range(1,-1,-1):
                    if self.matrice[i][j] != 0 and self.matrice[i+1][j] == 0:
                        self.matrice[i+1][j] = self.matrice[i][j]
                        self.matrice[i][j] = 0
  
    
    def coup_suivant(self,direction):
        """Effectue le mouvement complet :
           -> on décale toutes les cases dans la direction
           -> on fusionne les cases adjacentes 
           -> on redécale toutes les cases dans la direction """
           
        if direction == 'gauche' :
            self.decalage_gauche()
            self.fusion_gauche()
            
        elif direction == 'droite' :
            self.decalage_droite()
            self.fusion_droite()
                    
        elif direction == 'haut' :
            self.decalage_haut()
            self.fusion_haut()
        
        elif direction == 'bas' :
            self.decalage_bas()
            self.fusion_bas()

        else:
            raise ValueError("La direction n'existe pas")
        

    def fin_jeu(self):
        """Renvoie une liste qui contient la liste des mouvements possbiles
           ie ceux qui modifient la matrice    """
        
        Liste_coup = [] 
        mvt_bas = True
        mvt_haut = True  
        mvt_gauche = True  
        mvt_droite = True  
        
        """ Pour les mouvements verticaux """
        for i in range(3): #sur chaque ligne on verifie si on peut fusionner ou décaler
            for j in range(4):
                if mvt_bas and self.matrice[i][j] != 0 : 
                    if self.matrice[i+1][j] == 0 or self.matrice[i+1][j] == self.matrice[i][j] :
                        Liste_coup.append('bas')
                        mvt_bas = False
                            
                if mvt_haut and self.matrice[3-i][j] != 0 : 
                    if self.matrice[2-i][j] == 0 or self.matrice[2-i][j] == self.matrice[3-i][j] :
                        Liste_coup.append('haut')
                        mvt_haut = False
                  
                    
        """ Pour les mouvements horizontaux """
        for j in range(3): #sur chaque colonne on verifie si on peut fusionner ou décaler
            for i in range(4): 
                if mvt_droite and self.matrice[i][j] != 0 : 
                    if self.matrice[i][j+1] == 0 or self.matrice[i][j+1] == self.matrice[i][j] :  
                        Liste_coup.append('droite')
                        mvt_droite = False
                        
                if mvt_gauche and self.matrice[i][3-j] != 0 : 
                    if self.matrice[i][2-j] == 0 or self.matrice[i][2-j] == self.matrice[i][3-j] :   
                        Liste_coup.append('gauche')
                        mvt_gauche = False  
        
        return Liste_coup
    
    

    def jeu_2048_random(self,direction):
        """Effectue une partie aléatoire après le mouvement imposé et renvoie 
           le score"""
           
        self.coup_suivant(direction)   
        self.actualise()
        fin = self.fin_jeu()
        q = 0
        while len(fin) > 0 and q < 20 :        #On se limite à une profondeur de 20 coups
            self.coup_suivant(rd.choice(fin))  #On prend une direction aléatoiren et on fait le coup
            self.actualise()                   #On ajoute un 2/4 aléatoirment dans la grille
            fin = self.fin_jeu()               #On actualise la liste des coups possibles
            q += 1   
        
        return self.score
    

    def direction_suivante(self,coups):
        """Renvoie la meilleure direction :
           on fait la moyenne des scores sur N parties aléatoires pour un nombre maximum
           de coups après avoir fait une des direction possibles, celle avec les meilleures 
           scores en moyenne est considérée comme étant la meilleure 
           
           Le score est tel que si l'on forme un 8 on gagne 8 points, et ainsi de suite """
           
        if len(coups) == 1: #Si on ne peut que faire un mouvement on le fait
            return coups[0]
        
        N = 100   #Nombre de parties aléatoires
        
        res = coups[0]
        somme = 0
        for j in range(N):
            grille = self.copie()
            somme += grille.jeu_2048_random(coups[0])
            
        for i in range(1,len(coups)):
            total = 0
            for j in range(N):
                grille = self.copie()
                total += grille.jeu_2048_random(coups[i])
            if total > somme :
                somme = total
                res = coups[i]
      
        return res
    
    def simulation():
        """Cette fonction simule une partie complète et renvoie le score de la partie"""
        
        jeu = jeu2048()  #On initialise le jeu
        
        jeu.actualise()  #On initialise la matrice du jeu
        jeu.actualise()
        fin = jeu.fin_jeu()
            
        """Debut_du_jeu""" 
        for i in range(25): #On peut faire des coups aléatoire au début ça ne change rien
                            #On ne peut pas perdre en moins de 25 coups (empiriquement)
            jeu.coup_suivant(rd.choice(fin))
            jeu.actualise()
            fin = jeu.fin_jeu()
    
        while len(fin) > 0: #tant qu'on peut jouer on continue 
            jeu.coup_suivant(jeu.direction_suivante(fin))
            jeu.actualise()
            fin = jeu.fin_jeu()
            print(jeu)
        liste = []
        for i in range(4):
            liste += jeu.matrice[i]
        return liste.sorte(reverse = False)
    


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
        
        
        
    
"""On effectue les tests des fonctions"""
#unittest.main()


resultat = []
for i in range(100):
    print("#",i+1,sep="")
    t1 = time.time()
    resultat.append(jeu2048.simulation())
    t2 = time.time()
    print("Durée de la partie: {0}min {1}s\n".format(int(t2-t1)//60,int(t2-t1)%60))




