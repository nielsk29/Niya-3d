import globalVariable as glb
import pygame
import time
import math


def rect3d (iray,rayAngle,nb,cote,rayX,rayY,imageMur, col, ligne):  # fonction qui dessine un rectangle correspondant à un rayon
    debut = time.time()
    nb = nb * math.cos(glb.playerAngle - rayAngle)  # enlève le "fish eye" en prenant la longueur du côté adjacent au personage en formant un triangle rectangle avec le rayon en hypoténuse
    if nb!=0:
        RectLong = 1200/nb *110 * glb.reductionEcran  # calcul trouver par tâtonnement pour transformer la distance du rayon en longueur du rectangle
    else:
        RectLong = glb.lenListe-1
    if RectLong>glb.maxlong:
        glb.maxlong=RectLong
    if RectLong>=glb.lenListe:
        RectLong=glb.lenListe-1
    #mur = glb.listeImage[math.floor(RectLong)]
    if cote == 1 :
        signe = math.copysign(1,(glb.playerX-rayX))
        carre= int(ligne*glb.carteSize[0] + (col+signe))
        if glb.Carte[carre] == "2":
            mur = glb.murPorte
        else:
            mur = imageMur
    else:
        signe = math.copysign(1, (glb.playerY - rayY))
        carre = int((ligne+signe) * glb.carteSize[0] + col)
        if glb.Carte[carre] == "2":
            mur = glb.murPorte
        else:
            mur = imageMur
    imageSizeX = mur.get_width() - 1  # taille X de l'image de base
    imageSizeY = mur.get_height() - 1  # taille Y de l'image de base
    RectY = math.ceil((glb.screenY-RectLong)/2)  # calcul posY du rectangle
    #print(RectY, imageSizeY)
    coul= abs(int(nb*250/2400))  # couleur pour dégrader
    #mur = pygame.transform.scale(imageMur, (int(RectLong), int(RectLong)))
    rectLargeBase = glb.RectLarg*imageSizeX/RectLong

    if cote ==1:  # si on a touché un mur parallel à l'axe X
        if rayX > glb.playerX:
            Ximage = ((rayY % glb.rectSizeY)*imageSizeY)/glb.rectSizeY  # calcul de quel endroit on doit prendre dans l'image pour afficher les texture en fonction de quel endroit Y sur le mur le rayon touche
        else:
            Ximage = (abs((rayY % glb.rectSizeY)-glb.rectSizeY) * imageSizeY) / glb.rectSizeY
    else:  # si on a touché un mur parallel à l'axe Y
        if rayY>glb.playerY:
            Ximage = (abs((rayX % glb.rectSizeX)-glb.rectSizeX) * imageSizeX / glb.rectSizeX)
        else:
            Ximage = ((rayX % glb.rectSizeX)*imageSizeX/glb.rectSizeX)  # calcul de quel endroit on doit prendre dans l'image pour afficher les texture en fonction de quel endroit X sur le mur le rayon touche
    if (Ximage+rectLargeBase)>imageSizeX:  # teste si on arrive trops loin sur l'image donc qu'on veut prendre une partie qui n'existe par sur l'image

        mur = mur.subsurface((0, 0, math.ceil(rectLargeBase), imageSizeY))  # coupe l'image pour avoir que la dernière partie possible de la taille d'un rectangle dans l'image
    else:
        mur = mur.subsurface((Ximage, 0, math.ceil(rectLargeBase), imageSizeY))  # coupe l'image pour avoir que la partie qui nous intéresse
    #screen.blit(mur, (600, 600))
    mur = pygame.transform.scale(mur, (int(glb.RectLarg), int(RectLong)))
    #mur = pygame.transform.scale(mur, (int(glb.RectLarg), int(RectLong)))   # change la taille de l'image obtenu plus c'est loin plus c'est petit
    #pygame.draw.rect(screen,Grey,(600,600,500,500))
    #screen.blit(mur, (600, 600))
    glb.screen.blit(mur, (math.floor(iray*glb.RectLarg), RectY))  # affiche l'image
    #sombre = pygame.Color(0,0,0)
    debut = time.time()
    if RectLong < (glb.screenY/1.5):
        glb.screen.blit(glb.rectSombre[int(RectLong)][0], (iray*glb.RectLarg, RectY))
    glb.process3 += time.time() -debut
    #pygame.draw.rect(screen, (coul, coul, coul), (iray*RectLarg, RectY, RectLarg, RectLong))
