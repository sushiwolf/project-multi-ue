# BOITE A OUTILS PVC

from time import *
from random import *
from math import *
import os

''' Génération aléatoire des coordonnées des villes sur une carte 400x400
    Remplissage de la matrice des distances '''

def generation_villes(liste_ville_new,nb_villes):

    for ville in liste_ville_new:
        liste_coordonnees.append((float(ville[1]),float(ville[2])))
    for i in range( nb_villes ):
        ligne = []
        for j in range( nb_villes ):
            (x1,y1) = liste_coordonnees[ i ]
            (x2,y2) = liste_coordonnees[ j ]
            dx,dy = x1-x2,y1-y2
            ligne.append( sqrt( dx*dx + dy*dy ) )
        matrice_distances.append( ligne )


def sauver_villes_sur_fichier( fichier ):
    f = open( fichier , 'w' )
    for i in range( nb_villes ):
         ( x , y ) = liste_coordonnees[i]
         f.write( str(x)+"\n")
         f.write( str(y)+"\n")
    f.close()



def charger_villes_depuis_fichier( fichier ):
    f = open( fichier , "r" )
    while( True ):
        x = f.readline()
        if not x:
            break
        y = f.readline()
        if not y:
            break
        liste_coordonnees.append((float(x),float(y)))
    f.close()
    for i in range( nb_villes ):
        ligne = []
        for j in range( nb_villes ):
            (x1,y1) = liste_coordonnees[ i ]
            (x2,y2) = liste_coordonnees[ j ]
            dx,dy = x1-x2,y1-y2
            ligne.append( sqrt( dx*dx + dy*dy ) )
        matrice_distances.append( ligne )






# retourne la ville la plus proche de la ville "ville"
def ville_plus_proche( ville , villes_interdites ):
    d = 1000.0
    ville_plus_proche = None
    for v in range( nb_villes ):
        if ( v != ville ):
            if matrice_distances[ ville ] [ v ] < d and v not in villes_interdites :
                d = matrice_distances[ ville ][ v ]
                ville_plus_proche = v
    return (ville_plus_proche , d )

# PARTIE ALGORITHME GLOUTON : VILLE LA PLUS PROCHE
def glouton( ):
    ville_courante = 0
    parcours = [ ville_courante  ]
    for v in range( nb_villes-1 ):
        ( ville_courante , distance ) = ville_plus_proche( ville_courante , parcours )
        parcours.append( ville_courante )
    return parcours

# TRANSFORMATION 1 : echange de 2 villes

def permute_2_villes_hasard( parcours ):
    v1 = randint(0,nb_villes-1)
    v2 = v1
    while v2==v1:
        v2 = randint(0,nb_villes-1)
    parcours[v1], parcours[v2] = parcours[v2], parcours[v1]
    return parcours




# TRANSFORMATION 2 : retournement de la sous liste entre 2 villes

# Algorithme inspiré par Cambridge Numerical Recipes
# On propose d'autres opérations élémentaires plus efficaces !
#    - Renversement du chemin entre deux villes tirées au hasard
#    - Supression et insertion d'un bout de chemin tiré au hasard après une ville tirée au hasard
# Permet de renverser un sous chemin entre 2 villes
# Traite le cas particulier du sous chemin à 2 villes consécutives
# comme une permutation

def renverse_sous_liste(liste, depart, arrivee):
    # print("rsl")
    longueur = len(liste)
    while depart != arrivee:
        position_depart = liste[depart]
        liste[depart] = liste[arrivee]
        liste[arrivee] = position_depart
        delta = abs(depart - arrivee)
        if delta == 1 or delta == (longueur - 1):
            break
        depart = (depart + 1) % longueur
        arrivee = (arrivee - 1) % longueur
    return liste


# Evalue la longueur perdue ou gagnée par l'opération renverse_sous_liste
def delta_longueur_sur_renversement(liste, depart, arrivee):
    d = 0.0
    longueur = len(liste)
    # on casse les deux liens originaux
    avant_depart = (depart - 1) % longueur
    apres_arrivee = (arrivee + 1) % longueur
    d -= matrice_distances[liste[avant_depart]][liste[depart]]
    d -= matrice_distances[liste[arrivee]][liste[apres_arrivee]]
    # on rajoute les deux nouveaux liens
    d += matrice_distances[liste[avant_depart]][liste[arrivee]]
    d += matrice_distances[liste[depart]][liste[apres_arrivee]]
    return d


# Coupe la sous liste allant de l'indice depart jusqu'à l'indice arrivee
# et l'insere entre less villes d'index insertion et insertion+1

def coupe_et_insert_sous_liste(liste, depart, arrivee, insertion):
    # print("ceisl")
    longueur = len(liste)
    sous_liste = []
    ville_insertion = liste[insertion]
    ville_arrivee = liste[arrivee]
    ville_depart = liste[depart]
    ville = ville_depart
    while ville != ville_arrivee:
        ville = liste[depart]
        liste.remove(ville)
        sous_liste.append(ville)
        if depart == len(liste):
            depart = 0
    pos = liste.index(ville_insertion)
    l = len(sous_liste)
    liste[pos + 1: pos + 1] = sous_liste
    return liste


# Evalue la longueur gagnée ou perdue par l'opération coupe_et_insert_sous_liste
def delta_longueur_sur_coupe_et_insertion(liste, depart, arrivee, insertion):
    d = 0.0
    longueur = len(liste)
    # on casse les deux liens originaux
    avant_depart = (depart - 1) % longueur
    apres_arrivee = (arrivee + 1) % longueur
    d -= matrice_distances[liste[avant_depart]][liste[depart]]
    d -= matrice_distances[liste[arrivee]][liste[apres_arrivee]]
    # on retire la liaison entre les 2 villes insertion et insertion+1
    d -= matrice_distances[liste[insertion]][liste[(insertion + 1) % longueur]]
    # on rajoute les deux nouveaux liens
    d += matrice_distances[liste[insertion]][liste[depart]]
    # la ville suivant l'insertion que l'on rattache à l'autre bout ( arrivee )
    insertion = (insertion + 1) % longueur
    d += matrice_distances[liste[arrivee]][liste[insertion]]
    # Reconnexion entre avant_depart et apres_arrivee
    d += matrice_distances[liste[avant_depart]][liste[apres_arrivee]]
    return d


def retourne_deux_villes_avec_ecart_min(ecart,nb_villes):
    # print( "r2vaem" )
    e = 0
    ville1 = 0
    ville2 = 0
    while (e < ecart or e > (nb_villes - ecart)) or ville1 == ville2:
        ville1 = floor(uniform(0, nb_villes))
        ville2 = floor(uniform(0, nb_villes))
        e = abs(ville1 - ville2)
    return ville1, ville2


def ville_hors_segment(depart, arrivee,nb_villes):
    # print( "vhs" , depart , arrivee )
    ville = arrivee
    if depart < arrivee:
        while (ville >= depart - 1 and ville <= arrivee):
            ville = floor(uniform(0, nb_villes))
    else:
        while (ville <= arrivee or ville >= depart - 1):
            ville = floor(uniform(0, nb_villes))

    return ville




def longueur_parcours( parcours,nb_villes ):
    l = 0.0
    for v in range( nb_villes - 1 ):
        l += matrice_distances[parcours[v]][parcours[v+1]]
    l+= matrice_distances[ parcours[nb_villes - 1]][parcours[0]]
    return l

def solution_par_recuit_simule_avance(iterations_temperature, max_chemins, max_ameliorations, facteur_temperature,
                                      taux_renversement,nb_villes):
    nb_over = max_chemins * nb_villes
    nb_limite = max_ameliorations * nb_villes
    nb_succes = 0

    meilleur_parcours = list(range(0, nb_villes))
    meilleure_longueur = longueur_parcours(meilleur_parcours,nb_villes)
    #meilleure_solution = (meilleur_parcours, meilleure_longueur)
    parcours = list(meilleur_parcours)
    longueur = meilleure_longueur
    temperature = 0.5

    for j in range(iterations_temperature):
        nb_succes = 0
        print("iteration : ", j)
        for k in range(nb_over):
            # faut-il faire un renversement ou une insertion ?
            renversement = False
            if random() < taux_renversement:
                renversement = True
            (ville1, ville2) = retourne_deux_villes_avec_ecart_min(3,nb_villes)
            ville3 = 0
            deltaE = 0

            if renversement:
                # print( "Renversement " , ville1 , ville2 , nb_villes )
                deltaE = delta_longueur_sur_renversement(parcours, ville1, ville2)
            else:
                ville3 = ville_hors_segment(ville1, ville2, nb_villes)
                # print( "Insertion " , ville1 , ville2 , ville3 , nb_villes )
                deltaE = delta_longueur_sur_coupe_et_insertion(parcours, ville1, ville2, ville3)

            if (deltaE < 0) or (uniform(0.0, 1.0) < exp(-deltaE / temperature)):
                # on fait vraiement les transformations
                nb_succes += 1
                if renversement:
                    parcours = renverse_sous_liste(parcours, ville1, ville2)
                else:
                    coupe_et_insert_sous_liste(parcours, ville1, ville2, ville3)
                longueur = longueur_parcours(parcours,nb_villes)

                if longueur < meilleure_longueur:
                    meilleur_parcours = list(parcours)
                    meilleure_longueur = longueur
                    #temperature = 0.5

            if nb_succes >= nb_limite:
                break

        # On baisse la température
        # temperature -= deltaT
        temperature = temperature * facteur_temperature
        print("Température actuelle : ", temperature)
        print("Meilleure longueur du cycle : ", meilleure_longueur)
        # solution = parcours, longueur
        # affiche_solution("Recuit simulé avancé", solution)
        if nb_succes == 0:
            break

    return meilleur_parcours

# PARTIE PROGRAMME PRINCIPAL

#La liste des couples de coordonnées des villes
liste_coordonnees = []
#La matrice des distances entre les villes
matrice_distances =  []




#parcours_glouton = glouton()
#parcours_rs = solution_par_recuit_simule( parcours_glouton , nb_villes*10 , 100000 , 0.999 )
def solution(liste_ville_new,iterations_temperature):
    nb_villes = len(liste_ville_new)
    generation_villes(liste_ville_new,nb_villes)

    parcours_rs = solution_par_recuit_simule_avance( iterations_temperature , 100 , 10 , 0.9 , 0.9, nb_villes)
    parcours_final = []
    for p in parcours_rs:
        parcours_final.append(liste_ville_new[p])
    return parcours_final
