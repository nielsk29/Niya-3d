import time

import pygame

import globalVariable as glb
import math



def CreerListeAngleOBJ(listeObjet):
    debut = time.time()
    listeAngleOBJ = []
    minAngle = (glb.playerAngle-glb.angleRegard)%glb.pi2
    maxAngle = (glb.playerAngle+glb.angleRegard)%glb.pi2
    nb = 0
    for element in glb.Carte:
        if element == "2":
            long = 100
            posX = (nb % glb.carteSize[0]) * glb.rectSizeX + glb.rectSizeX / 2 + glb.statusPorte[nb][0]
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
            if diffY > 0:
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
        if angleOBJ1<angleOBJ2:
            listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1, glb.playerY + diffY1),(glb.playerX + diffX2, glb.playerY + diffY2), element[0],element[3], long))
        else:
            listeAngleOBJ.append((angleOBJ1,angleOBJ2, (glb.playerX + diffX1,glb.playerY + diffY1),(glb.playerX + diffX2,glb.playerY + diffY2),element[0],element[3], long))
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
        nbMonstre = nb - len(glb.listeObjet) - len(glb.listeBall) - glb.nbPorte
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
            rectLargbase = math.ceil(abs(glb.RectLarg * imgX / reduction))
            posRaySurOBJ = math.ceil(math.sqrt((intersectionX - element[2][0]) ** 2 + (intersectionY - element[2][1]) ** 2) * imgX /element[6])
            if element[4]==0:
                glb.statusMonstre[nbMonstre][0] = True
                if (glb.millieuX-glb.RectLarg)<(glb.RectLarg * i)<(glb.millieuX+glb.RectLarg) and glb.shoot and glb.vieMonstre[nbMonstre]>0:
                    glb.newSangLong = (int(reduction*2), int((reduction*2)* (glb.sangLongY/glb.sangLongX)))
                    glb.posSang = (glb.millieuX-(glb.newSangLong[0]/2),(glb.screenY-glb.newSangLong[1])/2)
                    glb.toucher = True
                    pygame.mixer.Sound.play(glb.hitDemonSound)
                    glb.vieMonstre[nbMonstre] -= 10
                    if glb.vieMonstre[nbMonstre]<=0:
                        glb.listeMonstre[nbMonstre][3] = 0
                        glb.lObjAnim.append(nbMonstre)

            if rectLargbase + posRaySurOBJ > imgX:
                image = image.subsurface((imgX - rectLargbase, 0, rectLargbase, imgY))
            else:
                image = image.subsurface((posRaySurOBJ, 0, rectLargbase, imgY))
            image = glb.pygame.transform.scale(image, (abs(glb.RectLarg), abs(int(reduction))))
            # print(imageTauneau,(posRaySurOBJ, 0,RectLarg , imgY))

            glb.objet2d.append((distanceOBJ, (image, (glb.RectLarg * i, posYOBJ))))

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
    debut = time.time()
    liste = sorted(glb.objet2d,key=lambda y: y[0], reverse=True)
    for objet in liste:
            glb.screen.blit(objet[1][0],objet[1][1])

