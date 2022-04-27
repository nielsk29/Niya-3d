
import globalVariable as glb  # importation des Variables globals
import time
import Draw3d
import objet
import math

def rays(murBrique):   # fonction qui envoie les rayons
    glb.listeRay = []  # liste qui contient les positions des rayons pour les afficher dans la MiniMap
    glb.listeRond = []  # liste qui contient les cercles à afficher sur la MiniMap
    diffRay = (glb.angleRegard*2 / glb.nbRay) // glb.precision * glb.precision  # calcul de la différence d'angle (en radiant) entre chaque rayon envoyé
    angleRay = (glb.playerAngle-glb.angleRegard) // glb.precision * glb.precision  # calcul de l'angle du 1er rayon
    for i in range(glb.nbRay):  # boucle de chaque rayon

        distanceRay=0  # variable qui contient la distance entre le joueur et la position du rayon
        angleRay=(angleRay +diffRay) // glb.precision * glb.precision  # angle (en radiant) à laquelle le rayon va être envoyé
        posRayX=glb.playerX  # initialisation de la position X du rayon à la position du joueur
        posRayY=glb.playerY  # initialisation de la position Y du rayon à la position du joueur
        pente = -math.tan(angleRay) // glb.precision * glb.precision  # calcul de la pente du rayon comme une fonction affine
        diffPiSur2 = angleRay % (glb.pi / 2)  # différence entre l'angle du rayon et pi sur 2 pour savoir si la pente va être trops grande pour les calculs
        cosAngle = math.cos(angleRay) // glb.precision * glb.precision  # calcul du cosinus de l'angle du rayon
        sinAngle = math.sin(angleRay) // glb.precision * glb.precision  # calcul du sinus de l'angle du rayon
        for nbCar in range(glb.diagCarre):  # boucle qui va envoyé le rayon à la prochaine frontière entre les carrés donc le nombre maximal de cette boucle est le diagonal de la carte
            debut = time.time()
            distCarre, posRayX, posRayY, cote = car_affine(pente,cosAngle,sinAngle,diffPiSur2, posRayX, posRayY)  # utilisation de la fonction qui va calculer où le rayon va toucher la prochaine frontière entre les carrés
            glb.process2 += time.time() - debut
            if cote ==False:  # si la pente du rayon est trops grandes, car le rayon forme une droite presque parallèle ou perpendiculaire à l'axe des abscisses
                pixelparpixel(angleRay,i, murBrique)  # dans ce cas la seule solution est de calculer ce rayon pixel par pixel ce qui prend plus de temps que carreau par carreau
                break  # stop la boucle, car le rayon a touché un mur
            distanceRay+=distCarre  # augmente la distance à laquelle se trouve le rayon du joueur par la distance entre le rayon et la prochaine frontière d'un carré qu'il touche

            colPosRay = math.floor(posRayX/glb.rectSizeX)  # calcul de la colonne à laquelle se trouve le rayon
            lignePosRay = math.floor(posRayY/glb.rectSizeY)  # calcul de la ligne à laquelle se trouve le rayon
            carre=int(lignePosRay*glb.carteSize[0] + colPosRay)  # calcul du carré à laquelle se trouve le rayon grâce à sa colonne et sa ligne

            glb.listeRond.append((posRayX * glb.minimap / glb.screenX, posRayY * glb.minimap / glb.screenY))  # ajoute un rond à la frontière pour la miniMap
            if glb.Carte[carre] == "1":  # si le rayon touche un mur
                glb.listeRay.append((posRayX * glb.minimap / glb.screenX, posRayY * glb.minimap / glb.screenY))  # ajoute le rayon pour la miniMap
                #objet.SaveObjet(i, pente, distanceRay, cosAngle, sinAngle)  # utilise la fonction qui regarde si le rayon à toucher un objet

                Draw3d.rect3d(i,angleRay,distanceRay,cote,posRayX,posRayY,murBrique)  # Utilise la fonction qui va dessiner le rectangle (avec un bout de l'image de mur) correspondant au rayon

                break  # stop la boucle, car le rayon a touché un mur
            """if Carte[carre] == "2":
                if (carre in objCarre) == False:
                    listeObjet.append((i,distanceRay))
                    objCarre.append(carre)"""

def pixelparpixel(angleRay,i, murBrique):  # fonction pour calculer le rayon pixel par pixel pour quand le rayon est perpendiculaire ou parallèle à l'axe des abscisses
    for nb in range(glb.diagonal):  # boucle qui va calculer le prochain pixel donc pour maximum de répétition le diagonal des pixels

        posRayX = glb.playerX - math.cos(angleRay) * nb  # calcul position X prochain pixel en soustrayant la position X du joueur par le cosinus de l'angle * le nombre de pixel qu'on a parcouru
        posRayY = glb.playerY - math.sin(angleRay) * nb  # calcul position Y prochain pixel en soustrayant la position Y du joueur par le sinus de l'angle * le nombre de pixel qu'on a parcouru

        colPosRay = math.floor(posRayX / glb.rectSizeX)  # calcul de la colonne à laquelle se trouve le rayon
        lignePosRay = math.floor(posRayY/glb.rectSizeY)  # calcul de la ligne à laquelle se trouve le rayon
        carre = int(lignePosRay * glb.carteSize[0] + colPosRay)  # calcul du carré à laquelle se trouve le rayon grâce à sa colonne et sa ligne


        if glb.Carte[carre] == "1":  # si le rayon touche un mur
            if -0.05<(posRayX%glb.rectSizeX)<0.05:  # on regarde si on a touché un mur perpendiculaire à l'axe X
                cote=1
            else:  # sinon ça veut dire qu'on a touché un mur perpendiculaire à l'axe Y
                cote=2
            Draw3d.rect3d(i, angleRay, nb , cote, posRayX, posRayY, murBrique)  # Utilise la fonction qui va dessiner le rectangle (avec un bout de l'image de mur) correspondant au rayon
            break  # stop la boucle, car le rayon a touché un mur


def car_affine(pente,cosAngle,sinAngle,diffPiSur2,posX, posY):  # fonction qui calcul la prochaine frontière de carré que va toucher le rayon

    if diffPiSur2<0.0001 or diffPiSur2>(glb.pi/2 - 0.0001 ):  # si la pente risque d'être infini ou égal à 0
        return 0,0,0,False  # termine la fonction pour calculer le rayon pixel par pixel

    def f_affine(x):  # création de la fonction affine du rayon avec sa pente
        return pente*x
    if cosAngle > 0:  # si le cosinus de l'angle du rayon est positif ça veut dire que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe X est plus petite que la position X actuelle du rayon
        dizainePosX = posX % glb.rectSizeX  # différence entre la pos X du rayon et la position X de la frontière qu'il peut toucher
        posXtest1 = posX - dizainePosX - 0.05  # position X de la frontière qu'il peut toucher

    else:  # le contraire est que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe X est plus grande que la position X actuelle du rayon
        dizainePosX = glb.rectSizeX - posX % glb.rectSizeX  # différence entre la pos X du rayon et la position X de la frontière qu'il peut toucher
        posXtest1 = posX + dizainePosX + 0.05  # position de la frontière qu'il peut toucher

    if sinAngle < 0:  # si le sinus de l'angle du rayon est négatif ça veut dire que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe Y est plus grande que la position Y actuelle du rayon
        dizainePosY = glb.rectSizeY -posY % glb.rectSizeY  # différence entre la pos Y du rayon et la position Y de la frontière qu'il peut toucher
        posYtest2=posY + dizainePosY + 0.05  # position Y de la frontière qu'il peut toucher
    else:  # le contraire est que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe Y est plus grande que la position Y actuelle du rayon
        dizainePosY = posY % glb.rectSizeY  # différence entre la pos Y du rayon et la position Y de la frontière qu'il peut toucher
        posYtest2 = posY - dizainePosY - 0.05  # position Y de la frontière qu'il peut toucher
    fx = dizainePosY / pente // glb.precision * glb.precision  # calcul de l'incrémentation de la position X pour atteindre l'endroit où il va toucher la frontière si elle est perpendiculaire à l'axe Y
    fy = (f_affine(dizainePosX) // glb.precision) * glb.precision  # calcul l'incrémentation de la position Y pour atteindre l'endroit où il va toucher la frontière si elle est perpendiculaire à l'axe X

    if cosAngle*sinAngle > 0:  # si le cosinus et le sinus sont de même signe
        if sinAngle > 0:  # si le sinus et le cosinus sont positifs
            posXtest2 = posX + fx -0.05  # on augmente la position x si on est dans le cas où on touche la frontière perpendiculaire à l'axe Y pour avoir la position X du rayon dans ce cas-là
            posYtest1 = posY + fy -0.05  # on augmente la position Y si on est dans le cas où on touche la frontière perpendiculaire à l'axe X pour avoir la position X du rayon dans ce cas-là
        else:  # si le sinus et le cosinus sont négatifs
            posXtest2 = posX - fx +0.05  # on baisse la position x si on est dans le cas où on touche la frontière perpendiculaire à l'axe Y pour avoir la position X du rayon dans ce cas-là
            posYtest1 = posY - fy +0.05  # on baisse la position Y si on est dans le cas où on touche la frontière perpendiculaire à l'axe X pour avoir la position X du rayon dans ce cas-là
    else:  # si le cosinus et le sinus ne sont pas de même signe
        if sinAngle > 0:  # si le sinus est positif et le cosinus est négatif
            posXtest2 = posX + fx +0.05   # on augmente la position x si on est dans le cas où on touche la frontière perpendiculaire à l'axe Y pour avoir la position X du rayon dans ce cas-là
            posYtest1 = posY - fy -0.05  # on baisse la position Y si on est dans le cas où on touche la frontière perpendiculaire à l'axe X pour avoir la position X du rayon dans ce cas-là
        else:  # si le sinus est négatif et le cosinus est positif
            posXtest2 = posX - fx -0.05  # on baisse la position x si on est dans le cas où on touche la frontière perpendiculaire à l'axe Y pour avoir la position X du rayon dans ce cas-là
            posYtest1 = posY + fy +0.05  # on augmente la position Y si on est dans le cas où on touche la frontière perpendiculaire à l'axe X pour avoir la position X du rayon dans ce cas-là

    test1 = math.sqrt(fy**2 + dizainePosX**2)  # calcul distance jusqu'à la prochaine frontière que va toucher le rayon perpendiculaire à l'axe X
    test2 = math.sqrt(fx**2 + dizainePosY**2)  # calcul distance jusqu'à la prochaine frontière que va toucher le rayon perpendiculaire à l'axe Y
    if test1 < test2:  # on regarde quelle est la plus petite distance entre le deux et ce sera celle-là qu'il aura touché en premier donc la prochaine frontière que le rayon touche
        return test1,posXtest1, posYtest1,1  # on renvoie les valeurs dans le cas ou le rayon touche en premier une frontière perpendiculaire à l'axe X
    else:
        return test2, posXtest2, posYtest2,2  # on renvoie les valeurs dans le cas ou le rayon touche en premier une frontière perpendiculaire à l'axe Y

