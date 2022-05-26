import globalVariable as glb
import pygame
import math
import sys

def charg():
    for x in range(0,int( glb.screenY/1.5)):
        sombre = pygame.Surface(( glb.RectLarg, x))
        sombre.set_alpha(int(abs(x*200/( glb.screenY/1.5)-200)))
        sombre.fill((0, 0, 0))
        glb.rectSombre[x] = (sombre,(x,int(abs(x*150/( glb.screenY/1.5)-150)), glb.screenY))
    for x in range(0,12):
        nameFrame = "image/gun/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.armeImage[0][x] = pygame.transform.scale(image,glb.armeTaille[0][x])
    for x in range(0,12):
        nameFrame = "image/sang/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.sang[x] = pygame.transform.scale(image,(glb.sangLongX,glb.sangLongY))
    for x in range(4):
        nameFrame = "image/poing/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.armeTaille[1][x] = (int(image.get_width()*glb.screenX/400),int(image.get_height()*glb.screenY/200))
        glb.armeImage[1][x] = pygame.transform.scale(image, glb.armeTaille[1][x])
        if x == 0:
            glb.posArme[1][x] = (glb.screenX / 3 - glb.armeTaille[1][x][0] / 2, glb.screenY - glb.armeTaille[1][x][1])
        else:
            glb.posArme[1][x] = (glb.screenX/ 3 - glb.armeTaille[1][x][0] / 2, glb.screenY - glb.armeTaille[1][x][1])
    print(glb.armeImage)
