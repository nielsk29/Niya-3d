import globalVariable as glb
import pygame
import math


def anim():
    if glb.gunStatus == True and glb.gunCurrentFrame<16:
        if glb.gunCurrentFrame==4:
            pygame.mixer.Sound.play(glb.gunSound)
        glb.gunCurrentFrame += 2
        glb.shoot = False
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
    nb=0
    for element in glb.lObjAnim:
        frame = glb.listeObjet[element][3]
        if frame<10:
            glb.listeObjet[element][3] += 0.2
        else:
            del glb.lObjAnim[nb]
