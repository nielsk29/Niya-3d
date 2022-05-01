import pygame
from math import *
import math
import sys

screenMulti = 1  # Si on est sur sur un plus petit écran mettre à 0.5
screenX = int(1200*screenMulti)  # taille X de la carte et taille X de la fenêtre divisé par deux (en pixel)
screenY = int(1200*screenMulti)  # taille Y de la carte et taille Y de la fenêtre (en pixel)
playerX = screenX/2  # Position X du joueur
playerY = screenY/2  # position Y du joueur
diagonal= int(sqrt(screenX**2+screenY**2)) # diagonal de la carte utile pour le nombre maximum de pixel que peut parcourir le rayon (en pixel)
carteSize = (12, 12)  # taille X et Y de la carte (en carré)
diagCarre=int(sqrt(carteSize[0]**2 + carteSize[1]**2))  # diagonal de la carte utile pour le nombre maximum de carré que peut parcourir le rayon (en pixel)
rectSizeX = screenX/carteSize[0]  # taille X d'un carré (en pixel)
rectSizeY = screenY/carteSize[1]  # taille Y d'un carré (en pixel)
precision = 0.00001  # pour pas avoir des nombres avec trops de virgule
pi=(math.pi // precision) * precision  # récupération de pi pour gagner du temps
playerAngle = 0  # angle à la quel regarde le joueur
angleRegard = pi/4  # angle que l'on rajoute et soustrais à l'angle du joueur pour savoir sur quel intervalle d'angle on doit envoyer les rayons
pi2=pi*2  # 2pi
nbRay = screenX # nombre de rayons qu'on envoie
RectLarg = screenX*2/nbRay  # calcul de la largeur d'un rectangle de l'affichage 3d
listeRay = []  # liste des rayons qui ce met à jour à chaque image et qui est utilisé pour la minimap
listeRond = []  # liste des point d'intersection utiliser pour la minimap
         #0;2;4;6;8;10
Carte = ("111111111111"#0
         "100200000001"#1
         "101000020001"#2
         "111100001111"#3
         "100020020001"#4
         "100000011111"#5
         "111100010001"#6               # carte avec 1 = mur et 0 = rien
         "100020020011"#7
         "101111002001"#8
         "100001021021"#9
         "100001001001"#10
         "111111111111")#11
         #;1;3;5;7;9;11
sizeMmap=20  # taille carré minimap
minimap = sizeMmap*carteSize[0]  # taille minimap en total
darkGrey = (120, 120, 120)
Grey = (80, 80, 80)
mapPlayerX = playerX * minimap / screenX  # emplacement X sur la minimap du joueur
mapPlayerY = playerY * minimap / screenY  # emplacement Y sur la minimap du joueur
vitesse=10  # vitesse joueur
afficherMap=False  # boolean true si la minimap est affiché
process = 0  # temps fps
process2 = 0
process3 = 0
listeObjet = [(0, 350, 150), (0, 450, 450), (0, 450, 750), (0, 750, 250), (0, 750, 450), (0, 750, 750),(0,850, 850), (0, 750, 950), (0, 1050, 950)]  # liste emplacement objet sous forme (objet,posX,posY)
listeParametreObjet = [(60,3),40]
objet2d=[]  # liste des objets qu'on voit
pygame.init()  # initialisation de pygame
screen = pygame.display.set_mode((screenX*2,screenY))  # initialisation de la fenêtre
maxlong = 0
murBrique = pygame.image.load("wall_bricks4.jpg")  # image des murs
listeImageOBJ = [pygame.image.load("demon.gif")]  # image Objet
lenListeOBJ = 3000
listeDiffImageOBJ = [[0] * lenListeOBJ] * len(listeImageOBJ)
font = pygame.font.SysFont('freesansbold.ttf', 90)  # Police pour les textes
temps = pygame.time.Clock()  # Initialisation temps
lenListe = screenX*5
listeImage=[0]*(lenListe + 50)
lenTotal = lenListe+lenListeOBJ
nbcharg = (screenX/1.6,screenY/2,screenX/1.5,screenX/12)
pygame.draw.rect(screen,(255,255,255),(0,0,screenX*2,screenY))
pygame.draw.rect(screen,(0,0,0),nbcharg,10)

charg = font.render("CHARGEMENT", True,(0,0,0))
screen.blit(charg,(screenX-300,screenY/2-100))
pygame.display.flip()
for x in range(1,screenX):
    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    longCharg = x * (nbcharg[2]-30)/ lenTotal
    pygame.draw.rect(screen,(0,0,150),(nbcharg[0]+15,nbcharg[1]+15,longCharg,nbcharg[3]-30))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(maxlong)
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()
for x in range(screenX,screenX*2,10):
    longCharg = x * (nbcharg[2] - 30) / lenTotal
    pygame.draw.rect(screen, (0, 0, 150), (nbcharg[0] + 15, nbcharg[1] + 15, longCharg, nbcharg[3] - 30))
    pygame.display.flip()
    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(maxlong)
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()
    for y in range(1,10):
        listeImage[x+y]=listeImage[x]
for x in range(screenX*2,lenListe,50):
    longCharg = x * (nbcharg[2] - 30) / lenTotal
    pygame.draw.rect(screen, (0, 0, 150), (nbcharg[0] + 15, nbcharg[1] + 15, longCharg, nbcharg[3] - 30))
    pygame.display.flip()
    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(maxlong)
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()
    for y in range(1,50):
        listeImage[x+y]=listeImage[x]
for x in range(0,1000,2):
    nb = 0
    for element in listeImageOBJ:
        tailleY = element.get_height()*x/element.get_width()

        longCharg = (x+lenListe) * (nbcharg[2] - 30) / lenTotal
        pygame.draw.rect(screen, (0, 0, 150), (nbcharg[0] + 15, nbcharg[1] + 15, longCharg, nbcharg[3] - 30))
        pygame.display.flip()
        listeDiffImageOBJ[nb][x]=(pygame.transform.scale(element, (int(x), int(tailleY))))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(maxlong)
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
        for y in range(1,2):
            listeDiffImageOBJ[nb][x+y]=listeDiffImageOBJ[nb][x]
        nb += 1
for x in range(1000,lenListeOBJ,20):
    nb = 0
    for element in listeImageOBJ:
        tailleY = element.get_height()*x/element.get_width()

        longCharg = (x+lenListe) * (nbcharg[2] - 30) / lenTotal
        pygame.draw.rect(screen, (0, 0, 150), (nbcharg[0] + 15, nbcharg[1] + 15, longCharg, nbcharg[3] - 30))
        pygame.display.flip()
        listeDiffImageOBJ[nb][x]=(pygame.transform.scale(element, (int(x), int(tailleY))))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(maxlong)
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
        for y in range(1,20):
            listeDiffImageOBJ[nb][x+y]=listeDiffImageOBJ[nb][x]
        nb += 1
"""for x in range(3500,6000,500):

    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    for y in range(1,500):
        listeImage[x+y]=listeImage[x]"""

print("fin")
