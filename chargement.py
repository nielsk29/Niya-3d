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
                           (20, -0.5, 20, 1000)]  # Munitions
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
