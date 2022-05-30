import time

import pygame
import Rayon
import globalVariable as glb
import math
import sys


def CreerListeAngleOBJ(listeObjet):
    debut = time.time()
    listeAngleOBJ = []
    minAngle = (glb.playerAngle-glb.angleRegard)%glb.pi2
    maxAngle = (glb.playerAngle+glb.angleRegard)%glb.pi2
    nb = 0
    for x in range(len(glb.statusMonstre)):
        glb.statusMonstre[x][0] = False
    for element in glb.Carte:
        if element == "2" or element == "3":
            long = 100
            if element == "2":
                posX = (nb % glb.carteSize[0]) * glb.rectSizeX + glb.rectSizeX / 2 + glb.statusPorte[nb][0]
            else:
                 posX = (nb % glb.carteSize[0]) * glb.rectSizeX + glb.rectSizeX / 2
            posY = (nb // glb.carteSize[1]) * glb.rectSizeY + glb.rectSizeY / 2
            diffX = posX - glb.playerX
            diffY = posY - glb.playerY
            angleOBJ = calculAngleObj(diffX, diffY)
            cosAngle = math.copysign(1, math.cos(angleOBJ))
            sinAngle = math.copysign(1, math.sin(angleOBJ))
            diffX1 = (posX - glb.playerX) - (long / 2 * sinAngle)
            diffX2 = (posX - glb.playerX) + (long / 2 * sinAngle)
            diffY1 = (posY - glb.playerY)
            diffY2 = (posY - glb.playerY)
            angleOBJ1 = calculAngleObj(diffX1, diffY1)
            angleOBJ2 = calculAngleObj(diffX2, diffY2)
            # if (angleOBJ1>minAngle or angleOBJ1<maxAngle) and (angleOBJ2>minAngle or angleOBJ2<maxAngle):
            pos1 = (int((glb.playerX + diffX1) * glb.minimap / glb.gameX),
                    int((glb.playerY + diffY1) * glb.minimap / glb.gameY))
            pos2 = (int((glb.playerX + diffX2) * glb.minimap / glb.gameX),
                    int((glb.playerY + diffY2) * glb.minimap / glb.gameY))
            if element == "3":
                listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),
                                      (glb.playerX + diffX2, glb.playerY + diffY2), 6, glb.statutPortal[1], long))
            elif diffY > 0:
                listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),
                                      (glb.playerX + diffX2, glb.playerY + diffY2), 2, 0, long))
            else:
                listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),
                                      (glb.playerX + diffX2, glb.playerY + diffY2), 3, 0, long))
            glb.listeRond.append(pos1)
            glb.listeRond.append(pos2)
        nb += 1
    nb = 0
    totalListeObj = listeObjet+glb.listeBall + glb.listeMonstre
    for element in totalListeObj :
        if element[0] == 4:
            long = glb.listeParametreObjet[element[0]][0] * (glb.listeImageOBJ[4][math.floor(element[3])].get_width()/glb.listeImageOBJ[4][0].get_width())
        else:
            long = glb.listeParametreObjet[element[0]][0]
        diffX = element[1] - glb.playerX
        diffY = element[2] - glb.playerY
        angleOBJ = calculAngleObj(diffX, diffY)
        distanceOBJ = math.sqrt(diffX**2+diffY**2)
        if element[0] == 0:
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

                distCarre, posRayX, posRayY, cote = Rayon.car_affine(pente, cosAngle, sinAngle, diffPiSur2, posRayX, posRayY,signCos,signSin)  # utilisation de la fonction qui va calculer où le rayon va toucher la prochaine frontière entre les carrés
                distanceRay += distCarre  # augmente la distance à laquelle se trouve le rayon du joueur par la distance entre le rayon et la prochaine frontière d'un carré qu'il touche

                colPosRay = math.floor(posRayX / glb.rectSizeX)  # calcul de la colonne à laquelle se trouve le rayon
                lignePosRay = math.floor(posRayY / glb.rectSizeY)  # calcul de la ligne à laquelle se trouve le rayon
                carre = int(lignePosRay * glb.carteSize[
                    0] + colPosRay)  # calcul du carré à laquelle se trouve le rayon grâce à sa colonne et sa ligne

                glb.listeRond.append((int(posRayX * glb.minimap / glb.gameX),
                                      int(posRayY * glb.minimap / glb.gameY)))  # ajoute un rond à la frontière pour la miniMap
                if distanceRay > distanceOBJ:
                    #glb.listeRay.append((posRayX * glb.minimap / glb.gameX, posRayY * glb.minimap / glb.gameY))  # ajoute le rayon pour la miniMap
                    glb.statusMonstre[nb - len(listeObjet) - len(glb.listeBall)][0] = True
                    break
                elif glb.Carte[carre] == "1" or (glb.Carte[carre] == "2" and glb.statusPorte[carre][1] == False) :  # si le rayon touche un mur
                    #glb.listeRay.append((posRayX * glb.minimap / glb.gameX,posRayY * glb.minimap / glb.gameY))  # ajoute le rayon pour la miniMap
                    glb.statusMonstre[nb-len(listeObjet)-len(glb.listeBall)][0] = False
                    break  # stop la boucle, car le rayon a touché un mur
        cosAngle = math.cos(angleOBJ)
        sinAngle = math.sin(angleOBJ)
        diffX1 = (element[1] - glb.playerX) - (long/2 * sinAngle)
        diffX2 = (element[1] - glb.playerX) + (long/2 * sinAngle)
        diffY1 = (element[2] - glb.playerY) + (long/2 * cosAngle)
        diffY2 = (element[2] - glb.playerY) - (long/2 * cosAngle)
        angleOBJ1 = calculAngleObj(diffX1, diffY1)
        angleOBJ2 = calculAngleObj(diffX2, diffY2)
        #if (angleOBJ1>minAngle or angleOBJ1<maxAngle) and (angleOBJ2>minAngle or angleOBJ2<maxAngle):
        pos1 = (int((glb.playerX+diffX1) * glb.minimap / glb.gameX), int((glb.playerY + diffY1 ) * glb.minimap / glb.gameY))
        pos2 = (int((glb.playerX+diffX2) * glb.minimap / glb.gameX), int((glb.playerY + diffY2) * glb.minimap / glb.gameY))
        listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),(glb.playerX + diffX2, glb.playerY + diffY2), element[0],element[3], long))
        glb.listeRond.append(pos1)
        glb.listeRond.append(pos2)
        nb += 1
    #print(listeAngleOBJ)
    return listeAngleOBJ
    #print(listeAngleOBJ)
def calculAngleObj(diffX,diffY):
    if diffX==0 :
        if diffY<0:
            angle = math.pi/2
        else :
            angle = glb.pi + math.pi/2
    elif diffX < 0 and diffY > 0:
        angle = math.atan(diffY / diffX) + glb.pi2
    elif diffX > 0:
        angle = math.atan(diffY / diffX) + glb.pi
    else:
        angle = math.atan(diffY / diffX)
    return angle


def drawOBJ(i,longRayon,angleRay,listeAngleOBJ, penteRay,posRayX, posRayY):
    penteRay = -penteRay
    nb=0
    debut = time.time()
    for element in listeAngleOBJ:
        angleMin = element[0]
        angleMax = element[1]
        if angleMin > angleMax:
            if angleRay > angleMin or angleRay < angleMax:
                saveOBJ(element, penteRay, longRayon, angleRay,i,nb)
        else :
            if angleRay > angleMin and angleRay < angleMax:
                saveOBJ(element, penteRay, longRayon, angleRay,i,nb)
        nb+=1
    glb.process3 += time.time() - debut
def saveOBJ(element,penteRay,longRayon,angleRay,i,nb) :

    if element[3][0] == element[2][0] :
        penteOBJ = (element[3][1] - element[2][1]) / (element[3][0] - element[2][0]+0.01)
    else:
        penteOBJ = (element[3][1] - element[2][1]) / (element[3][0] - element[2][0])
    departOBJ = element[2][1] - penteOBJ * element[2][0]
    departRay = glb.playerY - penteRay * glb.playerX
    intersectionX = (departRay - departOBJ) / (penteOBJ - penteRay)
    intersectionY = penteRay * intersectionX + departRay
    # print(penteOBJ,penteRay,departOBJ,departRay,intersectionX,intersectionY)
    glb.listeRond.append((int(intersectionX * glb.minimap / glb.gameX), int(intersectionY * glb.minimap / glb.gameX)))
    distanceOBJ = abs(abs(intersectionX - glb.playerX) / math.cos(angleRay))
    if distanceOBJ < longRayon:
        nbMonstre = nb - len(glb.listeObjet) - len(glb.listeBall) - glb.nbPorte - glb.nbPortal
        maxDistance = distanceOBJ
        distanceOBJ = distanceOBJ * math.cos(glb.playerAngle - angleRay)
        reduction = 1200 / distanceOBJ * glb.listeParametreObjet[element[4]][2] * glb.reductionEcran


        # Ximage = RectLarg * imgX / reduction

        posYOBJ = glb.screenY / 2 - reduction / glb.listeParametreObjet[element[4]][1]
        if posYOBJ<glb.screenY and distanceOBJ>20:

            #image = glb.listeDiffImageOBJ[element[4]][int(reduction)]
            maxImage = len(glb.listeImageOBJ[element[4]])-1
            if math.floor(element[5])>maxImage:
                image = glb.listeImageOBJ[element[4]][maxImage]
            else:
                image = glb.listeImageOBJ[element[4]][math.floor(element[5])]
            imgX = image.get_width()
            imgY = image.get_height()
            rectLargbase = math.ceil(abs(glb.listeRectLarge[i] * imgX / reduction))
            posRaySurOBJ = math.ceil(math.sqrt((intersectionX - element[2][0]) ** 2 + (intersectionY - element[2][1]) ** 2) * imgX /element[6])
            if element[4]==0 and i == glb.nbRay/2 and glb.armeStatus[2] and glb.vieMonstre[nbMonstre]>0 and distanceOBJ<glb.armeParrametre[glb.armeStatus[0]][2]:
                    glb.newSangLong = (int(reduction*2), int((reduction*2)* (glb.sangLongY/glb.sangLongX)))
                    glb.posSang = (glb.millieuX-(glb.newSangLong[0]/2),(glb.screenY-glb.newSangLong[1])/2)
                    glb.armeStatus[3] = True
                    pygame.mixer.Sound.play(glb.hitDemonSound)
                    glb.vieMonstre[nbMonstre] -= glb.armeParrametre[glb.armeStatus[0]][4]
                    print(glb.vieMonstre[nbMonstre])
                    if glb.vieMonstre[nbMonstre]<=0:
                        glb.listeMonstre[nbMonstre][3] = 0
                        glb.nbMonstreMort += 1
                        glb.lObjAnim.append(nbMonstre)

            if rectLargbase + posRaySurOBJ > imgX:
                image = image.subsurface((imgX - rectLargbase, 0, rectLargbase, imgY))
            else:
                image = image.subsurface((posRaySurOBJ, 0, rectLargbase, imgY))
            image = glb.pygame.transform.scale(image, (glb.listeRectLarge[i], abs(int(reduction))))
            # print(imageTauneau,(posRaySurOBJ, 0,RectLarg , imgY))

            glb.objet2d.append((distanceOBJ, (image, (math.floor(glb.listeRectPos[i]), posYOBJ))))
        elif element[4]==6 and glb.statutPortal[0]:
            pygame.quit()  # Si on quitte le jeu
            sys.exit()
"""def SaveObjet(ray, penteRay, distanceMur, cosAngle, sinAngle):
    for element in listeObjet:
        ray = element[0]
        distanceRay = element[1]
        RectLarg = screenX / nbRay
        reduction = 1200 / distanceRay * 30 * (screenMulti ** 2)
        imgX = tauneau.get_width()
        imgY = tauneau.get_height()
        #print(distanceRay,reduction)
        imageTauneau = pygame.transform.scale(tauneau,(reduction, reduction))
        screen.blit(imageTauneau,(RectLarg*ray,screenY/2))
    for element in glb.listeObjet :
        x = element[1]-glb.playerX
        Y=x * penteRay
        testY=x*penteRay+glb.playerY
        posObj=[element[1]-cosAngle*-10,element[2]-sinAngle*-10,element[1]+cosAngle*-10,element[2]+sinAngle*-10]
        penteObj=(posObj[2]-posObj[0])/(posObj[3]-posObj[1])
        departFObj = posObj[1] - penteObj * posObj[0]
        departFRay = glb.playerY - penteRay * glb.playerX
        IntersectionX = (departFRay - departFObj)/ (penteObj - penteRay)
        IntersectionY = penteRay*IntersectionX + departFRay
        if posObj[0]< posObj[2] :
            entrelesPoint = posObj[0] < IntersectionX < posObj[2]
        else :
            entrelesPoint = posObj[2] < IntersectionX < posObj[0]
        diffX = glb.playerX - IntersectionX
        diffY = glb.playerY - IntersectionY
        distanceObj = math.sqrt(diffX**2+diffY**2)
        if distanceObj<distanceMur and entrelesPoint :
            #x=x+playerX
            #print(playerX, playerY, x, testY, penteRay, playerAngle)
            #RectLarg = screenX*2 / nbRay
            #reduction = 1200 / distanceObj * 30 * (screenMulti ** 2)
            #imgX = tauneau.get_width()
            #imgY = tauneau.get_height()
            #print(distanceObj)
            #imageTauneau = pygame.transform.scale(tauneau, (reduction, reduction))
            #objet2d.append((imageTauneau, (RectLarg * ray, screenY / 2)))
            glb.listeRond.append((IntersectionX * glb.minimap / glb.screenX, IntersectionY * glb.minimap / glb.screenY))
"""
def drawObjet2d():

    liste = sorted(glb.objet2d,key=lambda y: y[0], reverse=True)
    for objet in liste:
            glb.screen.blit(objet[1][0],objet[1][1])

