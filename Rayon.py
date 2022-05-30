import globalVariable as glb  # importation des Variables globals
import time
import Draw3d
import objet
import math

def rays(murBrique):   # fonction qui envoie les rayons
    glb.prePosY = 0
    glb.listeRay = []  # liste qui contient les positions des rayons pour les afficher dans la MiniMap
    glb.listeRond = []  # liste qui contient les cercles à afficher sur la MiniMap
    diffRay = (glb.angleRegard*2 / glb.nbRay)   # calcul de la différence d'angle (en radiant) entre chaque rayon envoyé
    angleRay = (glb.playerAngle-glb.angleRegard)%glb.pi2   # calcul de l'angle du 1er rayon
    listAngleObj = objet.CreerListeAngleOBJ(glb.listeObjet)
    pente2 = -math.tan(angleRay)

    for i in range(glb.nbRay):  # boucle de chaque rayon

        distanceRay=0  # variable qui contient la distance entre le joueur et la position du rayon
        angleRay=(angleRay +diffRay)%glb.pi2 # angle (en radiant) à laquelle le rayon va être envoyé
        posRayX=glb.playerX  # initialisation de la position X du rayon à la position du joueur
        posRayY=glb.playerY  # initialisation de la position Y du rayon à la position du joueur
        pente = -math.tan(angleRay) # calcul de la pente du rayon comme une fonction affine
        diffPiSur2 = angleRay % (glb.pi / 2)  # différence entre l'angle du rayon et pi sur 2 pour savoir si la pente va être trops grande pour les calculs
        cosAngle = math.cos(angleRay)   # calcul du cosinus de l'angle du rayon
        sinAngle = math.sin(angleRay)   # calcul du sinus de l'angle du rayon
        signCos = (math.copysign(1,cosAngle),cosAngle<0)
        signSin = (math.copysign(1, sinAngle),sinAngle<0)
        fin = False
        for nbCar in range(glb.diagCarre):  # boucle qui va envoyé le rayon à la prochaine frontière entre les carrés donc le nombre maximal de cette boucle est le diagonal de la carte

            distCarre, posRayX, posRayY, cote = car_affine(pente,cosAngle,sinAngle,diffPiSur2, posRayX, posRayY,signCos,signSin)  # utilisation de la fonction qui va calculer où le rayon va toucher la prochaine frontière entre les carrés

            if cote ==False:  # si la pente du rayon est trops grandes, car le rayon forme une droite presque parallèle ou perpendiculaire à l'axe des abscisses
                pixelparpixel(angleRay,i, murBrique,pente2, listAngleObj, distanceRay)  # dans ce cas la seule solution est de calculer ce rayon pixel par pixel ce qui prend plus de temps que carreau par carreau
                break  # stop la boucle, car le rayon a touché un mur
            distanceRay+=distCarre  # augmente la distance à laquelle se trouve le rayon du joueur par la distance entre le rayon et la prochaine frontière d'un carré qu'il touche

            colPosRay = math.floor(posRayX/glb.rectSizeX)  # calcul de la colonne à laquelle se trouve le rayon
            lignePosRay = math.floor(posRayY/glb.rectSizeY)  # calcul de la ligne à laquelle se trouve le rayon
            carre=int(lignePosRay*glb.carteSize[0] + colPosRay)  # calcul du carré à laquelle se trouve le rayon grâce à sa colonne et sa ligne

            glb.listeRond.append((int(posRayX * glb.minimap / glb.gameX), int(posRayY * glb.minimap / glb.gameY)))  # ajoute un rond à la frontière pour la miniMap
            if glb.Carte[carre] == "1":  # si le rayon touche un mur
                glb.listeRay.append((posRayX * glb.minimap / glb.gameX, posRayY * glb.minimap / glb.gameY))  # ajoute le rayon pour la miniMap
                #objet.SaveObjet(i, pente, distanceRay, cosAngle, sinAngle)  # utilise la fonction qui regarde si le rayon à toucher un objet
                pente2 = pente
                Draw3d.rect3d(i,angleRay,distanceRay,cote,posRayX,posRayY,murBrique,colPosRay,lignePosRay)  # Utilise la fonction qui va dessiner le rectangle (avec un bout de l'image de mur) correspondant au rayon
                objet.drawOBJ(i, distanceRay, angleRay, listAngleObj, pente, posRayX, posRayY)
                break  # stop la boucle, car le rayon a touché un mur
            if fin:
                glb.listeRay.append((posRayX * glb.minimap / glb.gameX, posRayY * glb.minimap / glb.gameY))
                objet.drawOBJ(i, distanceRay, angleRay, listAngleObj, pente, posRayX, posRayY)
                break  # stop la boucle, car le rayon a touché un mur

            if glb.Carte[carre] == "2" and glb.statusPorte[carre][0] == 0:
                    fin = True
    objet.drawObjet2d()
def pixelparpixel(angleRay,i, murBrique,pente,listAngleObj,distanceRay):  # fonction pour calculer le rayon pixel par pixel pour quand le rayon est perpendiculaire ou parallèle à l'axe des abscisses
    for nb in range(glb.diagonal):  # boucle qui va calculer le prochain pixel donc pour maximum de répétition le diagonal des pixels

        posRayX = glb.playerX - math.cos(angleRay) * nb  # calcul position X prochain pixel en soustrayant la position X du joueur par le cosinus de l'angle * le nombre de pixel qu'on a parcouru
        posRayY = glb.playerY - math.sin(angleRay) * nb  # calcul position Y prochain pixel en soustrayant la position Y du joueur par le sinus de l'angle * le nombre de pixel qu'on a parcouru

        colPosRay = math.floor(posRayX / glb.rectSizeX)  # calcul de la colonne à laquelle se trouve le rayon
        lignePosRay = math.floor(posRayY/glb.rectSizeY)  # calcul de la ligne à laquelle se trouve le rayon
        carre = int(lignePosRay * glb.carteSize[0] + colPosRay)  # calcul du carré à laquelle se trouve le rayon grâce à sa colonne et sa ligne


        if glb.Carte[carre] == "1":  # si le rayon touche un mur
            if (posRayX%glb.rectSizeX)<1 or 99<(posRayX%glb.rectSizeX):  # on regarde si on a touché un mur perpendiculaire à l'axe X
                cote=1
            else:  # sinon ça veut dire qu'on a touché un mur perpendiculaire à l'axe Y
                cote=2
            Draw3d.rect3d(i, angleRay, nb, cote, posRayX, posRayY, murBrique,colPosRay,lignePosRay)  # Utilise la fonction qui va dessiner le rectangle (avec un bout de l'image de mur) correspondant au rayon
            objet.drawOBJ(i, nb, angleRay, listAngleObj, pente, posRayX, posRayY)
            break  # stop la boucle, car le rayon a touché un mur


def car_affine(pente,cosAngle,sinAngle,diffPiSur2,posX, posY,signCos,signSin):  # fonction qui calcul la prochaine frontière de carré que va toucher le rayon
    debut = time.time()
    if diffPiSur2<0.0001 or diffPiSur2>(glb.pi/2 - 0.0001 ):  # si la pente risque d'être infini ou égal à 0
        return 0,0,0,False  # termine la fonction pour calculer le rayon pixel par pixel

    def f_affine(x):  # création de la fonction affine du rayon avec sa pente
        return pente*x
    if signCos[1]:  # si le cosinus de l'angle du rayon est négatif ça veut dire que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe Y est plus petite que la position X actuelle du rayon

        dizainePosX = glb.rectSizeX - posX % glb.rectSizeX  # différence entre la pos X du rayon et la position X de la frontière qu'il peut toucher
        posXtest1 = posX + dizainePosX + 0.05  # position de la frontière qu'il peut toucher
    else:  # le contraire est que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe Y est plus grande que la position X actuelle du rayon
        dizainePosX = posX % glb.rectSizeX  # différence entre la pos X du rayon et la position X de la frontière qu'il peut toucher
        posXtest1 = posX - dizainePosX - 0.05  # position X de la frontière qu'il peut toucher

    if signSin[1]:  # si le sinus de l'angle du rayon est négatif ça veut dire que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe Y est plus grande que la position Y actuelle du rayon
        dizainePosY = glb.rectSizeY -posY % glb.rectSizeY  # différence entre la pos Y du rayon et la position Y de la frontière qu'il peut toucher
        posYtest2=posY + dizainePosY + 0.05  # position Y de la frontière qu'il peut toucher
    else:  # le contraire est que la prochaine frontière qui peut toucher si elle est sur perpendiculaire à l'axe Y est plus grande que la position Y actuelle du rayon
        dizainePosY = posY % glb.rectSizeY  # différence entre la pos Y du rayon et la position Y de la frontière qu'il peut toucher
        posYtest2 = posY - dizainePosY - 0.05  # position Y de la frontière qu'il peut toucher


    fx = dizainePosY / pente   # calcul de l'incrémentation de la position X pour atteindre l'endroit où il va toucher la frontière si elle est perpendiculaire à l'axe Y
    fy = f_affine(dizainePosX)   # calcul l'incrémentation de la position Y pour atteindre l'endroit où il va toucher la frontière si elle est perpendiculaire à l'axe X
    if abs(fx*dizainePosY)<abs(fy*dizainePosX):
        posXtest2 = posX + (fx * signSin[0])  # calcul de la position X dans le cas où on touche la frontière perpendiculaire à l'axe Y
        test2 = abs(fx / cosAngle)  # calcul distance jusqu'à la prochaine frontière que va toucher le rayon perpendiculaire à l'axe Y
        return test2, posXtest2, posYtest2, 2  # on renvoie les valeurs dans le cas ou le rayon touche en premier une frontière perpendiculaire à l'axe Y

    else:
        posYtest1 = posY + (fy * signCos[0])  # calcul de la position Y dans le cas où on touche la frontière perpendiculaire à l'axe X
        test1 = abs(dizainePosX / cosAngle) # calcul distance jusqu'à la prochaine frontière que va toucher le rayon perpendiculaire à l'axe X
        return test1, posXtest1, posYtest1, 1  # on renvoie les valeurs dans le cas ou le rayon touche en premier une frontière perpendiculaire à l'axe X


