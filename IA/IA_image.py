import IA_globalVariable as glb
import pygame
import IA_Map2d
import IA_Rayon
import IA_objet




def f_all(murBrique):  # fonction qui regroupe tout pour créer une image
    glb.process2 = 0
    glb.process3 = 0

    pygame.draw.rect(glb.screen, glb.Grey, (0, 0, glb.screenX, glb.screenY / 2)) # créer un rectangle pour le ciel
    pygame.draw.rect(glb.screen, glb.darkGrey, (0, glb.screenY / 2, glb.screenX, glb.screenY / 2)) # créer un rectangle pour le sol
    IA_Rayon.rays(murBrique)  # utilise la fonction qui envoie les Rayos et puis créer les murs

    #IA_objet.objet(glb.listeobjet)

    glb.objet2d=[]
    if glb.afficherMap:  # pour savoir si la MiniMap doit être affiché
        IA_Map2d.drawMap2D(glb.sizeMmap, glb.sizeMmap)  # utilise la fonction qui créer la MiniMap


def f_all2d():
    glb.process2 = 0
    glb.process3 = 0
    glb.listeRond = []  # liste qui contient les cercles à afficher sur la MiniMap
    glb.listeRay = []
    pygame.draw.rect(glb.screen, (0,0,0), (0, 0, glb.screenX, glb.screenY))
    IA_objet.CreerListeAngleOBJ(glb.listeObjet)
    IA_Map2d.drawMap2D(glb.sizeMmap, glb.sizeMmap)
    glb.objet2d = []
