import globalVariable as glb
import pygame
import math
import objet
import sys


def regard():
    mousex = pygame.mouse.get_pos()
    decalage = abs(mousex[0] - glb.millieuX) / (glb.screenX * 1.5) * glb.reductionEcran
    if mousex[0] > (glb.millieuX):
        glb.playerAngle = (glb.playerAngle + decalage) % glb.pi2  # on augmente l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
        pygame.mouse.set_pos(glb.millieuX, int(glb.screenY / 2))
    elif mousex[0] < (glb.millieuX):
        glb.playerAngle = (glb.playerAngle - decalage) % glb.pi2  # on réduit l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
        pygame.mouse.set_pos(glb.millieuX, int(glb.screenY / 2))

def zqsd():
    keys = pygame.key.get_pressed()  # variable des touches presser
    if keys[pygame.K_d]:  # si on appuie sur le "d"
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX + signeSin * 12) / glb.rectSizeX)
        playerLigne = int((glb.playerY - signeCos * 12) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX += math.sin(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)
            glb.playerY -= math.cos(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)
    if keys[pygame.K_q]: # si on appuie sur le q
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX - signeSin * 12) / glb.rectSizeX)
        playerLigne = int((glb.playerY + signeCos * 12) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX -= math.sin(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)
            glb.playerY += math.cos(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)
    if keys[pygame.K_s]: # si on appuie sur le "s"
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX + signeCos * 12) / glb.rectSizeX)
        playerLigne = int((glb.playerY + signeSin * 12) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX += math.cos(glb.playerAngle) * glb.vitesse *glb.varVitesse
            glb.playerY += math.sin(glb.playerAngle) * glb.vitesse *glb.varVitesse
    if keys[pygame.K_z] : # si on appuie sur le "z"

        # On fait la même chose sauf qu'au lieu d'augmenter du cosinus ou le sinus on le soustraie le cosinus ou le sinus
        signeCos = math.copysign(1,math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol=int((glb.playerX- signeCos * 12)/glb.rectSizeX)
        playerLigne=int((glb.playerY-signeSin * 12)/glb.rectSizeY)
        curentLigne = int(glb.playerY/glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre= (playerLigne*glb.carteSize[0] + curentCol,curentLigne*glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX -= math.cos(glb.playerAngle) * glb.vitesse *glb.varVitesse
            glb.playerY -= math.sin(glb.playerAngle) * glb.vitesse *glb.varVitesse
    if keys[pygame.K_LSHIFT]:
        glb.varVitesse = 1.5
    else :
        glb.varVitesse = 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                glb.exit = True
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
            if event.key == pygame.K_TAB:  # Si la touche "TAB" est pressé

                glb.afficherMap = not glb.afficherMap  # on inverse le boléen qui permet d'afficher la Minimap
            if event.key == pygame.K_e:
                signeCos = math.copysign(1, math.cos(glb.playerAngle))
                signeSin = math.copysign(1, math.sin(glb.playerAngle))
                playerCol = int((glb.playerX - signeCos * 75) / glb.rectSizeX)
                playerLigne = int((glb.playerY - signeSin * 75) / glb.rectSizeY)
                curentLigne = int(glb.playerY / glb.rectSizeY)
                curentCol = int(glb.playerX / glb.rectSizeX)
                playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol,
                               curentLigne * glb.carteSize[0] + curentCol)
                if glb.Carte[playerCarre[2]] != "2":
                    if glb.Carte[playerCarre[1]] == "2":
                        glb.statusPorte[playerCarre[1]][2] = True
                    elif glb.Carte[playerCarre[0]] == "2":
                        glb.statusPorte[playerCarre[0]][2] = True
                for obj in range(len(glb.listeObjet)):
                    diffx = glb.listeObjet[obj][1] - glb.playerX
                    diffy = glb.listeObjet[obj][2] - glb.playerY
                    if abs(diffx) < 100 and abs(diffy) < 100:
                        if (objet.calculAngleObj(diffx, diffy) - glb.playerAngle) < (glb.pi / 4):
                            if glb.listeObjet[obj][0]==1:
                                if glb.nbmedkit < 3:
                                    glb.nbmedkit += 1
                                    glb.medkitSound.play()
                                    del glb.listeObjet[obj]
                                    break
                            elif glb.listeObjet[obj][0] == 5:
                                glb.ammoSound.play()
                                glb.nbballes += 25
                                del glb.listeObjet[obj]
                                break
            if event.key == pygame.K_c:
                glb.armeStatus[0] = (glb.armeStatus[0] + 1) % 2
            if event.key == pygame.K_t:
                if glb.nbmedkit > 0:
                    glb.nbmedkit -= 1
                    glb.playerVie += 30
                    if glb.playerVie > 100:
                        glb.playerVie = 100
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and glb.armeStatus[1] == False and (glb.nbballes > 0 or glb.armeParrametre[glb.armeStatus[0]][3]==0):
            glb.nbballes -= glb.armeParrametre[glb.armeStatus[0]][3]
            glb.armeStatus[2] = True
            glb.armeStatus[1] = True
        if event.type == pygame.MOUSEMOTION:
            regard()
        if event.type == pygame.QUIT:
            print(glb.maxlong)
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()

