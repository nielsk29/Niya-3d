import globalVariable as glb
import math

def SaveObjet(ray, penteRay, distanceMur, cosAngle, sinAngle):
    """for element in listeObjet:
        ray = element[0]
        distanceRay = element[1]
        RectLarg = screenX / nbRay
        reduction = 1200 / distanceRay * 30 * (screenMulti ** 2)
        imgX = tauneau.get_width()
        imgY = tauneau.get_height()
        #print(distanceRay,reduction)
        imageTauneau = pygame.transform.scale(tauneau,(reduction, reduction))
        screen.blit(imageTauneau,(RectLarg*ray,screenY/2))"""
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

def drawObjet2d(listeObjet):
    for objet in listeObjet:
            glb.screen.blit(objet[0],objet[1])
