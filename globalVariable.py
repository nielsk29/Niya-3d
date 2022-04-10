import pygame
from math import *
import math


screenMulti = 1
screenX = int(1200*screenMulti)
screenY = int(1200*screenMulti)
playerX = screenX/2+0.5
playerY = screenY/2+0.5
diagonal=int(sqrt(screenX**2+screenY**2))
carteSize = (12, 12)
diagCarre=int(sqrt(carteSize[0]**2 + carteSize[1]**2))
rectSizeX = screenX/carteSize[0]
rectSizeY = screenY/carteSize[1]
precision = 0.00001
pi=(math.pi // precision) * precision
playerAngle = 0
angleRegard = pi/4
pi2=pi*2
nbRay = 1200
dist3D = 0
listeRay = []
listeRond = []
         #0;2;4;6;8;10
Carte = ("111111111111"#0
         "100200000001"#1
         "101000020001"#2
         "111100001111"#3
         "100020020001"#4
         "100000011111"#5
         "111100010001"#6
         "100020020011"#7
         "101111002001"#8
         "100001021021"#9
         "100001001001"#10
         "111111111111")#11
         #;1;3;5;7;9;11
sizeMmap=20
minimap = sizeMmap*carteSize[0]
darkGrey = (120, 120, 120)
Grey = (80, 80, 80)
mapPlayerX = playerX * minimap / screenX
mapPlayerY = playerY * minimap / screenY
vitesse=12
afficherMap=False
process = 0
listeObjet = [(1, 350, 150), (1, 450, 450), (1, 450, 750), (1, 750, 250), (1, 750, 450), (1, 750, 750), (1, 750, 950), (1, 1050, 950)]
objet2d=[]
test = 2
pygame.init()
screen = pygame.display.set_mode((screenX*2,screenY))
