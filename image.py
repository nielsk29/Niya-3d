import globalVariable as glb
import pygame
import Map2d
import Rayon





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
