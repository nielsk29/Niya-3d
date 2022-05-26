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


def f_all(murBrique):  # fonction qui regroupe tout pour créer une image
    glb.process2 = 0
    glb.process3 = 0

    pygame.draw.rect(glb.screen, glb.Grey, (0, 0, glb.screenX, glb.screenY / 2)) # créer un rectangle pour le ciel
    pygame.draw.rect(glb.screen, glb.darkGrey, (0, glb.screenY / 2, glb.screenX, glb.screenY / 2)) # créer un rectangle pour le sol
    Rayon.rays(murBrique)  # utilise la fonction qui envoie les rayons et puis créer les murs

    #objet.objet(glb.listeObjet)

    glb.objet2d=[]
    if glb.afficherMap:  # pour savoir si la MiniMap doit être affiché
        Map2d.drawMap2D(glb.sizeMmap, glb.sizeMmap)  # utilise la fonction qui créer la MiniMap


    #glb.screen.blit(textpro3, (10, 240))

f_all(glb.murBrique)  # créer la 1ère image
while True:  # boucle infinie jusqu'a qu'on quitte le jeu
    debut = time.time()  # debut du temps pour calculer les fps
    mouvement.zqsd()
    mapplayerX = glb.playerX * glb.minimap / glb.gameX  # calcul de la position X du joueur dans la MiniMap
    mapplayerY = glb.playerY * glb.minimap / glb.gameY  # calcul de la position Y du joueur dans la MiniMap
    f_all(glb.murBrique)  # création de l'image
    animation.anim()
    menu.afficher()
    glb.process = time.time() - debut  # fin chronomètre pour savoir le temps que prend une seul image à être affiché
    pygame.display.flip()  # mets à jour la fenêtre donc affiche la frame
    glb.temps.tick(30)

