import time
import pygame
import IA_Rayon
import IA_globalVariable as glb
import math
import sys


def CreerListeAngleOBJ(listeObjet):
    listeAngleOBJ = [] # liste des angles min et max à avoir pour les avoir dans nottre angle des vision pour tous les objets
    nb = 0  # indice de l'objet ou monstre

    for element in glb.Carte:  # boucle qui va faire les angles pour les portes et le portail car ils ont une oriantation fixe
        if element == "2" or element == "3":
            long = glb.rectSizeX  # ils font la taille d'un carreau
            if element == "2":   # si c'est une porte on change sa position X en fonction si on l'ouvre ou pas
                posX = (nb % glb.carteSize[0]) * glb.rectSizeX + glb.rectSizeX / 2 + glb.statusPorte[nb][0]
            else:
                 posX = (nb % glb.carteSize[0]) * glb.rectSizeX + glb.rectSizeX / 2  # calcul pos X
            posY = (nb // glb.carteSize[0]) * glb.rectSizeY + glb.rectSizeY / 2  # calcul pos Y
            diffX = posX - glb.playerX  # différence X entre le joueur et l'objet
            diffY = posY - glb.playerY  # différence Y entre le joueur et l'objet
            angleOBJ = glb.a_port   # calcul de l'angle entre le joueur est l'objet

            """sinAngle = math.copysign(1, math.sin(angleOBJ))  # -1 ou 1 en fonction du signe du sinus de l'angle
            diffX1 = (posX - glb.playerX) - (long / 2 * sinAngle)  # calcul pos X min
            diffX2 = (posX - glb.playerX) + (long / 2 * sinAngle)  # calcul pos X max
            diffY1 = (posY - glb.playerY)  # calcul pos Y min
            diffY2 = (posY - glb.playerY)  # calcul pos Y max"""
            cosAngle = math.cos(angleOBJ)  # cosinus de l'angle pour bien orienté le monstre
            sinAngle = math.sin(angleOBJ)  # sinus de l'angle pour bien orienté le monstre
            diffX1 = (posX - glb.playerX) - (long / 2 * sinAngle)  # calcul pos X min
            diffX2 = (posX - glb.playerX) + (long / 2 * sinAngle)  # calcul pos X max
            diffY1 = (posY - glb.playerY) + (long / 2 * cosAngle)  # calcul pos Y min
            diffY2 = (posY - glb.playerY) - (long / 2 * cosAngle)  # calcul pos Y max
            angleOBJ1 = calculAngleObj(diffX1, diffY1) # angle entre le joueur et la pos min de l'objet
            angleOBJ2 = calculAngleObj(diffX2, diffY2) # angle entre le joueur et la pos max de l'objet
            angleMilieu = calculAngleObj(diffX, diffY)
            pos1 = (int((glb.playerX + diffX1) * glb.minimap[0] / glb.gameX),
                    int((glb.playerY + diffY1) * glb.minimap[1] / glb.gameY))  # position pour minimap
            pos2 = (int((glb.playerX + diffX2) * glb.minimap[0] / glb.gameX),
                    int((glb.playerY + diffY2) * glb.minimap[1] / glb.gameY))
            if element == "3": # si c'est un portail
                listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),
                                      (glb.playerX + diffX2, glb.playerY + diffY2), 6, glb.statutPortal[1], long,angleMilieu))
                # on ajoute à la liste: (angleMin, angleMax, posMin, posMax, indice image objet, frame, longueur)
            elif diffY > 0: # si on est devant la porte on met l'image normale
                listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),
                                      (glb.playerX + diffX2, glb.playerY + diffY2), 2, 0, long,angleMilieu))
                # on ajoute à la liste: (angleMin, angleMax, posMin, posMax, indice image objet, frame, longueur)
            else:  # si on est derriere la porte on met l'image inversée
                listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),
                                      (glb.playerX + diffX2, glb.playerY + diffY2), 3, 0, long,angleMilieu))
                # on ajoute à la liste: (angleMin, angleMax, posMin, posMax, indice image objet, frame, longueur)
            glb.listeRond.append((pos1,(0,255,0))) # ajout rond pour minimap
            glb.listeRond.append((pos2,(0,255,0))) # ajout rond pour mini map
        nb += 1
    nb = 0
    totalListeObj = listeObjet+glb.listeBall + glb.listeMonstre  # liste de tout les objet qui sont toujours dans nottre direction
    for element in totalListeObj : # parcourt la liste des objet
        if element[0] == 4: # si c'est une rocket il faut mettre sa longueur en fonction de la taille de l'image utilisée
            long = glb.listeParametreObjet[element[0]][0] * (glb.listeImageOBJ[4][math.floor(element[3])].get_width()/glb.listeImageOBJ[4][0].get_width())
        else:
            long = glb.listeParametreObjet[element[0]][0]  # on met la longueur à celle dans les paramètres des objets
        diffX = element[1] - glb.playerX  # différence X entre le joueur et l'objet
        diffY = element[2] - glb.playerY  # différence Y entre le joueur et l'objet
        if element[0] == 0:
            angleOBJ = glb.statusMonstre[nb - len(listeObjet) - len(glb.listeBall)][8]
        else:
            angleOBJ = calculAngleObj(diffX, diffY)  # calcul de l'angle entre le joueur est l'objet
        distanceOBJ = math.sqrt(diffX**2+diffY**2)  # calcul de la distance avec l'objet
        if element[0] == 0: # si c'est un monstre on envoie un rayon vers sa direction pour savoir si on est dans son chant de vision
            distanceRay = 0  # variable qui contient la distance entre le joueur et la position du rayon
            posRayX = glb.playerX  # initialisation de la position X du rayon à la position du joueur
            posRayY = glb.playerY  # initialisation de la position Y du rayon à la position du joueur
            pente = -math.tan(angleOBJ)  # calcul de la pente du rayon comme une fonction affine
            diffPiSur2 = angleOBJ % (glb.pi / 2)  # différence entre l'angle du rayon et pi sur 2 pour savoir si la pente va être trops grande pour les calculs
            cosAngle = math.cos(angleOBJ)  # calcul du cosinus de l'angle du rayon
            sinAngle = math.sin(angleOBJ)  # calcul du sinus de l'angle du rayon
            signCos = (math.copysign(1, cosAngle), cosAngle < 0)
            signSin = (math.copysign(1, sinAngle), sinAngle < 0)
            for nbCar in range(glb.diagCarre):  # boucle qui va envoyé le rayon à la prochaine frontière entre les carrés donc le nombre maximal de cette boucle est le diagonal de la carte

                distCarre, posRayX, posRayY, cote = IA_Rayon.car_affine(pente, cosAngle, sinAngle, diffPiSur2, posRayX, posRayY,signCos,signSin)  # utilisation de la fonction qui va calculer où le Rayon va toucher la prochaine frontière entre les carrés
                distanceRay += distCarre  # augmente la distance à laquelle se trouve le Rayon du joueur par la distance entre le Rayon et la prochaine frontière d'un carré qu'il touche

                colPosRay = math.floor(posRayX / glb.rectSizeX)  # calcul de la colonne à laquelle se trouve le rayon
                lignePosRay = math.floor(posRayY / glb.rectSizeY)  # calcul de la ligne à laquelle se trouve le rayon
                carre = int(lignePosRay * glb.carteSize[0] + colPosRay)  # calcul du carré à laquelle se trouve le rayon grâce à sa colonne et sa ligne


                glb.listeRond.append(((int(posRayX * glb.minimap[0] / glb.gameX),
                                      int(posRayY * glb.minimap[1] / glb.gameY)),(0,0,255)))  # ajoute un rond à la frontière pour la miniMap

                if distanceRay > distanceOBJ: # si le rayon est plus grand que la distance entre le joueur et le monstre alors on est dans son chant de vision
                    glb.statusMonstre[nb - len(listeObjet) - len(glb.listeBall)][0] = True  # on met dans son status un True
                    break
                elif glb.Carte[carre] == "1" or (glb.Carte[carre] == "2" and glb.statusPorte[carre][1] == False) :  # si le rayon touche un mur alors on est pas dans son chant de vision
                    glb.statusMonstre[nb-len(listeObjet)-len(glb.listeBall)][0] = False
                    break  # stop la boucle, car le rayon a touché un mur
            if glb.v_2d:
                glb.listeRay.append(((element[1]* glb.minimap[0] / glb.gameX,element[2]* glb.minimap[1] / glb.gameY),(glb.mapPlayerX, glb.mapPlayerY)))

        cosAngle = math.cos(angleOBJ)  # cosinus de l'angle pour bien orienté le monstre
        sinAngle = math.sin(angleOBJ)   # sinus de l'angle pour bien orienté le monstre
        diffX1 = (element[1] - glb.playerX) - (long/2 * sinAngle)  # calcul pos X min
        diffX2 = (element[1] - glb.playerX) + (long/2 * sinAngle)  # calcul pos X max
        diffY1 = (element[2] - glb.playerY) + (long/2 * cosAngle)  # calcul pos Y min
        diffY2 = (element[2] - glb.playerY) - (long/2 * cosAngle)  # calcul pos Y max
        angleOBJ1 = calculAngleObj(diffX1, diffY1)  # angle entre le joueur et la pos min de l'objet
        angleOBJ2 = calculAngleObj(diffX2, diffY2)  # angle entre le joueur et la pos max de l'objet
        pos1 = (int((glb.playerX+diffX1) * glb.minimap[0] / glb.gameX), int((glb.playerY + diffY1 ) * glb.minimap[1] / glb.gameY))  # position pour minimap
        pos2 = (int((glb.playerX+diffX2) * glb.minimap[0] / glb.gameX), int((glb.playerY + diffY2) * glb.minimap[1] / glb.gameY))  # position pour minimap

        listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),(glb.playerX + diffX2, glb.playerY + diffY2), element[0],element[3], long,angleOBJ))
        # on ajoute à la liste: (angleMin, angleMax, posMin, posMax, indice image objet, frame, longueur)

        glb.listeRond.append((pos1,(255,0,0)))
        glb.listeRond.append((pos2,(255,0,0)))

        nb += 1
    #glb.statusMonstre[0][8] = angleOBJ
    return listeAngleOBJ


# fonction qui calcul un angle entre 2 point avec la différence X et la différence Y
def calculAngleObj(diffX,diffY):
    if diffX==0 :  # si les 2 point sont sur le même X alors l'angle est soit pi/2 ou 3pi/2 car la tangente sera infini
        if diffY<0:
            angle = math.pi/2
        else :
            angle = glb.pi + math.pi/2
    elif diffX < 0 and diffY > 0:  # si on est dans ce cas-là la tangente sera négative donc on rajoute 2*pi
        angle = math.atan(diffY / diffX) + glb.pi2
    elif diffX > 0:  # si on est dans ce cas-là la tangente sera la même que celui de l'angle - pi donc on rajoute + pi
        angle = math.atan(diffY / diffX) + glb.pi
    else:
        angle = math.atan(diffY / diffX)  # on calcule la tangente avec opposé / adjacent puis on fait arcTan pour avoir l'angle
    return angle


def OBJ(i,longRayon,angleRay,listeAngleOBJ, penteRay,posRayX, posRayY):
    penteRay = -penteRay  # on inverse la pente car le point 0,0 est en haut à gauche
    nb=0
    for element in listeAngleOBJ:  # on parcourt la liste des angles de tous les objets
        angleMin = element[0]
        angleMax = element[1]
        if angleMin > angleMax: # si dans le cas ou l'angle min et plus grand que l'angle max alors on est dans le cas où entre les 2 angle il y a 0 en radiant
            if angleMin>element[7]>angleMax:
                if (angleRay < angleMin and angleRay > angleMax) :  # donc on verifie si le rayon touche l'objet avec un or car 0<angle < 2pi
                        drawOBJ(element, penteRay, longRayon, angleRay,i,nb)  # on dessine l'objet
            else:
                if (angleRay > angleMin or angleRay < angleMax) :  # donc on verifie si le rayon touche l'objet avec un or car 0<angle < 2pi
                    drawOBJ(element, penteRay, longRayon, angleRay,i,nb)  # on dessine l'objet
        else :
            if angleRay > angleMin and angleRay < angleMax:  # on verifie si le rayon touche l'objet avec un and
                drawOBJ(element, penteRay, longRayon, angleRay,i,nb)  # on dessine l'objet
        nb+=1
def drawOBJ(element,penteRay,longRayon,angleRay,i,nb) :

    if element[3][0] == element[2][0] : # dans ce cas la sa ferait une division par 0 donc crash
        penteOBJ = (element[3][1] - element[2][1]) / 0.01  # on rajoute 0.01 pour faire une division qui corespond à peut près
    else:
        penteOBJ = (element[3][1] - element[2][1]) / (element[3][0] - element[2][0])  # calcul de la pente de l'objet
    departOBJ = element[2][1] - penteOBJ * element[2][0]  # calcul du départ de la fonction de l'objet donc quand le x=0
    departRay = glb.playerY - penteRay * glb.playerX  # calcul du départ de la fonction du rayon donc quand le x = 0
    intersectionX = (departRay - departOBJ) / (penteOBJ - penteRay)  # calcul de la pos X de l'intersection entre les deux fonction
    intersectionY = penteRay * intersectionX + departRay  # calcul de la pos Y de l'intersection entre les deux fonction

    glb.listeRond.append(((int(intersectionX * glb.minimap[0] / glb.gameX), int(intersectionY * glb.minimap[1] / glb.gameY)),(0,255,0)))

    distanceOBJ = abs(abs(intersectionX - glb.playerX) / math.cos(angleRay))  # calcul la distance entre le joueur est l'intersection
    if distanceOBJ < longRayon : # si la distance est plus petite que la longueur du rayon donc la disatnce jusqu'au mur alors on dessine sur l'écran le rectangle de l'objet
        nbMonstre = nb - len(glb.listeObjet) - len(glb.listeBall) - glb.nbPorte - glb.nbPortal  # indice dans la liste des monstres
        distanceOBJ = distanceOBJ * math.cos(glb.playerAngle - angleRay)  # enlève le fisheye
        reduction = 1200 / distanceOBJ * glb.listeParametreObjet[element[4]][2] * glb.reductionEcran # calcul longueur sur l'écran du rectangle
        posYOBJ = glb.screenY / 2 - reduction / glb.listeParametreObjet[element[4]][1]  # calcul la pos Y du rectangle sur l'écran
        if posYOBJ<glb.screenY and distanceOBJ>20:  # verifie que le rectangle s'affiche bien sur l'écran et qu'on est pas trops proche de l'objet

            maxImage = len(glb.listeImageOBJ[element[4]])-1  # prend la frame maximum de cette image pour ne pas aller au deçu
            if math.floor(element[5])>maxImage:  # regarde si la frame qu'on veut est n'existe pas
                image = glb.listeImageOBJ[element[4]][maxImage]  # alors on met la dernière frame possible
            else:
                image = glb.listeImageOBJ[element[4]][math.floor(element[5])]  # prend la frame qu'on veut
            imgX = image.get_width()  # calcul taille X image
            imgY = image.get_height()  # calcul taille Y image
            rectLargbase = math.ceil(abs(glb.listeRectLarge[i] * imgX / reduction))  # calcul la largeur qu'on veut dans l'image de base
            posRaySurOBJ = math.ceil(math.sqrt((intersectionX - element[2][0]) ** 2 + (intersectionY - element[2][1]) ** 2) * imgX /element[6])  # calcul de la pos sur l'image de base à laquelle on va prend une partie
            if element[4]==0 and i == glb.nbRay/2 and glb.armeStatus[2] and glb.vieMonstre[nbMonstre]>0 and distanceOBJ<glb.armeParrametre[glb.armeStatus[0]][2]:  # si on a tiré sur un monstre
                    glb.newSangLong = (int(reduction*2), int((reduction*2)* (glb.sangLongY/glb.sangLongX)))  # calcul la longueur du sang en fonction de la taille du monstre
                    glb.posSang = (glb.millieuX-(glb.newSangLong[0]/2),(glb.screenY-glb.newSangLong[1])/2)  # calcul pos sang
                    glb.armeStatus[3] = True  # True car on a touché un enemies
                    pygame.mixer.Sound.play(glb.hitDemonSound)  # joue le son du monstre
                    glb.vieMonstre[nbMonstre] -= glb.armeParrametre[glb.armeStatus[0]][4]  # enleve à la vie du monstre les dégat que met l'arme
                    if glb.vieMonstre[nbMonstre]<=0:  # si la vie du monstre < 0 donc qu'il meurt
                        glb.listeMonstre[nbMonstre][3] = 0
                        glb.nbMonstreMort += 1  # ajout 1 monstre mort
                        glb.lObjAnim.append(nbMonstre)  # ajoute à la liste des objets à animé le monstre

            if rectLargbase + posRaySurOBJ > imgX:  # cas où on serai au bout de l'image ce qui pourait faire une erreur
                image = image.subsurface((imgX - rectLargbase, 0, rectLargbase, imgY))  # on coupe l'image au dernier rectangle de cette taille posssible
            else:
                image = image.subsurface((posRaySurOBJ, 0, rectLargbase, imgY))  # on coupe l'image avec les valleurs calculé
            image = glb.pygame.transform.scale(image, (glb.listeRectLarge[i], abs(int(reduction))))  # on change la taille de l'image à la taille qu'on a calculé

            glb.objet2d.append((distanceOBJ, (image, (math.floor(glb.listeRectPos[i]), posYOBJ))))  # ajoute à une liste des objets l'image et la distance de l'objet et le joueur pour pouvoir dabord affiché les objet les plus loin
        elif element[4]==6 and glb.statutPortal[0]:  # si on est plus proche de 20 pixel de l'objet et que c'est un portail et qu'il est actif alors il faut quitté le jeu parce qu'on a réussi
            pygame.quit()  # Si on quitte le jeu
            sys.exit()


def drawObjet2d():

    liste = sorted(glb.objet2d,key=lambda y: y[0], reverse=True)  # tri la liste en fonction de la distance avec les plus grandes distances en 1er
    for objet in liste:
            glb.screen.blit(objet[1][0],objet[1][1])  # on affiche chaque rectangle des objets



