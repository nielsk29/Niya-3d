import globalVariable as glb
import pygame
import math
import sys

def charg():        # fonction pour charger certaine image

    # chargement des rectangle sombre possible en fonction de chaque largeur et longueur possible
    for x in range(0,int( glb.screenY/1.5)):    #change la longueur du rectangle jusqu'a une longueur à laquel je ne met plus d'effet sombre
        for long in range (math.floor(min(glb.listeRectLarge)),math.ceil(max(glb.listeRectLarge)+1),1) :    # change la largeur du rectangle du minimum de largeur possilbe au maximum
            sombre = pygame.Surface(( long, x))  #créer le rectangle
            sombre.set_alpha(int(abs(x*200/( glb.screenY/1.5)-200)))    #met la tansparance plus la longueur est grande plus la transaparance est élévé
            sombre.fill((0, 0, 0))   #rempli le rectangle avec du noir
            glb.rectSombre[x][long] = (sombre,(x,int(abs(x*150/( glb.screenY/1.5)-150)), glb.screenY))  # ajout du rectangle à la liste avec comme indice la longueur puis la largeur

    #chargement frame gun
    for x in range(0,12):
        nameFrame = "image/gun/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.armeImage[0][x] = pygame.transform.scale(image,glb.armeTaille[0][x])

    #chargement frame sang
    for x in range(0,12):
        nameFrame = "image/sang/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.sang[x] = pygame.transform.scale(image,(glb.sangLongX,glb.sangLongY))

    #chargment frame poing avec la position du poing
    for x in range(4):
        nameFrame = "image/poing/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.armeTaille[1][x] = (int(image.get_width()*glb.screenX/400),int(image.get_height()*glb.screenY/200))
        glb.armeImage[1][x] = pygame.transform.scale(image, glb.armeTaille[1][x])
        glb.posArme[1][x] = (glb.screenX / 3 - glb.armeTaille[1][x][0] / 2, glb.screenY - glb.armeTaille[1][x][1])


#finction utilisé pour recomancé car remmet toute les variable à leur valleur initial
def restart():
    glb.playerX = 400  # Position X du joueur
    glb.playerY = 300  # position Y du joueur
    glb.playerAngle = glb.pi / 2  # angle à la quel regarde le joueur
    glb.listeRay = []  # liste des rayons qui ce met à jour à chaque image et qui est utilisé pour la minimap
    glb.listeRond = []  # liste des point d'intersection utiliser pour la minimap
    glb.listeObjet = [[1, 350, 150, 0], [1, 1950, 1850, 0],
                  [5, 550, 350, 0]]  # liste emplacement objet sous forme (objet,posX,posY)
    glb.listeMonstre = [[0, 150, 1350, 0], [0, 850, 1350, 0],
                    [0, 150, 1950, 0], [0, 350, 1650, 0], [0, 350, 1150, 0],
                    [0, 650, 950, 0], [0, 1750, 550, 0], [0, 1850, 750, 0],
                    [0, 1750, 350, 0], [0, 1750, 150, 0], [0, 1550, 1250, 0],
                    [0, 1650, 1250, 0], [0, 1550, 1350, 0], [0, 1650, 1350, 0]]
    glb.listeBall = []
    glb.statusPorte = []
    for element in glb.Carte:
        if element == "2":
            glb.statusPorte.append(
                [0, False, False, False])  # [ajout position, si on peut passer, en animation, entrain d'être fermé]
        else:
            glb.statusPorte.append([0, True, False, False])
    glb.mapPlayerX = glb.playerX * glb.minimap / glb.gameX  # emplacement X sur la minimap du joueur
    glb.mapPlayerY = glb.playerY * glb.minimap / glb.gameY  # emplacement Y sur la minimap du joueur
    glb.varVitesse = 1
    glb.afficherMap = False  # boolean true si la minimap est affiché
    glb.process = 1  # temps fps
    glb.process2 = 0
    glb.process3 = 0
    glb.pygame.mouse.set_visible(False)
    glb.listeParametreObjet = [(50, 2.50, 100, 100),  # Monstre
                           (20, -0.75, 25, 1000),  # Kit de soin
                           (100, 2, 110, 1000),  # Porte
                           (100, 2, 110, 1000),  # Porte à l'envers
                           (10, 3, 13, 1000),  # Balle monstre
                           (20, -0.5, 20, 1000),
                            (10, 3, 13, 1000)]  # Munitions
    # (largeur sur map, coeff hauteur, coeff taille, )
    glb.vieMonstre = []
    glb.statusMonstre = []
    glb.lObjAnim = []
    for element in glb.listeMonstre:
        glb.statusMonstre.append(
            [False, False, 0, False, 0])  # [visible, animation tir, temps dernier tir, à tirer, attente prochain tir]
        glb.vieMonstre.append(glb.listeParametreObjet[element[0]][3])
    glb.objet2d = []  # liste des objets qu'on voit
    glb.maxlong = 0
    glb.nbballes = 30
    glb.playerVie = 100
    glb.armeStatus = [0, False, False, False, 1]  # [arme, animation, tirer, toucher, frame]
    glb.newSangLong = (0, 0)
    glb.sangCurrentFrame = 0
    glb.nbmedkit = 0


# fonction qui calcul la position de chaque rectangle sur l'écran en fonction de quel rayon affiche ce rectangle
# pour ce faire on fait semblant qu'il y a un mur qui fait la taille de l'écran devant notre personage puis on tire
# tous les rayons avec le 1er qui touche le début du mur et en fonction d'où il atterrisse on à leur position
# par exemple si le rayon 15 arrive à une distance de 70 pixels du debut du mur alors on met son rectangle à
# une position X de 70
def calculPlaceRayonSurEcran():
    listePlaceRayon = []  # initialisation de la liste qui va avoir la largeur de chaque rectangle
    listeXRayon = []  # initialisation de la liste qui va avoir la pos X de chaque rectangle
    diffRay = (glb.angleRegard * 2 / glb.nbRay)  # diff de radiant entre chaque rayon
    angle = -glb.angleRegard  # angle de départ
    for x in range(glb.nbRay):      # boucle de tous les rayons
        tanAngle = math.tan(angle)  # tan de l'angle
        pos = math.floor(tanAngle*glb.millieuX + glb.millieuX)  # position du rayon
        listeXRayon.append(pos)
        angle = angle + diffRay  # augmentation du rayon
    for x in range(len(listeXRayon)-1):  # boucle pour calculer la largeur de chaque rectangle
        listePlaceRayon.append(listeXRayon[x+1]-listeXRayon[x])  # calcul de la largeur avec la différence entre la pos et la pos du prochain rectangle
    listePlaceRayon.append(glb.screenX - listeXRayon[-1])  # ajout de la dernière largeur car il n'y a pas de rectangle après pour comparer donc on prend la largeur de l'écran
    return listePlaceRayon, listeXRayon
