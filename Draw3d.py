import globalVariable as glb
import pygame
import time
import math


def rect3d (iray,rayAngle,nb,cote,rayX,rayY,imageMur):  # fonction qui dessine un rectangle correspondant à un rayon

    nb = nb * math.cos(glb.playerAngle - rayAngle)  # enlève le "fish eye" en prenant la longueur du côté adjacent au personage en formant un triangle rectangle avec le rayon en hypoténuse
    RectLong = 1200/nb *100*(glb.screenMulti**2)  # calcul trouver par tâtonnement pour transformer la distance du rayon en longueur du rectangle
    RectLarg = glb.screenX*2/glb.nbRay  # calcul de la largeur d'un rectangle
    RectY = (glb.screenY-RectLong)/2  # calcul posY du rectangle
    coul=abs((nb*150/2400) - 150)  # couleur pour dégrader
    #mur = pygame.transform.scale(imageMur, (int(RectLong), int(RectLong)))

    imageSizeX = imageMur.get_width()-1  # taille X de l'image
    imageSizeY = imageMur.get_height()-1  # taille Y de l'image

    if cote ==1:  # si on a touché un mur parallel à l'axe X
        Ximage=int((rayY%glb.rectSizeY)*imageSizeX/glb.rectSizeY)  # calcul de quel endroit on doit prendre dans l'image pour afficher les texture en fonction de quel endroit Y sur le mur le rayon touche

    else:  # si on a touché un mur parallel à l'axe Y
        Ximage = int((rayX % glb.rectSizeX)*imageSizeX/glb.rectSizeX)  # calcul de quel endroit on doit prendre dans l'image pour afficher les texture en fonction de quel endroit X sur le mur le rayon touche
    debut = time.time()
    if (Ximage+RectLarg)>imageSizeX:  # teste si on arrive trops loin sur l'image donc qu'on veut prendre une partie qui n'existe par sur l'image
        mur = imageMur.subsurface((Ximage, 0, imageSizeX-Ximage, imageSizeY))  # coupe l'image pour avoir que la dernière partie possible de la taille d'un rectangle dans l'image
    else:
        mur = imageMur.subsurface((Ximage, 0, RectLarg, imageSizeY))  # coupe l'image pour avoir que la partie qui nous intéresse
    #screen.blit(mur, (600, 600))

    mur = pygame.transform.scale(mur, (int(RectLarg), int(RectLong)))   # change la taille de l'image obtenu plus c'est loin plus c'est petit

    #pygame.draw.rect(screen,Grey,(600,600,500,500))
    #screen.blit(mur, (600, 600))
    glb.screen.blit(mur, (iray*RectLarg, RectY))  # affiche l'image
    #pygame.draw.rect(screen, (coul, coul, coul), (iray*RectLarg, RectY, RectLarg, RectLong))