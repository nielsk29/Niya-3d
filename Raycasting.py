import time

import pygame
from math import *
import math
import sys

screenMulti = 1
screenX = int(1200*screenMulti)
screenY = int(1200*screenMulti)
playerX = screenX/2+0.5
playerY = screenY/2+0.5
diagonal=int(sqrt(screenX**2+screenY**2))
carteSize = (12, 12)
diagCarre=int(sqrt(carteSize[0]**2 + carteSize[1]**2))
rectSizeX = screenX/carteSize[0]
rectSizeY = screenY/carteSize[1]
precision = 0.00001
pi=(math.pi // precision) * precision
playerAngle = 0
angleRegard = pi/4
pi2=pi*2
nbRay = 1200
dist3D = 0
listeRay = []
listeRond = []
         #0;2;4;6;8;10
Carte = ("111111111111"#0
         "100200000001"#1
         "101000020001"#2
         "111100001111"#3
         "100020020001"#4
         "100000011111"#5
         "111100010001"#6
         "100020020011"#7
         "101111002001"#8
         "100001021021"#9
         "100001001001"#10
         "111111111111")#11
         #;1;3;5;7;9;11
sizeMmap=20
minimap = sizeMmap*carteSize[0]
darkGrey = (120, 120, 120)
Grey = (80, 80, 80)
mapPlayerX = playerX * minimap / screenX
mapPlayerY = playerY * minimap / screenY
vitesse=12
afficherMap=False
process = 0
listeObjet = [(1, 350, 150), (1, 450, 450), (1, 450, 750), (1, 750, 250), (1, 750, 450), (1, 750, 750), (1, 750, 950), (1, 1050, 950)]
objet2d=[]
def rays(murBrique):
    global listeRay, listeRond
    listeRay, listeRond = [], []
    diffRay = (angleRegard*2 / nbRay) // precision * precision
    angleRay = (playerAngle-angleRegard) // precision * precision
    for i in range(nbRay):
        distanceRay=0
        angleRay=(angleRay +diffRay) // precision * precision
        posRayX=playerX
        posRayY=playerY
        pente = -tan(angleRay) // precision * precision
        diffPiSur2 = angleRay % (pi / 2)
        cosAngle = cos(angleRay) // precision * precision
        sinAngle = sin(angleRay) // precision * precision
        for nbCar in range(diagCarre):
            distCarre, posRayX, posRayY, cote = car_affine(pente,cosAngle,sinAngle,diffPiSur2, posRayX, posRayY)
            if cote ==False:
                pixelparpixel(angleRay,i, murBrique)
                break
            distanceRay+=distCarre

            colPosRay = floor(posRayX/rectSizeX)
            lignePosRay = floor(posRayY/rectSizeY)
            carre=int(lignePosRay*carteSize[0] + colPosRay)

            listeRond.append((posRayX * minimap / screenX, posRayY * minimap / screenY))
            if Carte[carre] == "1":
                listeRay.append((posRayX * minimap / screenX, posRayY * minimap / screenY))
                rect3d(i,angleRay,distanceRay,cote,posRayX,posRayY,murBrique)
                SaveObjet(i, pente, distanceRay, cosAngle, sinAngle)
                break
            """if Carte[carre] == "2":
                if (carre in objCarre) == False:
                    listeObjet.append((i,distanceRay))
                    objCarre.append(carre)"""

def rect3d (iray,rayAngle,nb,cote,rayX,rayY,imageMur):
    global process, objet2d
    debut=time.time()
    nb = nb * math.cos(playerAngle - rayAngle)
    RectLong = 1200/nb *100*(screenMulti**2)

    RectLarg = screenX*2/nbRay
    RectY = (screenY-RectLong)/2
    coul=abs((nb*150/2400) - 150)
    #mur = pygame.transform.scale(imageMur, (int(RectLong), int(RectLong)))

    imageSizeX = imageMur.get_width()-1
    imageSizeY = imageMur.get_height()-1

    if cote ==1:
        Ximage=int((rayY%rectSizeY)*imageSizeX/rectSizeY)

    else:
        Ximage = int((rayX % rectSizeX)*imageSizeX/rectSizeX)
    mur = imageMur.subsurface((Ximage, 0, RectLarg, imageSizeY))
    #screen.blit(mur, (600, 600))
    mur = pygame.transform.scale(mur, (int(RectLarg), int(RectLong)))
    #pygame.draw.rect(screen,Grey,(600,600,500,500))
    #screen.blit(mur, (600, 600))
    screen.blit(mur, (iray*RectLarg, RectY))
    #pygame.draw.rect(screen, (coul, coul, coul), (iray*RectLarg, RectY, RectLarg, RectLong))


def pixelparpixel(angleRay,i, murBrique):
    for nb in range(diagonal):

        posRayX = playerX - math.cos(angleRay) * nb
        posRayY = playerY - math.sin(angleRay) * nb

        colPosRay = floor(posRayX / rectSizeX)
        lignePosRay = floor(posRayY / rectSizeY)
        carre = int(lignePosRay * carteSize[0] + colPosRay)


        if Carte[carre] == "1":
            if -0.05<(posRayX%rectSizeX)<0.05:
                cote=1
            else:
                cote=2
            rect3d(i, angleRay, nb , cote, posRayX, posRayY, murBrique)
            break

def car_affine(pente,cosAngle,sinAngle,diffPiSur2,posX, posY):

    if diffPiSur2<0.0001 or diffPiSur2>(pi/2 - 0.0001 ):
        return 0,0,0,False

    def f_affine(x):
        return pente*x
    if cosAngle > 0:
        dizainePosX = posX % rectSizeX
        posXtest1 = posX - dizainePosX - 0.05

    else:
        dizainePosX = rectSizeX - posX % rectSizeX
        posXtest1 = posX + dizainePosX + 0.05
    if sinAngle < 0:
        dizainePosY = rectSizeY -posY % rectSizeY
        posYtest2=posY + dizainePosY + 0.05
    else:
        dizainePosY = posY % rectSizeY
        posYtest2 = posY - dizainePosY - 0.05
    fx = dizainePosY / pente // precision * precision
    fy = (f_affine(dizainePosX) // precision) * precision
    #print(fx,fy)
    if cosAngle*sinAngle > 0:
        if sinAngle > 0:
            posXtest2 = posX + fx -0.05
            posYtest1 = posY + fy -0.05
        else:
            posXtest2 = posX - fx +0.05
            posYtest1 = posY - fy +0.05
    else:
        if sinAngle > 0:
            posXtest2 = posX + fx +0.05
            posYtest1 = posY - fy -0.05
        else:
            posXtest2 = posX - fx -0.05

            posYtest1 = posY + fy +0.05


    test1=sqrt(fy**2 + dizainePosX**2)
    test2=sqrt(fx**2 + dizainePosY**2)
    if test1<test2:
        return test1,posXtest1, posYtest1,1
    else:
        return test2, posXtest2, posYtest2,2

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
    for element in listeObjet :
        x = element[1]-playerX
        Y=x * penteRay
        testY=x*penteRay+playerY
        posObj=[element[1]-cosAngle*-10,element[2]-sinAngle*-10,element[1]+cosAngle*-10,element[2]+sinAngle*-10]
        penteObj=(posObj[2]-posObj[0])/(posObj[3]-posObj[1])
        departFObj = posObj[1] - penteObj * posObj[0]
        departFRay = playerY - penteRay * playerX
        IntersectionX = (departFRay - departFObj)/ (penteObj - penteRay)
        IntersectionY = penteRay*IntersectionX + departFRay
        if posObj[0]< posObj[2] :
            entrelesPoint = posObj[0] < IntersectionX < posObj[2]
        else :
            entrelesPoint = posObj[2] < IntersectionX < posObj[0]
        diffX = playerX - IntersectionX
        diffY = playerY - IntersectionY
        distanceObj = sqrt(diffX**2+diffY**2)
        if distanceObj<distanceMur and entrelesPoint :
            #x=x+playerX
            #print(playerX, playerY, x, testY, penteRay, playerAngle)
            #RectLarg = screenX*2 / nbRay
            #reduction = 1200 / distanceObj * 30 * (screenMulti ** 2)
            #imgX = tauneau.get_width()
            #imgY = tauneau.get_height()
            print(distanceObj)
            #imageTauneau = pygame.transform.scale(tauneau, (reduction, reduction))
            #objet2d.append((imageTauneau, (RectLarg * ray, screenY / 2)))
            listeRond.append((IntersectionX * minimap / screenX, IntersectionY * minimap / screenY))
def drawMap2D(sizeX,sizeY):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, sizeX *carteSize[1], sizeY * carteSize[0]))
    for y in range(carteSize[0]):
        for x in range(carteSize[1]):
            rect = y*carteSize[0]+x
            rectX = x * sizeX
            rectY = y * sizeY
            if Carte[rect] == '1':
                pygame.draw.rect(screen, Grey, pygame.Rect(rectX, rectY, sizeX-1, sizeY-1))
            elif Carte[rect] == '2':
                pygame.draw.rect(screen, (0,0,255), pygame.Rect(rectX, rectY, sizeX - 1, sizeY - 1))
            else:
                pygame.draw.rect(screen, darkGrey, pygame.Rect(rectX, rectY, sizeX-1, sizeY-1))
    for x in range(nbRay-1):
        pygame.draw.line(screen, (255, 1, 0), (mapPlayerX, mapPlayerY),listeRay[x], 1)
    for rond in listeRond:
        pygame.draw.circle(screen, (0, 255, 0), rond, 2)
        #pygame.draw.line(screen, (255, 0, 255), rond, (rond[0]+cos(playerAngle+pi/2)*10,rond[1]+sin(playerAngle+pi/2)*10), 1)
        #pygame.draw.line(screen, (0, 255, 255), rond, (rond[0] - cos(playerAngle+pi/2) * 10, rond[1] - sin(playerAngle+pi/2) * 10), 1)
def drawObjet2d(listeObjet):
    for objet in listeObjet:
            screen.blit(objet[0],objet[1])
def player(size):


    pygame.draw.circle(screen, (255, 0, 0), (int(mapPlayerX), int(mapPlayerY)), 2)
    pygame.draw.line(screen, (0, 0, 255), (mapPlayerX, mapPlayerY), (mapPlayerX - math.cos(playerAngle) * 10, mapPlayerY - math.sin(playerAngle) * 10), 1)
    pygame.draw.line(screen, (0, 255, 255), (mapPlayerX, mapPlayerY), (mapPlayerX - math.cos(playerAngle - angleRegard) * 10, mapPlayerY - math.sin(playerAngle - angleRegard) * 10), 1)
    pygame.draw.line(screen, (0, 0, 255), (mapPlayerX, mapPlayerY), (mapPlayerX - math.cos(playerAngle + angleRegard) * 10, mapPlayerY - math.sin(playerAngle + angleRegard) * 10), 1)


def f_all(murBrique):
    global process, objet2d
    debut=time.time()
    pygame.draw.rect(screen, Grey, (0, 0, screenX*2, screenY / 2))
    pygame.draw.rect(screen, darkGrey, (0, screenY / 2, screenX*2, screenY / 2))
    rays(murBrique)
    #objet(listeObjet)
    #drawObjet2d(objet2d)
    objet2d=[]
    if afficherMap:
        drawMap2D(sizeMmap,sizeMmap)
        player(sizeMmap)
    process = time.time() - debut
    textAngle = font.render(str(int(1/process)), True,(0,0,0))
    screen.blit(textAngle,(10,30))


pygame.init()
screen = pygame.display.set_mode((screenX*2,screenY))
murBrique = pygame.image.load("wall_bricks.jpg")
tauneau = pygame.image.load("tauneau.png")

font = pygame.font.SysFont('freesansbold.ttf', 90)
temps = pygame.time.Clock()
f_all(murBrique)
while True:
    f_all(murBrique)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        playerAngle = (playerAngle+0.1)%pi2
    if keys[pygame.K_q]:
        playerAngle = (playerAngle-0.1)%pi2
    if keys[pygame.K_s]:
        playerCol = int((playerX + math.cos(playerAngle) * vitesse*3) / rectSizeX)
        playerLigne = int((playerY + math.sin(playerAngle) * vitesse*3) / rectSizeY)
        playerCarre = playerLigne * carteSize[0] + playerCol
        if Carte[playerCarre] != "1":
            playerX += math.cos(playerAngle) * vitesse
            playerY += math.sin(playerAngle) * vitesse
    if keys[pygame.K_z] :
        playerCol=int((playerX-math.cos(playerAngle) * vitesse*3)/rectSizeX)
        playerLigne=int((playerY-math.sin(playerAngle) * vitesse*3)/rectSizeY)
        playerCarre=playerLigne*carteSize[0] + playerCol
        if Carte[playerCarre]!="1":
            playerX -= math.cos(playerAngle) * vitesse
            playerY -= math.sin(playerAngle) * vitesse
    if keys[pygame.K_TAB]:
        if afficherMap:
            afficherMap=False
        else:
            afficherMap=True
    mapPlayerX = playerX * minimap / screenX
    mapPlayerY = playerY * minimap / screenY
    pygame.display.flip()
    temps.tick(30)

