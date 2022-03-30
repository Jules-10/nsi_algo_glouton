"""
Sujet : dm algorithme glouton
Auteur : Jules TENNENBAUM, 103
Date : 25/03/2022
"""

# un compteur d'étapes k est intégré aux deux fonctions principales (et affiché également)


# ------------------------- pour l'algorithme brute -------------------------


def calculer_score(binary, items, k) :
    """
    calcule le score d'une série de vidéos à partie de son code binaire
    Entrée : le code binaire de la série, la liste des vidéos
    Sortie : la taille de la série et sa durée totale
    """
    duree, taille = 0,0
    for i in range(len(binary)) :
        k+=1
        if binary[i] == "1" :
            taille += items[i]["taille"]
            duree += items[i]["duree"]
    return taille,duree, k



def algo_brute(items, taille_max=5) :
    """
    algorithme qui parcourt chaque possibilité et en trouve la meilleure
    Entrée : une liste de toutes les videos sous forme de dictionnaires conprenant duree et taille comme clés et des float comme valeurs, et un entier : l'espace disponible sur la clé usb (facultatif, à 5 par défaut)
    Sortie : le numéro des vidéos pour avoir la durée la plus grande possible stockée sur la clé
    """
    k=0

    #initialisations
    n_items = len(items)
    meilleure_serie = ""
    meilleur_score = 0
    meilleure_taille = 0

    # parcourt de chaque possibilité, codée sous forme d'un nombre binaire. Un 0 correspond à une video non ajoutée. Un 1 correspond à une video ajoutée.
    for i in range(2**n_items) :
        k+=1
        # conversion de i en binaire
        n_bin = str("{0:0"+str(n_items)+"b}").format(i)
        taille, duree, k = calculer_score(n_bin, items, k)
        # on compare le temps total de vidéos avec le max précédemment atteint (à condition qu'il rentre sur la clé usb). Si le temps de cet ensemble est supérieur, on met à jour les variables
        if taille <= taille_max :
            if duree > meilleur_score :
                meilleur_score = duree
                meilleure_serie = n_bin
                meilleure_taille = taille
    
    print("Nombre d'étapes :",k)
    return [i+1 for i in range(n_items) if meilleure_serie[i] == "1"]






# ------------------------- pour l'algorithme glouton -------------------------


def classement_videos(items, k) :
    """
    classe les videos par ordre croissant de rentabilité, avec un tri par insertion
    Entrée : la liste des vidéos en désordre
    Sortie : la liste des vidéos classées
    """
    for i in range(1, len(items)) :
        v_temp = items[i]
        j = i
        while j > 0 and v_temp["rentabilite"] > items[j-1]["rentabilite"] :
            k+=1
            items[j] = items[j-1]
            j -= 1
        items[j] = v_temp
    return items, k



def algo_glouton(items, taille_restante=5) :
    """
    Trouve une des meilleures séries de vidéos en sélectionnant celle avec le meilleure ratio durée/volume à répétition
    Entrée : une liste de toutes les videos sous forme de dictionnaires conprenant duree et taille comme clés et des float comme valeurs, et un entier : l'espace disponible sur la clé usb (facultatif, à 5 par défaut)
    Sortie : le numéro des vidéos pour avoir la durée la plus grande possible stockée sur la clé
    """
    k=0
    n_items = len(items)

    for i in range(n_items) :
        k+=1
        # calcul du ratio de rentabilite de chaque video
        items[i]["rentabilite"] = items[i]["duree"] / items[i]["taille"]
        # ajoute un numéro (de 1 à n_items) à chaque video, pour pouvoir les classer différemment après tout en se rappelant de leur position initiale
        items[i]["id"] = i+1

    items, k = classement_videos(items, k)
    liste_videos_prises = []

    # parcours les videos dans l'ordre, dès qu'on croise une qui rentre dans la clé on l'y ajoute et reprend au début de la boucle
    suite_possible = True
    while suite_possible :
        for i in range(n_items) :
            k+=1
            if items[i]["taille"] < taille_restante :
                taille_restante -= items[i]["taille"]
                liste_videos_prises.append(items[i]["id"])
                items.pop(i)
                n_items -= 1
                break
            # si on a finit le parcours de chaque video sans en trouver une qui correspond, on sort des boucles
            elif i == n_items-1 :
                suite_possible = False
    print("Nombre d'étapes :",k)
    return liste_videos_prises






# ------------------------- appel des fonctions -------------------------

items = [{"duree": 114, "taille": 4.57},{"duree": 32, "taille": 630/1024},{"duree": 20, "taille": 1.65},{"duree": 4, "taille": 85/1024},{"duree": 18, "taille": 2.15},{"duree": 80, "taille": 2.71},{"duree": 5, "taille": 320/1024}]
print("Algorithme de force brute : ")
print(algo_brute(items))

print()

items = [{"duree": 114, "taille": 4.57},{"duree": 32, "taille": 630/1024},{"duree": 20, "taille": 1.65},{"duree": 4, "taille": 85/1024},{"duree": 18, "taille": 2.15},{"duree": 80, "taille": 2.71},{"duree": 5, "taille": 320/1024}]
print("\nAlgorithme glouton : ")
print(algo_glouton(items))

print()