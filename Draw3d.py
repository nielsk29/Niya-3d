import globalVariable as glb
import pygame
import time
import math
def rect3d (iray,rayAngle,nb,cote,rayX,rayY,imageMur):
    global process, objet2d
    debut= time.time()
    nb = nb * math.cos(glb.playerAngle - rayAngle)
    RectLong = 1200/nb *100*(glb.screenMulti**2)

    RectLarg = glb.screenX*2/glb.nbRay
    RectY = (glb.screenY-RectLong)/2
    coul=abs((nb*150/2400) - 150)
    #mur = pygame.transform.scale(imageMur, (int(RectLong), int(RectLong)))

    imageSizeX = imageMur.get_width()-1
    imageSizeY = imageMur.get_height()-1

    if cote ==1:
        Ximage=int((rayY%glb.rectSizeY)*imageSizeX/glb.rectSizeY)

    else:
        Ximage = int((rayX % glb.rectSizeX)*imageSizeX/glb.rectSizeX)
    mur = imageMur.subsurface((Ximage, 0, RectLarg, imageSizeY))
    #screen.blit(mur, (600, 600))
    mur = pygame.transform.scale(mur, (int(RectLarg), int(RectLong)))
    #pygame.draw.rect(screen,Grey,(600,600,500,500))
    #screen.blit(mur, (600, 600))
    glb.screen.blit(mur, (iray*RectLarg, RectY))
    #pygame.draw.rect(screen, (coul, coul, coul), (iray*RectLarg, RectY, RectLarg, RectLong))
