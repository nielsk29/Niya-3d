import animation
import globalVariable as glb
import Rayon
import Map2d
import mouvement
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
    pygame.draw.rect(glb.screen, glb.Grey, (0, 0, glb.screenX, glb.screenY / 2)) # créer un rectangle pour le ciel
    pygame.draw.rect(glb.screen, glb.darkGrey, (0, glb.screenY / 2, glb.screenX, glb.screenY / 2)) # créer un rectangle pour le sol
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
    glb.screen.blit(glb.gunImage[math.floor(glb.gunCurrentFrame)], glb.posGun)
    glb.screen.blit(glb.viseur,glb.posViseur)
    #glb.screen.blit(frame,(10,100)) # affiche l'image des FPS
    #glb.screen.blit(temps3d, (10, 170))
    #glb.screen.blit(textpro3, (10, 240))

f_all(glb.murBrique)  # créer la 1ère image
while True:  # boucle infinie jusqu'a qu'on quitte le jeu
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                glb.exit = True
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and glb.gunStatus == False:
            glb.shoot = True
            glb.gunStatus = True
        if event.type == pygame.MOUSEMOTION:
            mouvement.regard()
        if event.type == pygame.QUIT:
            print(glb.maxlong)
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()
    mouvement.zqsd()
    mapplayerX = glb.playerX * glb.minimap / glb.gameX  # calcul de la position X du joueur dans la MiniMap
    mapplayerY = glb.playerY * glb.minimap / glb.gameY  # calcul de la position Y du joueur dans la MiniMap
    f_all(glb.murBrique)  # création de l'image
    animation.anim()
    pygame.display.flip()  # mets à jour la fenêtre donc affiche la frame
    glb.temps.tick(25)

