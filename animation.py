import time

import globalVariable as glb
import pygame
import math
import random
import objet


def anim():
    if glb.gunStatus == True and glb.gunCurrentFrame<10:
        if glb.gunCurrentFrame==4:
            pygame.mixer.Sound.play(glb.gunSound)
        glb.gunCurrentFrame += 2
        glb.shoot = False
    else :
        glb.gunCurrentFrame = 0
        glb.shoot = False
        glb.gunStatus = False
    if glb.toucher and glb.sangCurrentFrame<10:
        glb.sangCurrentFrame += 2
        newFrame = pygame.transform.scale(glb.sang[glb.sangCurrentFrame],glb.newSangLong)
        glb.screen.blit(newFrame,glb.posSang)
    else:
        glb.sangCurrentFrame = 0
        glb.toucher = False
    nb=0
    for element in glb.lObjAnim:
        frame = glb.listeMonstre[element][3]
        if frame<10:
            glb.listeMonstre[element][3] += 0.2
        else:
            del glb.lObjAnim[nb]
    nb=0
    for element in glb.statusPorte:
        if element[2]:
            if element[1] or element[3]:
                if glb.statusPorte[nb][0] == glb.rectSizeX:
                    pygame.mixer.Sound.play(glb.CloseDoorSound)
                glb.statusPorte[nb][0] -= 3
                glb.statusPorte[nb][3] = True
                glb.statusPorte[nb][1] = False
                if glb.statusPorte[nb][0] <= 0:
                    glb.statusPorte[nb][0] = 0
                    glb.statusPorte[nb][1] = False
                    glb.statusPorte[nb][2] = False
                    glb.statusPorte[nb][3] = False
            else:
                if glb.statusPorte[nb][0] == 0:
                    pygame.mixer.Sound.play(glb.OpenDoorSound)
                glb.statusPorte[nb][0] += 3
                if glb.statusPorte[nb][0] >= glb.rectSizeX:
                    glb.statusPorte[nb][0] = glb.rectSizeX
                    glb.statusPorte[nb][1] = True
                    glb.statusPorte[nb][2] = False

        nb+=1
    nb=0

    for element in glb.listeBall:
        cosBalle =  math.cos(element[4])
        sinBalle =  math.sin(element[4])
        glb.listeBall[nb][1] =glb.listeBall[nb][1]-cosBalle*30
        glb.listeBall[nb][2] =glb.listeBall[nb][2]-sinBalle*30
        ligne = int(glb.listeBall[nb][2] / glb.rectSizeY)
        col = int(glb.listeBall[nb][1] / glb.rectSizeX)
        carre = ligne * glb.carteSize[0] + col
        if glb.Carte[carre]=="1":
            del glb.listeBall[nb]
        nb+=1
    nb = 0
    for element in glb.statusMonstre :
        if glb.vieMonstre[nb]>0 :
            if element[0] and not(element[1]):
                diffTemps = time.time()-element[2]
                if diffTemps>element[4]:
                    glb.statusMonstre[nb][1] = True
                    glb.statusMonstre[nb][4] = random.randint(1,5)
                    glb.statusMonstre[nb][2] = time.time()
            if glb.statusMonstre[nb][1]:
                frame = glb.listeMonstre[nb][3]
                if frame >=13:
                    glb.statusMonstre[nb][3] = False
                    glb.statusMonstre[nb][1] = False
                    glb.listeMonstre[nb][3] = 0
                elif math.floor(frame) == 12 and element[3] == False:
                    angle = objet.calculAngleObj((glb.playerX - glb.listeMonstre[nb][1]),
                                                 (glb.playerY - glb.listeMonstre[nb][2]))
                    glb.listeBall.append([4, glb.listeMonstre[nb][1], glb.listeMonstre[nb][2], 0, angle])
                    glb.statusMonstre[nb][3] = True
                elif frame==0 :
                    glb.listeMonstre[nb][3] = 11
                else:
                    glb.listeMonstre[nb][3] += 0.5

        nb += 1
