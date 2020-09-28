#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:06:42 2019

@author: alanloret
"""

import random as rd

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


cdef class jeu2048:
    cdef public list matrice
    cdef public int score

    def __init__(self):
        self.matrice = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.score = 0

    def __str__(self):
        cdef int i
        string = "Le score est de " + str(self.score) + "\n"
        for i in range(4):
            string += f"{self.matrice[4*i]}|{self.matrice[4*i + 1]}|{self.matrice[4*i + 2]}|{self.matrice[4*i + 3]}\n"

        return string

    cdef copie(self):
        """ Effectue une copie de self dans grille"""

        cdef int i
        grille = jeu2048()

        for i in range(16):
            grille.matrice[i] = self.matrice[i]
        return grille

    cpdef list case_vide(self):
        """Actualise la liste des cases vides de la grille"""

        cdef list Liste = []
        cdef int i

        for i in range(16):
            if self.matrice[i] == 0: Liste.append(i)
        return Liste

    cpdef void actualise(self):
        """Actualise la grille en ajoutant un 2 ou 4 aléatoirement dans 
           une case vide de la grille"""

        cdef int i = rd.choice(self.case_vide())  # On en choisit une au hasard

        if rd.uniform(0,1) < 0.875:
            self.matrice[i] = 2
        else:
            self.matrice[i] = 4

    cpdef void decalage_gauche(self):
        """Decale toutes les cases vers la gauche"""

        cdef int i, j, q

        for i in range(4):
            for j in range(1, 4):
                if self.matrice[4*i + j] != 0:
                    q = j - 1
                    while q >= 0 and self.matrice[4*i + q] == 0:
                        self.matrice[4*i + q] = self.matrice[4*i + q + 1]
                        self.matrice[4*i + q + 1] = 0
                        q -= 1

    cpdef void decalage_droite(self):
        """Decale toutes les cases vers la droite"""

        cdef int i, j, q

        for i in range(4):
            for j in range(2, -1, -1):
                if self.matrice[4*i + j] != 0:
                    q = j + 1
                    while q <= 3 and self.matrice[4*i + q] == 0:
                        self.matrice[4*i + q] = self.matrice[4*i + q - 1]
                        self.matrice[4*i + q - 1] = 0
                        q += 1

    cpdef void decalage_haut(self):
        """Decale toutes les cases vers le haut"""

        cdef int i, j, q

        for j in range(4):
            for i in range(1, 4):
                if self.matrice[4*i + j] != 0:
                    q = i - 1
                    while q >= 0 and self.matrice[4*q + j] == 0:
                        self.matrice[4*q + j] = self.matrice[4*q + 4 + j]
                        self.matrice[4*q + 4 + j] = 0
                        q -= 1

    cpdef void decalage_bas(self):
        """Decale toutes les cases vers le bas"""

        cdef int i, j, q

        for j in range(4):
            for i in range(2, -1, -1):
                if self.matrice[4*i + j] != 0:
                    q = i + 1
                    while q <= 3 and self.matrice[4*q + j] == 0:
                        self.matrice[4*q + j] = self.matrice[4*q - 4 + j]
                        self.matrice[4*q - 4 + j] = 0
                        q += 1

    cpdef void fusion_gauche(self):
        """Fusionne les cases adjacentes : si la case à droite vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle de droite de la case considérée
           -> on actualise le score de la partie                          """

        cdef int i, j
        cdef bint test

        for i in range(4):
            j = 0
            test = False
            while j <= 2:
                if self.matrice[4*i + j + 1] == self.matrice[4*i + j] and self.matrice[4*i + j] != 0:
                    self.matrice[4*i + j] *= 2
                    self.matrice[4*i + j + 1] = 0
                    self.score += self.matrice[4*i + j]
                    test = True
                j += 1
            if test:  # Si on a fusionné sur la ligne on décale
                # On a au plus un décalage à faire par case
                for j in range(2, 4):
                    if self.matrice[4*i + j] != 0 and self.matrice[4*i + j - 1] == 0:
                        self.matrice[4*i + j - 1] = self.matrice[4*i + j]
                        self.matrice[4*i + j] = 0

    cpdef void fusion_droite(self):
        """Fusionne les cases adjacentes : si la case à gauche vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle de gauche de la case considérée
           -> on actualise le score de la partie                          """

        cdef int i, j
        cdef bint test

        for i in range(4):
            j = 3
            test = False
            while j >= 1:
                if self.matrice[4*i + j] == self.matrice[4*i + j - 1] and self.matrice[4*i + j] != 0:
                    self.matrice[4*i + j] *= 2
                    self.matrice[4*i + j - 1] = 0
                    self.score += self.matrice[4*i + j]
                    test = True
                j -= 1
            if test:
                for j in range(1, -1, -1):
                    if self.matrice[4*i + j] != 0 and self.matrice[4*i + j + 1] == 0:
                        self.matrice[4*i + j + 1] = self.matrice[4*i + j]
                        self.matrice[4*i + j] = 0

    cpdef void fusion_haut(self):
        """Fusionne les cases adjacentes : si la case en dessous vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle en dessous de la case considérée
           -> on actualise le score de la partie                          """

        cdef int i, j
        cdef bint test

        for j in range(4):
            i = 0
            test = False
            while i <= 2:
                if self.matrice[4*i + 4 + j] == self.matrice[4*i + j] and self.matrice[4*i + j] != 0:
                    self.matrice[4*i + j] *= 2
                    self.matrice[4*i + 4 + j] = 0
                    self.score += self.matrice[4*i + j]
                    test = True
                i += 1
            if test:
                for i in range(2, 4):
                    if self.matrice[4*i + j] != 0 and self.matrice[4*i - 4 + j] == 0:
                        self.matrice[4*i - 4 + j] = self.matrice[4*i + j]
                        self.matrice[4*i + j] = 0

    cpdef void fusion_bas(self):
        """Fusionne les cases adjacentes : si la case au dessus vaut la même chose
           -> on multiplie par deux la case
           -> on met à 0 celle au dessus de la case considérée
           -> on actualise le score de la partie                          """

        cdef int i, j
        cdef bint test

        for j in range(4):
            i = 3
            test = False
            while i >= 1:
                if self.matrice[4*i + j] == self.matrice[4*i - 4 + j] and self.matrice[4*i + j] != 0:
                    self.matrice[4*i + j] *= 2
                    self.matrice[4*i - 4 + j] = 0
                    self.score += self.matrice[4*i + j]
                    test = True
                i -= 1
            if test:
                for i in range(1, -1, -1):
                    if self.matrice[4*i + j] != 0 and self.matrice[4*i + 4 + j] == 0:
                        self.matrice[4*i + 4 + j] = self.matrice[4*i + j]
                        self.matrice[4*i + j] = 0

    cpdef void coup_suivant(self, str direction):
        """ Effectue le mouvement complet :
           -> on décale toutes les cases dans la direction
           -> on fusionne les cases adjacentes 
           -> on redécale toutes les cases dans la direction """

        if direction == 'gauche':
            self.decalage_gauche()
            self.fusion_gauche()

        elif direction == 'droite':
            self.decalage_droite()
            self.fusion_droite()

        elif direction == 'haut':
            self.decalage_haut()
            self.fusion_haut()

        elif direction == 'bas':
            self.decalage_bas()
            self.fusion_bas()

        else:
            raise ValueError("La direction n'existe pas")

    cpdef fin_jeu(self):
        """ Renvoie une liste qui contient la liste des mouvements possbiles
           ie ceux qui modifient la matrice    """

        Liste_coup = []
        cdef int i, j
        cdef bint mvt_bas, mvt_haut, mvt_gauche, mvt_droite
        mvt_bas, mvt_haut, mvt_gauche, mvt_droite = True, True, True, True

        # Pour les mouvements verticaux
        for i in range(3):  # sur chaque ligne on verifie si on peut fusionner ou décaler
            for j in range(4):
                if mvt_bas and self.matrice[4*i + j] != 0:
                    if self.matrice[4*i + 4 + j] == 0 or self.matrice[4*i + 4 + j] == self.matrice[4*i + j]:
                        Liste_coup.append('bas')
                        mvt_bas = False

                if mvt_haut and self.matrice[12 - 4*i + j] != 0:
                    if self.matrice[8 - 4*i + j] == 0 or self.matrice[8 - 4*i + j] == self.matrice[12 - 4*i + j]:
                        Liste_coup.append('haut')
                        mvt_haut = False

        # Pour les mouvements horizontaux
        for j in range(3):  # sur chaque colonne on verifie si on peut fusionner ou décaler
            for i in range(4):
                if mvt_droite and self.matrice[4*i + j] != 0:
                    if self.matrice[4*i + j + 1] == 0 or self.matrice[4*i + j + 1] == self.matrice[4*i + j]:
                        Liste_coup.append('droite')
                        mvt_droite = False

                if mvt_gauche and self.matrice[4*i + 3 - j] != 0:
                    if self.matrice[4*i + 2 - j] == 0 or self.matrice[4*i + 2 - j] == self.matrice[4*i + 3 - j]:
                        Liste_coup.append('gauche')
                        mvt_gauche = False

        return Liste_coup

    cpdef int jeu_2048_random(self, str direction):
        """Effectue une partie aléatoire après le mouvement imposé et renvoie le score"""

        cdef int q = 0
        self.coup_suivant(direction)
        self.actualise()
        fin = self.fin_jeu()

        while len(fin) > 0 and q <= 20:  # On se limite à une profondeur de 20 coups
            self.coup_suivant(rd.choice(fin))  # On prend une direction aléatoirement et on fait le coup
            self.actualise()  # On ajoute un 2/4 aléatoirement dans la grille
            fin = self.fin_jeu()  # On actualise la liste des coups possibles
            q += 1

        return self.score

    cpdef str direction_suivante(self, coups):
        """ Renvoie la meilleure direction :
           on fait la moyenne des scores sur N parties aléatoires pour un nombre maximum
           de coups après avoir fait une des direction possibles, celle avec les meilleures 
           scores en moyenne est considérée comme étant la meilleure 
           
           Le score est tel que si l'on forme un 8 on gagne 8 points, et ainsi de suite """

        if len(coups) == 1: return coups[0]

        cdef int N = 200  # Nombre de parties aléatoires
        cdef str res = coups[0]
        cdef int somme = 0
        cdef int total = 0
        cdef int i
        cdef str dir

        for i in range(N):
            grille = self.copie()
            somme += grille.jeu_2048_random(res)

        for dir in coups:
            total = 0
            for i in range(N):
                grille = self.copie()
                total += grille.jeu_2048_random(dir)
            if total > somme:
                somme = total
                res = dir

        return res

    cpdef void simulation(self):
        """Cette fonction simule une partie complète et affiche la grille à chaque coup"""

        jeu = jeu2048()  # On initialise le jeu

        jeu.actualise()  # On initialise la matrice du jeu avec 2 cases non vides
        jeu.actualise()
        fin = jeu.fin_jeu()

        # Debut du jeu
        while len(fin) > 0:  # Tant qu'on peut jouer on continue
            jeu.coup_suivant(jeu.direction_suivante(fin))
            jeu.actualise()
            print(jeu)
            fin = jeu.fin_jeu()

    cpdef int partie(self):
        """Cette fonction joue une partie complète et renvoie le score de la partie"""

        cdef int i

        jeu = jeu2048()  # On initialise le jeu

        jeu.actualise()  # On initialise la matrice du jeu
        jeu.actualise()
        fin = jeu.fin_jeu()

        # Debut du jeu
        while len(fin) > 0:  # Tant qu'on peut jouer on continue
            jeu.coup_suivant(jeu.direction_suivante(fin))
            jeu.actualise()
            fin = jeu.fin_jeu()

        print(jeu)

        return jeu.score

