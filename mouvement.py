import globalVariable as glb
import pygame
import math
import objet
import sys
import menu


def regard():
    mousex = pygame.mouse.get_pos()  # on prend la position de la souris
    decalage = abs(mousex[0] - glb.millieuX) / (glb.screenX * 1.5) * glb.reductionEcran  # calcul de combien on doit décaler la souris
    if mousex[0] > (glb.millieuX):  # si on va à droite
        glb.playerAngle = (glb.playerAngle + decalage) % glb.pi2  # on augmente l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
        pygame.mouse.set_pos(glb.millieuX, int(glb.screenY / 2))
    elif mousex[0] < (glb.millieuX):  # si onva à gauche
        glb.playerAngle = (glb.playerAngle - decalage) % glb.pi2  # on réduit l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
        pygame.mouse.set_pos(glb.millieuX, int(glb.screenY / 2))

def zqsd():
    keys = pygame.key.get_pressed()  # variable des touches presser
    if keys[pygame.K_d]:  # si on appuie sur le "d"
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX + signeSin * 12) / glb.rectSizeX)  # calcul de la colonne inverse de laquelle on regarde
        playerLigne = int((glb.playerY - signeCos * 12) / glb.rectSizeY)  # calcul de la ligne sur la carte vers laquelle on regarde
        curentLigne = int(glb.playerY / glb.rectSizeY)  # ligne actuelle du joueur
        curentCol = int(glb.playerX / glb.rectSizeX)  # colonne actuelle du joueur
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)  # calcul des indices des deux carre qu'on verifie
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]: # si il y a rien on avance
            glb.playerX += math.sin(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)   # on baisse la pos X
            glb.playerY -= math.cos(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)  # on augmente la pos Y
    if keys[pygame.K_q]: # si on appuie sur le q
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX - signeSin * 12) / glb.rectSizeX)                   # même calcul que pour le d met c'est la ligne qu'on inverse
        playerLigne = int((glb.playerY + signeCos * 12) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX -= math.sin(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)  # on augmente la pos X
            glb.playerY += math.cos(glb.playerAngle) * (glb.vitesse *glb.varVitesse/2)  # on baisse la pos Y
    if keys[pygame.K_s]: # si on appuie sur le "s"
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX + signeCos * 12) / glb.rectSizeX)                  # même chose mais les deux on inverse
        playerLigne = int((glb.playerY + signeSin * 12) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX += math.cos(glb.playerAngle) * glb.vitesse *glb.varVitesse  # on baisse la pos X
            glb.playerY += math.sin(glb.playerAngle) * glb.vitesse *glb.varVitesse  # on baisse la pos Y
    if keys[pygame.K_z] : # si on appuie sur le "z"

        # On fait la même chose sauf qu'au lieu d'augmenter du cosinus ou le sinus on le soustraie le cosinus ou le sinus
        signeCos = math.copysign(1,math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol=int((glb.playerX- signeCos * 12)/glb.rectSizeX)           # même chose sans en inverser
        playerLigne=int((glb.playerY-signeSin * 12)/glb.rectSizeY)
        curentLigne = int(glb.playerY/glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre= (playerLigne*glb.carteSize[0] + curentCol,curentLigne*glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1" and glb.statusPorte[playerCarre[1]][1] and glb.statusPorte[playerCarre[0]][1]:
            glb.playerX -= math.cos(glb.playerAngle) * glb.vitesse *glb.varVitesse  # on augmente la pos X
            glb.playerY -= math.sin(glb.playerAngle) * glb.vitesse *glb.varVitesse  # on augmente la pos Y
    if keys[pygame.K_LSHIFT]:  # si on appuie sur shift
        glb.varVitesse = 1.5  # on le met à 1.5 pour que ça multiplie la vitesse de 1,5
    else :
        glb.varVitesse = 1
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # si on appuie sur echap
                menu.pause()  # si on met le menu pause
            if event.key == pygame.K_TAB:  # Si la touche "TAB" est pressé

                glb.afficherMap = not glb.afficherMap  # on inverse le boléen qui permet d'afficher la Minimap
            if event.key == pygame.K_e:  # si on appuie sur e
                signeCos = math.copysign(1, math.cos(glb.playerAngle))
                signeSin = math.copysign(1, math.sin(glb.playerAngle))
                playerCol = int((glb.playerX - signeCos * 75) / glb.rectSizeX)
                playerLigne = int((glb.playerY - signeSin * 75) / glb.rectSizeY)        # même calcul que pour avancer
                curentLigne = int(glb.playerY / glb.rectSizeY)
                curentCol = int(glb.playerX / glb.rectSizeX)
                playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol,
                               curentLigne * glb.carteSize[0] + curentCol)
                if glb.Carte[playerCarre[2]] != "2":  # si on est pas sur une porte car on veut pas faire bouger la porte alors que on est deçu
                    if glb.Carte[playerCarre[1]] == "2":  # si le carre devant sur la même ligne
                        glb.statusPorte[playerCarre[1]][2] = True  # on le met à True car on veut animé la porte
                    elif glb.Carte[playerCarre[0]] == "2":  # si le carre devant sur la même colonne
                        glb.statusPorte[playerCarre[0]][2] = True  # on le met à True car on veut animé la porte
                for obj in range(len(glb.listeObjet)):  # on parcours tout les objets
                    diffx = glb.listeObjet[obj][1] - glb.playerX  # différence en x avec l'objet
                    diffy = glb.listeObjet[obj][2] - glb.playerY  # différence en x avec l'objet
                    if abs(diffx) < 100 and abs(diffy) < 100: # si la différence est plus petit que 100
                        if (objet.calculAngleObj(diffx, diffy) - glb.playerAngle) < (glb.pi / 4): # on regarde si on regarde dans sa direction
                            if glb.listeObjet[obj][0]==1:  # si c'est un medkit
                                if glb.nbmedkit < 3:  # si on en a moin que 3
                                    glb.nbmedkit += 1  # on ajoute 1
                                    glb.medkitSound.play()  # on joue le son du medkit
                                    del glb.listeObjet[obj]  # on suprime l'objet de la liste
                                    break
                            elif glb.listeObjet[obj][0] == 5:  # si c'est une boite de munition
                                glb.ammoSound.play()  # on joue le son de la boite de munition
                                glb.nbballes += 25  # on ajoute 25 au nombre de balles
                                del glb.listeObjet[obj]  # on suprime l'objet de la liste
                                break
            if event.key == pygame.K_c:  # si on appuie sur c
                glb.armeStatus[0] = (glb.armeStatus[0] + 1) % 2  # on met à 1 si c'est 0 et on met à 0 si c'est 1
            if event.key == pygame.K_t:  # t
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

