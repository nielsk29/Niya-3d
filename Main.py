
import globalVariable as glb
import Rayon
import Map2d
import test
import objet
import Draw3d
import pygame
import sys
import math
import time


def f_all(murBrique):  # fonction qui regroupe tout pour créer une image
    glb.process2 = 0
    glb.process3 = 0
    debut=time.time()  # debut du temps pour calculer les fps
    pygame.draw.rect(glb.screen, glb.Grey, (0, 0, glb.screenX*2, glb.screenY / 2)) # créer un rectangle pour le ciel
    pygame.draw.rect(glb.screen, glb.darkGrey, (0, glb.screenY / 2, glb.screenX*2, glb.screenY / 2)) # créer un rectangle pour le sol
    Rayon.rays(murBrique)  # utilise la fonction qui envoie les rayons et puis créer les murs

    #objet.objet(glb.listeObjet)

    glb.objet2d=[]
    if glb.afficherMap:  # pour savoir si la MiniMap doit être affiché
        Map2d.drawMap2D(glb.sizeMmap, glb.sizeMmap)  # utilise la fonction qui créer la MiniMap
    glb.process = time.time() - debut    #fin chronomètre pour savoir le temps que prend une seul image à être affiché
    textFPS = glb.font.render(str(int(1/glb.process)), True,(0,0,0)) # créer l'image du chiffre des fps
    temps3d = glb.font.render(str(glb.process2), True, (0, 0, 0))
    frame = glb.font.render(str(glb.process), True,(0,0,0))
    textpro3 = glb.font.render(str(glb.process3), True,(0,0,0))
    glb.screen.blit(textFPS, (10, 30))
    glb.screen.blit(glb.gunImage[glb.gunCurrentFrame], glb.posGun)
    glb.screen.blit(glb.viseur,glb.posViseur)
    #glb.screen.blit(frame,(10,100)) # affiche l'image des FPS
    #glb.screen.blit(temps3d, (10, 170))
    #glb.screen.blit(textpro3, (10, 240))

f_all(glb.murBrique)  # créer la 1ère image
while True:  # boucle infinie jusqu'a qu'on quitte le jeu
    f_all(glb.murBrique)  # création de l'image
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                glb.exit = True
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and glb.gunStatus == False:
            glb.shoot = True
            glb.gunStatus = True
        if event.type == pygame.MOUSEMOTION:
            mousex = pygame.mouse.get_pos()
            decalage = abs(mousex[0] - 1200) / 2400
            if mousex[0] > (glb.screenX+5) :
                glb.playerAngle = (glb.playerAngle+decalage)%glb.pi2  # on augmente l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
                pygame.mouse.set_pos(glb.screenX, int(glb.screenY/2))
            elif mousex[0] < (glb.screenX-5):
                glb.playerAngle = (glb.playerAngle-decalage)%glb.pi2 # on réduit l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
                pygame.mouse.set_pos(glb.screenX, int(glb.screenY/2))
        if event.type == pygame.QUIT:
            print(glb.maxlong)
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()
    keys = pygame.key.get_pressed()  # variable des touches presser
    if glb.gunStatus == True and glb.gunCurrentFrame<16:
        if glb.gunCurrentFrame==4:
            pygame.mixer.Sound.play(glb.gunSound)
        glb.gunCurrentFrame += 2
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
    if keys[pygame.K_d]:  # si on appuie sur le "d"
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX + signeSin * 24) / glb.rectSizeX)
        playerLigne = int((glb.playerY - signeCos * 24) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]] != "1" and glb.Carte[playerCarre[0]] != "1":
            glb.playerX += math.sin(glb.playerAngle) * (glb.vitesse/2)
            glb.playerY -= math.cos(glb.playerAngle) * (glb.vitesse/2)
    if keys[pygame.K_q]: # si on appuie sur le q
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX - signeSin * 24) / glb.rectSizeX)
        playerLigne = int((glb.playerY + signeCos * 24) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]] != "1" and glb.Carte[playerCarre[0]] != "1":
            glb.playerX -= math.sin(glb.playerAngle) * (glb.vitesse/2)
            glb.playerY += math.cos(glb.playerAngle) * (glb.vitesse/2)
    if keys[pygame.K_s]: # si on appuie sur le "s"
        signeCos = math.copysign(1, math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol = int((glb.playerX + signeCos * 24) / glb.rectSizeX)
        playerLigne = int((glb.playerY + signeSin * 24) / glb.rectSizeY)
        curentLigne = int(glb.playerY / glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre = (playerLigne * glb.carteSize[0] + curentCol, curentLigne * glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]] != "1" and glb.Carte[playerCarre[0]] != "1":
            glb.playerX += math.cos(glb.playerAngle) * glb.vitesse
            glb.playerY += math.sin(glb.playerAngle) * glb.vitesse
    if keys[pygame.K_z] : # si on appuie sur le "z"

        # On fait la même chose sauf qu'au lieu d'augmenter du cosinus ou le sinus on le soustraie le cosinus ou le sinus
        signeCos = math.copysign(1,math.cos(glb.playerAngle))
        signeSin = math.copysign(1, math.sin(glb.playerAngle))
        playerCol=int((glb.playerX- signeCos * 24)/glb.rectSizeX)
        playerLigne=int((glb.playerY-signeSin * 24)/glb.rectSizeY)
        curentLigne = int(glb.playerY/glb.rectSizeY)
        curentCol = int(glb.playerX / glb.rectSizeX)
        playerCarre= (playerLigne*glb.carteSize[0] + curentCol,curentLigne*glb.carteSize[0] + playerCol)
        if glb.Carte[playerCarre[1]]!="1" and glb.Carte[playerCarre[0]]!="1":
            glb.playerX -= math.cos(glb.playerAngle) * glb.vitesse
            glb.playerY -= math.sin(glb.playerAngle) * glb.vitesse
    if keys[pygame.K_TAB]:  # Si la touche "TAB" est pressé

            glb.afficherMap = not glb.afficherMap  # on inverse le boléen qui permet d'afficher la Minimap

    mapplayerX = glb.playerX * glb.minimap / glb.gameX  # calcul de la position X du joueur dans la MiniMap
    mapplayerY = glb.playerY * glb.minimap / glb.gameY  # calcul de la position Y du joueur dans la MiniMap
    pygame.display.flip()  # mets à jour la fenêtre donc affiche la frame
    glb.temps.tick(30)

