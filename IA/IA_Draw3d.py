import IA_globalVariable as glb
import pygame
import time
import math


def rect3d (iray,rayAngle,nb,cote,rayX,rayY,imageMur, col, ligne):  # fonction qui dessine un rectangle correspondant à un rayon
    nb = nb * math.cos(glb.playerAngle - rayAngle)  # enlève le "fish eye" en prenant la longueur du côté adjacent au personage en formant un triangle rectangle avec le rayon en hypoténuse
    RectLong = 1200/nb *110 * glb.reductionEcran  # calcul trouver par tâtonnement pour transformer la distance du rayon en longueur du rectangle

    # regarde si le mur toucher est juste à côté d'une porte
    if cote == 1 :
        signe = math.copysign(1,(glb.playerX-rayX))
        carre= int(ligne*glb.carteSize[0] + (col+signe))  # augmente la colonne du carré touché par le rayon pour avoir le carré ou il peut y avoir posssiblement une porte
        if glb.Carte[carre] == "2":
            mur = glb.murPorte
        else:
            mur = imageMur
    else:
        signe = math.copysign(1, (glb.playerY - rayY))
        carre = int((ligne+signe) * glb.carteSize[0] + col)  # augmente la ligne du carré touché par le rayon pour avoir le carré ou il peut y avoir posssiblement une porte
        if glb.Carte[carre] == "2":  # verifie si il y a une porte
            mur = glb.murPorte
        else:
            mur = imageMur

    imageSizeX = mur.get_width()   # taille X de l'image de base
    imageSizeY = mur.get_height()   # taille Y de l'image de base
    RectY = math.ceil((glb.screenY-RectLong)/2)  # calcul posY du rectangle
    rectLargeBase = glb.listeRectLarge[iray]*imageSizeX/RectLong

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

    mur = pygame.transform.scale(mur, (int(glb.listeRectLarge[iray]), int(RectLong)))
    glb.screen.blit(mur, (math.floor(glb.listeRectPos[iray]), RectY))  # affiche l'image
    if RectLong < (glb.screenY/1.5):
        glb.screen.blit(glb.rectSombre[math.floor(RectLong)][int(glb.listeRectLarge[iray])][0], (math.floor(glb.listeRectPos[iray]), RectY))  # si le rectangle est assez petit on affiche un rectangle sombre

