import pygame
from math import *
import math


screenMulti = 1  # Si on est sur sur un plus petit écran mettre à 0.5
screenX = int(1200*screenMulti)  # taille X de la carte et taille X de la fenêtre divisé par deux (en pixel)
screenY = int(1200*screenMulti)  # taille Y de la carte et taille Y de la fenêtre (en pixel)
playerX = screenX/2+0.5  # Position X du joueur
playerY = screenY/2+0.5  # position Y du joueur
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
nbRay = 1200  # nombre de rayons qu'on envoie
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
vitesse=12  # vitesse joueur
afficherMap=False  # boolean true si la minimap est affiché
process = 0  # temps fps
process2 = 0
listeObjet = [(1, 350, 150), (1, 450, 450), (1, 450, 750), (1, 750, 250), (1, 750, 450), (1, 750, 750), (1, 750, 950), (1, 1050, 950)]  # liste emplacement objet sous forme (objet,posX,posY)
objet2d=[]  # liste des objets qu'on voit
pygame.init()  # initialisation de pygame
screen = pygame.display.set_mode((screenX*2,screenY))  # initialisation de la fenêtre
