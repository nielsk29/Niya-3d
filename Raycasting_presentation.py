import time

import pygame
from math import *
import math
import sys

screenX = 1200
screenY = 1200
playerX = screenX/2 +20.05
playerY = screenY/2 +20.05
diagonal=int(sqrt(screenX**2+screenY**2))
carteSize = (12, 12)
diagCarre=int(sqrt(carteSize[0]**2 + carteSize[1]**2))
rectSize = screenX/carteSize[0]
precision = 0.00001
pi=(math.pi // precision) * precision
playerAngle = 0
angleRegard = pi/6
pi2=pi*2
nbRay = 300
dist3D = 0

Carte = ("111111111111"
         "100000000001"
         "101000000001"
         "111100001111"
         "100000000001"
         "100000011111"
         "111100010001"
         "100000000011"
         "101111000001"
         "100001001001"
         "100001001001"
         "111111111111")
darkGrey = (100, 100, 100)
Grey = (150, 150, 150)
def draw2D():
    for y in range(carteSize[0]):
        for x in range(carteSize[1]):
            rect = y*carteSize[0]+x
            rectX = x * rectSize
            rectY = y * rectSize
            if Carte[rect] == '1':
                pygame.draw.rect(screen, Grey, pygame.Rect(rectX, rectY, rectSize-2, rectSize-2))
            else:
                pygame.draw.rect(screen, darkGrey, pygame.Rect(rectX, rectY, rectSize - 2, rectSize - 2))



def player():
    pygame.draw.circle(screen, (255, 0, 0), (int(playerX), int(playerY)), 10)
    pygame.draw.line(screen, (0, 0, 255), (playerX, playerY), (playerX - math.cos(playerAngle) * 50, playerY - math.sin(playerAngle) * 50), 4)
    pygame.draw.line(screen, (0, 255, 255), (playerX, playerY), (playerX - math.cos(playerAngle - angleRegard) * 50, playerY - math.sin(playerAngle - angleRegard) * 50), 4)
    pygame.draw.line(screen, (0, 0, 255), (playerX, playerY), (playerX - math.cos(playerAngle + angleRegard) * 50, playerY - math.sin(playerAngle + angleRegard) * 50), 4)


def rays():
    diffRay = (angleRegard*2 / nbRay) // precision * precision
    angleRay = (playerAngle-angleRegard) // precision * precision
    for i in range(nbRay):
        #print(i)
        distanceRay=0
        angleRay=(angleRay +diffRay) // precision * precision
        posRayX=playerX
        posRayY=playerY
        pente = tan(angleRay) // precision * -precision
        diffPiSur2 = angleRay % (pi / 2)
        cosAngle = cos(angleRay) // precision * precision
        sinAngle = sin(angleRay) // precision * precision
        debut=time.time()
        if cosAngle>0:
            signeCos=1
        else:
            signeCos=-1
        if sinAngle>0:
            signeSin=1
        else:
            signeSin=-1
        for nbCar in range(diagCarre):
            distCarre, posRayX, posRayY, n = car_affine(pente,cosAngle,sinAngle,signeCos,signeSin,diffPiSur2, posRayX, posRayY)
            if n ==False:
                pixelparpixel(angleRay,i)
                break
            distanceRay+=distCarre

            colPosRay = floor(posRayX/rectSize)
            lignePosRay = floor(posRayY/rectSize)
            carre=int(lignePosRay*carteSize[0] + colPosRay)
            #print(i,angleRay,(distCarre,posRayX,posRayY),n)
            #pygame.draw.circle(screen, (0, 255, 0), (int(posRayX), int(posRayY)), 2)

            if Carte[carre] == "1":
                #print(i,math.cos(angleRay), carre, (colPosRay, lignePosRay), (posRayX, posRayY))
                #print(carre,Carte[carre])
                #print(i,angleRay,posRayX, posRayY)
                rect3d(i,angleRay,distanceRay)
                pygame.draw.line(screen, (255, 1, 0), (playerX, playerY), (posRayX, posRayY), 1)
                break


def rect3d (iray,rayAngle,nb):
    nb = nb * math.cos(playerAngle - rayAngle)
    RectLong = 2000/nb *50
    RectLarg = screenY/nbRay
    RectY = (screenY-RectLong)/2
    coul=abs((nb*150/1200) - 150)
    pygame.draw.rect(screen, (coul, coul, coul), (screenX+iray*RectLarg, RectY, RectLarg, RectLong))
def pixelparpixel(angleRay,i):
    for nb in range(diagonal):

        posRayX = playerX - math.cos(angleRay) * nb
        posRayY = playerY - math.sin(angleRay) * nb

        colPosRay = floor(posRayX / rectSize)
        lignePosRay = floor(posRayY / rectSize)
        carre = int(lignePosRay * carteSize[0] + colPosRay)


        if Carte[carre] == "1":
            rect3d(i, angleRay, nb)
            pygame.draw.line(screen, (255, 255, 0), (playerX, playerY), (posRayX, posRayY), 1)
            break
def car_affine(pente,cosAngle,sinAngle,signeCos,signeSin,diffPiSur2,posX, posY):

    if diffPiSur2<precision or diffPiSur2>(pi/2 - precision ):
        return 0,0,0,False

    def f_affine(x):
        return pente*x
    if cosAngle > 0:
        dizainePosX = posX % 100
        posXtest1 = posX - dizainePosX - 0.05

    else:
        dizainePosX = rectSize - posX % 100
        posXtest1 = posX + dizainePosX + 0.05
    if sinAngle < 0:
        dizainePosY = rectSize -posY % 100
        posYtest2=posY + dizainePosY + 0.05
    else:
        dizainePosY = posY % 100
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

def f_all():
    debut=time.time()
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screenX, screenY))
    pygame.draw.rect(screen, Grey, (screenX, 0, screenX, screenY/2))
    pygame.draw.rect(screen, darkGrey, (screenX, screenY / 2, screenX, screenY / 2))
    draw2D()
    player()
    rays()
    process = time.time() - debut
    textAngle = font.render(str(int(1/process)), True,(0,0,0))
    screen.blit(textAngle,(10,30))
pygame.init()
screen = pygame.display.set_mode((screenX*2,screenY))
font = pygame.font.SysFont('freesansbold.ttf', 90)
temps = pygame.time.Clock()
f_all()
while True:
    f_all()
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
        playerCol = int((playerX + math.cos(playerAngle) * 8) / rectSize)
        playerLigne = int((playerY + math.sin(playerAngle) * 8) / rectSize)
        playerCarre = playerLigne * carteSize[1] + playerCol
        if Carte[playerCarre] != "1":
            playerX += math.cos(playerAngle) * 8
            playerY += math.sin(playerAngle) * 8
            f_all()
    if keys[pygame.K_z] :
        playerCol=int((playerX-math.cos(playerAngle) * 8)/rectSize)
        playerLigne=int((playerY-math.sin(playerAngle) * 8)/rectSize)
        playerCarre=playerLigne*carteSize[1] + playerCol
        if Carte[playerCarre]!="1":
            playerX -= math.cos(playerAngle) * 8
            playerY -= math.sin(playerAngle) * 8

    pygame.display.flip()
    temps.tick(30)

