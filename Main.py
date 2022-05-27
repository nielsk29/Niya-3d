import animation
import globalVariable as glb
import Rayon
import Map2d
import mouvement
import menu
import objet
import Draw3d
import pygame
import sys
import math
import time
import image




    #glb.screen.blit(textpro3, (10, 240))

while True:  # boucle infinie jusqu'a qu'on quitte le jeu
    debut = time.time()  # debut du temps pour calculer les fps
    mouvement.zqsd()
    mapplayerX = glb.playerX * glb.minimap / glb.gameX  # calcul de la position X du joueur dans la MiniMap
    mapplayerY = glb.playerY * glb.minimap / glb.gameY  # calcul de la position Y du joueur dans la MiniMap
    image.f_all(glb.murBrique)  # création de l'image
    animation.anim()
    menu.afficher()
    glb.process = time.time() - debut  # fin chronomètre pour savoir le temps que prend une seul image à être affiché
    pygame.display.flip()  # mets à jour la fenêtre donc affiche la frame
    glb.temps.tick(30)

