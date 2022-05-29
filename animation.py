import time

import globalVariable as glb

import chargement
import pygame
import math
import random
import image
import menu
import objet
import sys

def anim():
    if glb.armeStatus[1] == True and glb.armeStatus[4]<(glb.armeParrametre[glb.armeStatus[0]][0]-glb.armeParrametre[glb.armeStatus[0]][1]):
        if glb.armeStatus[4]==0:
            pygame.mixer.Sound.play(glb.armeParrametre[glb.armeStatus[0]][5])
        glb.armeStatus[4] += glb.armeParrametre[glb.armeStatus[0]][1]
        glb.armeStatus[2] = False
    else :
        glb.armeStatus[4] = 0
        glb.armeStatus[2] = False
        glb.armeStatus[1] = False
    if glb.armeStatus[3] and glb.sangCurrentFrame<10:
        glb.sangCurrentFrame += 2
        newFrame = pygame.transform.scale(glb.sang[glb.sangCurrentFrame],glb.newSangLong)
        glb.screen.blit(newFrame,glb.posSang)
    else:
        glb.sangCurrentFrame = 0
        glb.armeStatus[3] = False
    nb=0
    for element in glb.lObjAnim:
        frame = glb.listeMonstre[element][3]
        if frame<10:
            glb.listeMonstre[element][3] += 0.2
        else:
            if random.choice([False,False,False,True]):
                glb.listeObjet.append([random.choice([1,5]),glb.listeMonstre[element][1]-5,glb.listeMonstre[element][2]-5,0])
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
        anglePlayer = objet.calculAngleObj(element[1]-glb.playerX, element[2]-glb.playerY)
        glb.listeBall[nb][1] =glb.listeBall[nb][1]-cosBalle*20
        glb.listeBall[nb][2] =glb.listeBall[nb][2]-sinBalle*20
        ligne = int(glb.listeBall[nb][2] / glb.rectSizeY)
        col = int(glb.listeBall[nb][1] / glb.rectSizeX)
        carre = ligne * glb.carteSize[0] + col
        diffAngle = abs(anglePlayer-element[4])
        if diffAngle>glb.pi :
            reverse = anglePlayer < element[4]
        else :
            reverse = anglePlayer > element[4]
        if glb.pi8*9 > diffAngle > glb.pi8*7:
            glb.listeBall[nb][3] = 0
        if glb.pi8*7 > diffAngle > glb.pi8*5 or glb.pi8*11 > diffAngle > glb.pi8*9:
            glb.listeBall[nb][3] = 1 + reverse
        if glb.pi8*5 > diffAngle > glb.pi8*3 or glb.pi8*13 > diffAngle > glb.pi8*11:
            glb.listeBall[nb][3] = 3 + reverse
        if glb.pi8*3 > diffAngle > glb.pi8 or glb.pi8*15 > diffAngle > glb.pi8*13:
            glb.listeBall[nb][3] = 5 + reverse
        if glb.pi8 > diffAngle or glb.pi8*15 < diffAngle:
            glb.listeBall[nb][3] = 7
        if (abs(element[1]-glb.playerX)<25 and abs(element[2]-glb.playerY)<15) \
                or (abs(glb.playerX - (element[1]+cosBalle*20)) < 15 and abs(glb.playerY - (element[2]+sinBalle*20)) < 15) \
                or (abs(glb.playerX - (element[1]+cosBalle*10)) < 15 and abs(glb.playerY - (element[2]+sinBalle*10)) < 15) :
            glb.playerVie -= 30
            if glb.playerVie>0:
                pygame.mixer.Sound.play(glb.injuredSound)
            else:
                pygame.mixer.Sound.play(glb.deathSound)
            del glb.listeBall[nb]
        elif glb.Carte[carre]=="1":
            del glb.listeBall[nb]
        nb+=1

    nb = 0
    for element in glb.statusMonstre :
        if glb.vieMonstre[nb]>0 :
            if element[0] and not(element[1]):
                diffTemps = time.time()-element[2]
                if diffTemps>element[4]:
                    glb.statusMonstre[nb][1] = True
                    glb.statusMonstre[nb][4] = random.randint(2,6)
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
                    glb.shootMonstreSound.play()
                    glb.listeBall.append([4, glb.listeMonstre[nb][1], glb.listeMonstre[nb][2], 0, angle])
                    glb.statusMonstre[nb][3] = True
                elif frame==0 :
                    glb.listeMonstre[nb][3] = 11
                else:
                    glb.listeMonstre[nb][3] += 0.5

        nb += 1
    nb = 0
    for element in glb.listeObjet:
        if element[0] == 5:
            if abs(glb.playerX - element[1]) < 10 and abs(glb.playerY - element[2]) < 10:
                glb.ammoSound.play()
                glb.nbballes += random.randint(10, 25)
                del glb.listeObjet[nb]

        nb += 1
    if glb.playerVie<=0:
        mort()

def mort():
    listeRectNoir = []
    for i in range(int(glb.screenX/4)):
        listeRectNoir.append([i*4,0,4,0])
    verif=True
    nbTerminer = [False]*len(listeRectNoir)
    while verif:

        for x in range(len(listeRectNoir)):
            if listeRectNoir[x][3]<glb.screenY:
                listeRectNoir[x][3] += random.randint(0,20)
            else :
                nbTerminer[x] = True
            pygame.draw.rect(glb.screen, (50,0,0), listeRectNoir[x])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glb.exit = True
                    pygame.quit()  # Si on quitte le jeu
                    sys.exit()
            if event.type == pygame.QUIT:
                print(glb.maxlong)
                pygame.quit()  # Si on quitte le jeu
                sys.exit()
        glb.temps.tick(60)
        pygame.display.flip()
        if not(False in nbTerminer):
            verif=False
    pygame.mouse.set_visible(True)
    verif=True
    while verif:
        quitter = glb.screen.blit(glb.imageQuit, ((glb.screenX - glb.imageQuit.get_width()) / 2, glb.screenY * 2 / 3 - glb.imageQuit.get_height() / 2))
        restart = glb.screen.blit(glb.imageRestart, ((glb.screenX - glb.imageRestart.get_width()) / 2, glb.screenY / 3 - glb.imageRestart.get_height() / 2))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x,y)
                print(glb.imageQuit.get_rect())
                if quitter.collidepoint(x, y):
                    glb.exit = True
                    pygame.quit()  # Si on quitte le jeu
                    sys.exit()
                if restart.collidepoint(x, y):
                    chargement.restart()
                    rest = True
                    nbTerminer = [False] * len(listeRectNoir)
                    print(listeRectNoir)
                    while verif :
                        image.f_all(glb.murBrique)
                        menu.afficher()
                        for x in range(len(listeRectNoir)):
                            if listeRectNoir[x][3] > 0 :
                                listeRectNoir[x][3] -= random.randint(0, 30)
                                print(listeRectNoir[x][3])
                            else:
                                nbTerminer[x] = True
                            pygame.draw.rect(glb.screen, (50, 0, 0), listeRectNoir[x])
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    glb.exit = True
                                    pygame.quit()  # Si on quitte le jeu
                                    sys.exit()
                            if event.type == pygame.QUIT:
                                print(glb.maxlong)
                                pygame.quit()  # Si on quitte le jeu
                                sys.exit()
                      #  glb.temps.tick(60)
                        pygame.display.flip()
                        if not (False in nbTerminer):
                            verif = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glb.exit = True
                    pygame.quit()  # Si on quitte le jeu
                    sys.exit()
            if event.type == pygame.QUIT:
                print(glb.maxlong)
                pygame.quit()  # Si on quitte le jeu
                sys.exit()
        glb.temps.tick(60)
        pygame.display.flip()
