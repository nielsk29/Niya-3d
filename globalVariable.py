import pygame
from math import *
import math
import sys

screenMulti = 1  # Si on est sur sur un plus petit écran mettre à 0.5
pygame.init()  # initialisation de pygame
pygame.mixer.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  # initialisation de la fenêtre
screenX = int(pygame.display.get_desktop_sizes()[0][0]/2) # taille X de la carte et taille X de la fenêtre divisé par deux (en pixel)
screenY = pygame.display.get_desktop_sizes()[0][1]  # taille Y de la carte et taille Y de la fenêtre (en pixel)
print(screenX,screenY)
gameX = 1200
gameY = 1200
playerX = gameX/2  # Position X du joueur
playerY = gameY/2  # position Y du joueur
diagonal= int(sqrt(gameX**2+gameY**2)) # diagonal de la carte utile pour le nombre maximum de pixel que peut parcourir le rayon (en pixel)
carteSize = (12, 12)  # taille X et Y de la carte (en carré)
diagCarre=int(sqrt(carteSize[0]**2 + carteSize[1]**2))  # diagonal de la carte utile pour le nombre maximum de carré que peut parcourir le rayon (en pixel)
rectSizeX = gameX/carteSize[0]  # taille X d'un carré (en pixel)
rectSizeY = gameY/carteSize[1]  # taille Y d'un carré (en pixel)
precision = 0.00001  # pour pas avoir des nombres avec trops de virgule
pi=(math.pi // precision) * precision  # récupération de pi pour gagner du temps
playerAngle = 0  # angle à la quel regarde le joueur
angleRegard = pi/4  # angle que l'on rajoute et soustrais à l'angle du joueur pour savoir sur quel intervalle d'angle on doit envoyer les rayons
pi2=pi*2  # 2pi
nbRay = int(600) # nombre de rayons qu'on envoie
RectLarg = math.ceil(screenX*2/nbRay)  # calcul de la largeur d'un rectangle de l'affichage 3d
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
darkGrey = (100, 100, 100)
Grey = (50, 50, 50)
mapPlayerX = playerX * minimap / screenX  # emplacement X sur la minimap du joueur
mapPlayerY = playerY * minimap / screenY  # emplacement Y sur la minimap du joueur
vitesse=10  # vitesse joueur
afficherMap=False  # boolean true si la minimap est affiché
process = 0  # temps fps
process2 = 0
process3 = 0
pygame.mouse.set_visible(False)
listeObjet = [(1, 350*screenMulti, 150*screenMulti), (0, 450*screenMulti, 450*screenMulti), (0, 450*screenMulti, 750*screenMulti), (0, 750*screenMulti, 250*screenMulti), (0, 750*screenMulti, 450*screenMulti), (0, 750*screenMulti, 750*screenMulti),(0,850*screenMulti, 850*screenMulti), (0, 750*screenMulti, 950*screenMulti), (0, 1050*screenMulti, 950*screenMulti)]  # liste emplacement objet sous forme (objet,posX,posY)
listeParametreObjet = [(70*screenMulti,2.5, 80),(30*screenMulti,-1, 40)]
objet2d=[]  # liste des objets qu'on voit
maxlong = 0
murBrique = pygame.image.load("image/wall_bricks4.jpg")  # image des murs
viseur = pygame.image.load("image/viseur.png")
posViseur = (screenX-(viseur.get_width()/2),(screenY-viseur.get_height())/2)
gunImage = [pygame.image.load("image/gun.gif")]*17
gunSound = pygame.mixer.Sound("sound/gunSound.mp3")
hitDemonSound = pygame.mixer.Sound("sound/HitDemon.mp3")
hitDemonSound.set_volume(0.3)
tailleGun =(int(gunImage[0].get_width()*screenX/1000),int(gunImage[0].get_height()*screenY/1000))
posGun = (screenX-tailleGun[0]/2,screenY-tailleGun[1])
gunCurrentFrame = 1
gunStatus = False
shoot = False
sang = [pygame.image.load("image/sang.gif")]*12
sangLongX = sang[0].get_width()
sangLongY = sang[0].get_height()
newSangLong = (0,0)
posSang = (screenX-(sangLongX/2),(screenY-sangLongY)/2)
sangCurrentFrame = 0
toucher = False
listeImageOBJ = [pygame.image.load("image/demon.gif"), pygame.image.load("image/kit.png")]  # image Objet
lenListeOBJ = 3000
rectSombre = [0]*screenY
listeDiffImageOBJ = [[0] * lenListeOBJ,[0] * lenListeOBJ]
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
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.play(-1)
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
for x in range(0,int(screenY/1.5)):
    sombre = pygame.Surface((RectLarg, x))
    sombre.set_alpha(int(abs(x*150/(screenY/1.5)-150)))
    sombre.fill((0, 0, 0))
    rectSombre[x] = (sombre,(x,int(abs(x*150/(screenY/1.5)-150)),screenY))
for x in range(0,17):
    nameFrame = "image/gun/frame-"+str(x+1)+".gif"
    image = pygame.image.load(nameFrame)
    gunImage[x] = pygame.transform.scale(image,tailleGun)
for x in range(0,12):
    nameFrame = "image/sang/frame-"+str(x+1)+".gif"
    image = pygame.image.load(nameFrame)
    sang[x] = pygame.transform.scale(image,(sangLongX,sangLongY))
print(gunImage)
"""for x in range(3500,6000,500):

    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    for y in range(1,500):
        listeImage[x+y]=listeImage[x]"""

