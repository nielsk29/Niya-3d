import globalVariable as glb
import math



def CreerListeAngleOBJ(listeObjet):
    listeAngleOBJ = []
    minAngle = (glb.playerAngle-glb.angleRegard)%glb.pi2
    maxAngle = (glb.playerAngle+glb.angleRegard)%glb.pi2
    nb = 0
    for element in listeObjet :
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
        if minAngle>maxAngle:
            #if (angleOBJ1>minAngle or angleOBJ1<maxAngle) and (angleOBJ2>minAngle or angleOBJ2<maxAngle):
            pos1 = ((glb.playerX+diffX1) * glb.minimap / glb.screenX, (glb.playerY + diffY1 ) * glb.minimap / glb.screenY)
            pos2 = ((glb.playerX+diffX2) * glb.minimap / glb.screenX, (glb.playerY + diffY2) * glb.minimap / glb.screenY)
            listeAngleOBJ.append((angleOBJ1,angleOBJ2, (glb.playerX + diffX1,glb.playerY + diffY1),(glb.playerX + diffX2,glb.playerY + diffY2),element[0]))
            glb.listeRond.append(pos1)
            glb.listeRond.append(pos2)
        else:
            #if(angleOBJ1>minAngle and angleOBJ1<maxAngle) and (angleOBJ2>minAngle and angleOBJ2<maxAngle):
            pos1 = ((glb.playerX + diffX1) * glb.minimap / glb.screenX, (glb.playerY + diffY1) * glb.minimap / glb.screenY)
            pos2 = ((glb.playerX + diffX2) * glb.minimap / glb.screenX, (glb.playerY + diffY2) * glb.minimap / glb.screenY)
            listeAngleOBJ.append((angleOBJ1, angleOBJ2, (glb.playerX + diffX1,glb.playerY + diffY1),(glb.playerX + diffX2,glb.playerY + diffY2),element[0]))
            glb.listeRond.append(pos1)
            glb.listeRond.append(pos2)
        nb += 1
    #print(listeAngleOBJ)
    return listeAngleOBJ
    #print(listeAngleOBJ)
def calculAngleObj(diffX,diffY):
    if diffX < 0 and diffY > 0:
        angle = math.atan(diffY / diffX) + glb.pi2
    elif diffX > 0:
        angle = math.atan(diffY / diffX) + glb.pi
    else:
        angle = math.atan(diffY / diffX)
    return angle


def drawOBJ(i,longRayon,angleRay,listeAngleOBJ, penteRay,posRayX, posRayY):
    penteRay = -penteRay
    for element in listeAngleOBJ:
        angleMin = element[0]
        angleMax = element[1]
        if angleMin > angleMax:
            if angleRay > angleMin or angleRay < angleMax:
                saveOBJ(element, penteRay, longRayon, angleRay,i)
        else :
            if angleRay > angleMin and angleRay < angleMax:
                saveOBJ(element, penteRay, longRayon, angleRay,i)


def saveOBJ(element,penteRay,longRayon,angleRay,i) :
    penteOBJ = (element[3][1] - element[2][1]) / (element[3][0] - element[2][0])
    departOBJ = element[2][1] - penteOBJ * element[2][0]
    departRay = glb.playerY - penteRay * glb.playerX
    intersectionX = (departRay - departOBJ) / (penteOBJ - penteRay)
    intersectionY = penteRay * intersectionX + departRay
    # print(penteOBJ,penteRay,departOBJ,departRay,intersectionX,intersectionY)
    glb.listeRond.append((intersectionX * glb.minimap / glb.screenX, intersectionY * glb.minimap / glb.screenX))
    RectLarg = glb.screenX * 2 / glb.nbRay
    distanceOBJ = abs(abs(intersectionX - glb.playerX) / math.cos(angleRay))
    if distanceOBJ < longRayon:
        maxDistance = distanceOBJ
        reduction = 1200 / distanceOBJ * 100 * (glb.screenMulti ** 2)
        imgX = glb.tauneau.get_width()
        imgY = glb.tauneau.get_height()
        posRaySurOBJ = math.ceil(
            math.sqrt((intersectionX - element[2][0]) ** 2 + (intersectionY - element[2][1]) ** 2) * imgX /
            glb.listeParametreObjet[element[4]][0])
        # Ximage = RectLarg * imgX / reduction
        rectLargbase = math.ceil(abs(RectLarg * imgX / reduction))
        posYOBJ = glb.screenY / 2 - reduction / glb.listeParametreObjet[element[4]][1]
        if rectLargbase + posRaySurOBJ > imgX:
            imageTauneau = glb.tauneau.subsurface((imgX - rectLargbase, 0, rectLargbase, imgY))
        else:
            imageTauneau = glb.tauneau.subsurface((posRaySurOBJ, 0, rectLargbase, imgY))
        imageTauneau = glb.pygame.transform.scale(imageTauneau, (abs(RectLarg), abs(reduction)))
        # print(imageTauneau,(posRaySurOBJ, 0,RectLarg , imgY))

        glb.objet2d.append((distanceOBJ, (imageTauneau, (RectLarg * i, posYOBJ))))
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
            print(objet[0],objet[1])
            glb.screen.blit(objet[1][0],objet[1][1])
