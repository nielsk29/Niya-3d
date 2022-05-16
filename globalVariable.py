import pygame
from math import *
import math
import sys
import chargement

screenMulti = 1  # Si on est sur sur un plus petit écran mettre à 0.5
pygame.init()  # initialisation de pygame
pygame.mixer.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  # initialisation de la fenêtre
screenX, screenY = screen.get_size() # taille X de la carte et taille X de la fenêtre divisé par deux (en pixel)
millieuX = screenX/2
print(screenX,screenY)
reductionEcran = screenX/2560
gameX = 2100
gameY = 2100
playerX = 400 # Position X du joueur
playerY = 300  # position Y du joueur
diagonal= int(sqrt(gameX**2+gameY**2)) # diagonal de la carte utile pour le nombre maximum de pixel que peut parcourir le rayon (en pixel)
carteSize = (21, 21)  # taille X et Y de la carte (en carré)
diagCarre=int(carteSize[0]*2)  # diagonal de la carte utile pour le nombre maximum de carré que peut parcourir le rayon (en pixel)
rectSizeX = gameX/carteSize[0]  # taille X d'un carré (en pixel)
rectSizeY = gameY/carteSize[1]  # taille Y d'un carré (en pixel)
precision = 0.00001  # pour pas avoir des nombres avec trops de virgule
pi=(math.pi // precision) * precision  # récupération de pi pour gagner du temps
playerAngle = pi/2  # angle à la quel regarde le joueur
angleRegard = pi/4  # angle que l'on rajoute et soustrais à l'angle du joueur pour savoir sur quel intervalle d'angle on doit envoyer les rayons
pi2=pi*2  # 2pi
nbRay =int(screenX/4) # nombre de rayons qu'on envoie
RectLarg = math.ceil(screenX/nbRay)  # calcul de la largeur d'un rectangle de l'affichage 3d
listeRay = []  # liste des rayons qui ce met à jour à chaque image et qui est utilisé pour la minimap
listeRond = []  # liste des point d'intersection utiliser pour la minimap


         #0;2;4;6;8;0;2;4;6;8;0
Carte = ("111111111111111111111"#0
         "100000000101000000001"#1
         "100000000100000000001"#2
         "100000000101000000001"#3
         "100000000121000001111"#4
         "121111111101111110001"#5
         "101000000000000000121"#6               # carte avec 1 = mur et 0 = rien
         "101000001101111111001"#7
         "101000000101000000001"#8
         "101000000101000000001"#9
         "101000000101000000001"#10
         "101000000101000000001"#11
         "101111121101000000001"#12
         "100000000101000000001"#13
         "111111211101000000001"#14
         "100000000101000000001"#15
         "100000000101000000001"#16
         "100000000101000000011"#17
         "100000000121111111101"#18
         "100000000100000000001"#19
         "111111111111111111111")#20
         #;1;3;5;7;9;1;3;5;7;9;

listeObjet = [[1, 350, 150,0],  [0, 150, 1350,0 ],  [0, 850, 1350,0 ],
               [0, 150, 1950,0 ],  [0, 350, 1650,0 ],  [0, 350, 1150,0 ],
               [0, 650, 950,0 ],  [0, 1750, 550,0 ],  [0, 1850, 750,0 ],
               [0, 1750, 350,0 ],  [0, 1750, 150,0 ],  [0, 1550, 1250,0 ],
               [0, 1650, 1250,0 ],  [0, 1550, 1350,0 ],  [0, 1650, 1350,0 ],[1, 1950, 1850,0]]        # liste emplacement objet sous forme (objet,posX,posY)
statusPorte=[]
for element in Carte:
    if element=="2":
        statusPorte.append([0,False,False,False])
    else:
        statusPorte.append([0,True,False,False])
sizeMmap=20  # taille carré minimap
minimap = sizeMmap*carteSize[0]  # taille minimap en total
darkGrey = (100, 100, 100)
Grey = (50, 50, 50)
mapPlayerX = playerX * minimap / gameX  # emplacement X sur la minimap du joueur
mapPlayerY = playerY * minimap / gameY  # emplacement Y sur la minimap du joueur
vitesse=8  # vitesse joueur
varVitesse = 1
afficherMap=False  # boolean true si la minimap est affiché
process = 0  # temps fps
process2 = 0
process3 = 0
pygame.mouse.set_visible(False)
listeParametreObjet = [(50,2.50, 100,50),(30,-1, 40,1000),(100,2, 110,1000),(100,2, 110,1000)]
vieObjet = []
lObjAnim = []
for element in listeObjet:
    vieObjet.append(listeParametreObjet[element[0]][3])
print(vieObjet)
objet2d=[]  # liste des objets qu'on voit
maxlong = 0
murPorte = pygame.image.load("image/cotePorte.png")
OpenDoorSound = pygame.mixer.Sound("sound/doorOpen.mp3")
CloseDoorSound = pygame.mixer.Sound("sound/doorClose.mp3")
murBrique = pygame.image.load("image/wall_bricks4.jpg")  # image des murs
viseur = pygame.image.load("image/viseur.png")
posViseur = ((screenX-viseur.get_width())/2,(screenY-viseur.get_height())/2)
gunImage = [pygame.image.load("image/gun.gif")]*17
gunSound = pygame.mixer.Sound("sound/gunSound.mp3")
hitDemonSound = pygame.mixer.Sound("sound/HitDemon.mp3")
hitDemonSound.set_volume(0.3)
tailleGun =(int(gunImage[0].get_width()*screenX/2000),int(gunImage[0].get_height()*screenY/1000))
posGun = (screenX/2-tailleGun[0]/2,screenY-tailleGun[1])
gunCurrentFrame = 1
gunStatus = False
shoot = False
sang = [pygame.image.load("image/sang.gif")]*12
sangLongX = sang[0].get_width()
sangLongY = sang[0].get_height()
newSangLong = (0,0)
posSang = (int((screenX-sangLongX)/2),int((screenY-sangLongY)/2))
sangCurrentFrame = 0
toucher = False
listeImageOBJ = [[pygame.image.load("image/demon.gif")], [pygame.image.load("image/kit.png")],[pygame.image.load("image/door.png")],[pygame.image.load("image/doorReverse.png")]]  # image Objet
for x in range(1,11):
    nameFrame = "image/cyberdemon/death/frame-" + str(x) + ".gif"
    listeImageOBJ[0].append(pygame.image.load(nameFrame))
print(listeImageOBJ)
rectSombre = [0]*screenY
font = pygame.font.SysFont('freesansbold.ttf', 90)  # Police pour les textes
temps = pygame.time.Clock()  # Initialisation temps
lenListe = screenX*4
listeImage=[0]*lenListe
lenTotal = lenListe
nbcharg = (screenX/3.2,screenY/2,screenX/3,screenY/12)
pygame.draw.rect(screen,(255,255,255),(0,0,screenX,screenY))
pygame.draw.rect(screen,(0,0,0),nbcharg,10)
charg = font.render("CHARGEMENT", True,(0,0,0))
screen.blit(charg,(screenX/2-300,screenY/2-100))
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.play(-1)
pygame.display.flip()

chargement.charg()
"""for x in range(3500,6000,500):

    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    for y in range(1,500):
        listeImage[x+y]=listeImage[x]"""

