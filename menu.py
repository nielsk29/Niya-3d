import pygame
import globalVariable as glb

def afficher():
    tailleballes = glb.ballesimg.get_height()
    glb.screen.blit(glb.ballesimg , (10, int(glb.screenY- tailleballes)))
    nbammo = glb.font.render(str(glb.nbballes), True, (0,0,0))
    glb.screen.blit(nbammo, (35 , int(glb.screenY / 6 * 5)))