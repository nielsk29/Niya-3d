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
    nb=0
    for element in glb.statusPorte:
        if element[2]:
            if element[1] or element[3]:
                if glb.statusPorte[nb][0] == glb.rectSizeX:
                    pygame.mixer.Sound.play(glb.CloseDoorSound)
                glb.statusPorte[nb][0] -= 3
                glb.statusPorte[nb][3] = True
                glb.statusPorte[nb][1] = False
                if glb.statusPorte[nb][0] <= 0:
                    glb.statusPorte[nb][0] = 0
                    glb.statusPorte[nb][1] = False
                    glb.statusPorte[nb][2] = False
                    glb.statusPorte[nb][3] = False
            else:
                if glb.statusPorte[nb][0] == 0:
                    pygame.mixer.Sound.play(glb.OpenDoorSound)
                glb.statusPorte[nb][0] += 3
                if glb.statusPorte[nb][0] >= glb.rectSizeX:
                    glb.statusPorte[nb][0] = glb.rectSizeX
                    glb.statusPorte[nb][1] = True
                    glb.statusPorte[nb][2] = False

        nb+=1
