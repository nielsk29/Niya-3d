import time

import pygame
import globalVariable as glb
import math

def afficher():
    tailleballes = glb.ballesimg.get_height()
    glb.screen.blit(glb.ballesimg , (10, int(glb.screenY- tailleballes)))
    nbammo = glb.font.render(str(glb.nbballes), True, (0,0,0))
    glb.screen.blit(nbammo, (35 , int(glb.screenY / 6 * 5)))
    textFPS = glb.font.render(str(int(1/glb.process)), True,(0,0,0)) # créer l'image du chiffre des fps
    texteVie = glb.font.render(str(glb.armeStatus), True, (0, 0, 0))

    textpro3 = glb.font.render(str(glb.process3), True,(0,0,0))
    glb.screen.blit(textFPS, (10, 30))
    debut = time.time()
    glb.screen.blit(glb.armeImage[glb.armeStatus[0]][math.floor(glb.armeStatus[4])], glb.posArme[glb.armeStatus[0]][math.floor(glb.armeStatus[4])])
    glb.process2 = time.time()- debut
    frame = glb.font.render(str(glb.process2), True, (0, 0, 0))
    glb.screen.blit(glb.viseur,glb.posViseur)
    #glb.screen.blit(frame,(10,100)) # affiche l'image des FPS
    #glb.screen.blit(texteVie, (10, 170))
    nbmedkits = glb.font.render(str(glb.nbmedkit), True, (0,0,0))
    taillekity = glb.listeImageOBJ[1][0].get_height()
    taillekitx = glb.listeImageOBJ[1][0].get_width()
    tailletxty = nbmedkits.get_height()
    tailletxtx = nbmedkits.get_width()
    imgmedkit = pygame.transform.scale(glb.listeImageOBJ[1][0],(int(tailletxty * taillekitx / taillekity), tailletxty))
    taillekitx = imgmedkit.get_width()
    glb.screen.blit(imgmedkit, (glb.screenX - (taillekitx+10) ,glb.screenY - tailletxty))
    glb.screen.blit(nbmedkits, (glb.screenX - (tailletxtx+20) ,glb.screenY - (tailletxty+80)))
    pygame.draw.rect(glb.screen, (192, 18, 0), (glb.screenX/2-300,glb.screenY-110, glb.playerVie*600/100, 100))
    pygame.draw.rect(glb.screen, (0, 0, 0), (glb.screenX/2-300,glb.screenY-110,600,100) , 10)
