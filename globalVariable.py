import pygame
from math import *
import math
import sys
import chargement
import os


                # Se fichier va servir à stocké les variable global pour tout les autres fichier


os.getcwd()
screenMulti = 1  # Si on est sur sur un plus petit écran mettre à 0.5

pygame.init()  # initialisation de pygame
pygame.mixer.init(44100, -16, 2, 2048)
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)  # initialisation de la fenêtre
screenX, screenY = screen.get_size() # taille X de la carte et taille X de la fenêtre divisé par deux (en pixel)
millieuX = screenX/2  #millieu X de l'ecran
print(screenX,screenY)
reductionEcran = screenX/2560  # valleur qui change les certain paramètre en fonction de la taille de l'écran car tout les paramètre sont pour l'écran de chze moi de 2560
gameX = 2100  #taille X de la carte
gameY = 2000  #taille Y de la carte
playerX = 200 # Position X du joueur
playerY = 300  # position Y du joueur
diagonal= int(sqrt(gameX**2+gameY**2)) # diagonal de la carte utile pour le nombre maximum de pixel que peut parcourir le rayon (en pixel)
carteSize = (21, 20)  # taille X et Y de la carte (en carré)
diagCarre=int(carteSize[0]*2)  # diagonal de la carte utile pour le nombre maximum de carré que peut parcourir le rayon (en pixel)
rectSizeX = gameX/carteSize[0]  # taille X d'un carré (en pixel)
rectSizeY = gameY/carteSize[1]  # taille Y d'un carré (en pixel)
precision = 0.00001  # pour pas avoir des nombres avec trops de virgule
pi=(math.pi // precision) * precision  # récupération de pi pour gagner du temps
playerAngle = pi/2  # angle à la quel regarde le joueur
angleRegard = pi/4  # angle que l'on rajoute et soustrais à l'angle du joueur pour savoir sur quel intervalle d'angle on doit envoyer les rayons
pi2=pi*2  # 2pi
pi8 = pi/8
nbRay =int(screenX/2) # nombre de rayons qu'on envoie
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
         "101000000000000000121"#6               # carte avec 1 = mur / 0 = rien / 2 = Porte / 3 = portail de fin 
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
         "100000000101000000311"#17
         "100000000121111111101"#18
         "111111111111111111111")#20
         #;1;3;5;7;9;1;3;5;7;9;
nbPorte = Carte.count('2')  # nombre de porte
nbPortal = Carte.count('3')  # nombre de portail

listeObjet = [[1, 350, 150,0],  [1, 1950, 1850,0],  [5, 550, 350,0]]        # liste emplacement objet sous forme [indice dans la liste des image,posX,posY, frame]
listeMonstre = [[0, 150, 1350,0 ],  [0, 850, 1350,0 ],
               [0, 150, 1850,0 ],  [0, 350, 1650,0 ],  [0, 350, 1150,0 ],
               [0, 650, 950,0 ],  [0, 1750, 550,0 ],  [0, 1850, 750,0 ],        # liste emplacement monstre sous forme [indice dans la liste des image,posX,posY, frame]
               [0, 1750, 350,0 ],  [0, 1750, 150,0 ],  [0, 1550, 1250,0 ],
               [0, 1650, 1250,0 ],  [0, 1550, 1350,0 ],  [0, 1650, 1350,0 ]]

listeBall = []  #liste des rocket sur la carte sous forme [indice dans la liste des image,posX,posY, frame, angle avec lequel il se dirige]
statusPorte=[]  # liste de chaque carre sur la carte mais surtout utile pour les portes
for element in Carte:
    if element=="2":
        statusPorte.append([0,False,False,False])  # [ajout position, si on peut passer, en animation, entrain d'être fermé]
    else:
        statusPorte.append([0,True,False,False])

statutPortal = [False,0]  # status portail de fin sous forme [ouvert, frame]
sizeMmap=int(screenX/100)  # taille carré minimap
minimap = (sizeMmap*carteSize[0], sizeMmap*carteSize[1])  # taille minimap en total
darkGrey = (100, 100, 100)
Grey = (50, 50, 50)
mapPlayerX = playerX * minimap[0] / gameX  # emplacement X sur la minimap du joueur
mapPlayerY = playerY * minimap[1] / gameY  # emplacement Y sur la minimap du joueur
vitesse=6  # vitesse joueur
varVitesse = 1  # multiplicateur de la vitesse
afficherMap=False  # boolean true si la minimap est affiché
process = 1  # temps fps
process2 = 0
process3 = 0
pygame.mouse.set_visible(False)  # n'affiche pas la souris

listeParametreObjet = [(50,2.50, 100,100), #Monstre
                       (20,-0.75, 25,1000), #Kit de soin
                       (100,2, 110,1000), #Porte
                       (100,2, 110,1000), #Porte à l'envers
                       (10,3, 13,1000), # Balle monstre
                       (20,-0.5, 20,1000),#Munitions
                       (50,2, 110,1000)]
                        #(largeur sur map, coeff hauteur, coeff taille, vie )

vieMonstre = []  #liste de la vie de chaque monstre
statusMonstre = []  #status de chaque monstre
nbMonstreMort = 0   #nombre de monstre mort
lObjAnim = []  #liste monstre à animé pour sa mort
for element in listeMonstre:
    statusMonstre.append([False, False, 0,False,0, False, [0,0], [0,0]])  #[visible, animation tir, temps dernier tir, à tirer, attente prochain tir, en mouvement, direction(cos,sin), point arriver]
    vieMonstre.append(listeParametreObjet[element[0]][3])  #vie
objet2d=[]  # liste des objets qu'on voit
maxlong = 0
nbballes = 30   #nombre de balle dans le pistolet
playerVie = 100  #vie du joueur qui sera <=100

imageQuit = pygame.image.load("image/text/quit.png")
imageRestart = pygame.image.load("image/text/restart.png")
imageReprendre = pygame.image.load("image/text/reprendre.png")              #chargement des image utilisé
imageQuitter = pygame.image.load("image/text/quitter.png")
ballesimg = pygame.image.load("image/balles.png")
murPorte = pygame.image.load("image/cotePorte.png")
murBrique = pygame.image.load("image/wall.png")  # image des murs

injuredSound = pygame.mixer.Sound("sound/injured.wav")
OpenDoorSound = pygame.mixer.Sound("sound/doorOpen.wav")        #chargement des sons utilisé
CloseDoorSound = pygame.mixer.Sound("sound/doorClose.wav")
deathSound = pygame.mixer.Sound("sound/Death.wav")
shootMonstreSound = pygame.mixer.Sound("sound/shootMonster.wav")
hitDemonSound = pygame.mixer.Sound("sound/HitDemon.wav")
ammoSound = pygame.mixer.Sound("sound/ammo.wav")
medkitSound = pygame.mixer.Sound("sound/medkit.wav")

shootMonstreSound.set_volume(0.8)
deathSound.set_volume(0.3)
hitDemonSound.set_volume(0.3)           # baisse volume des sons
injuredSound.set_volume(0.5)
OpenDoorSound.set_volume(0.3)
CloseDoorSound.set_volume(0.3)

armeImage = [[pygame.image.load("image/gun.gif")]*17,[pygame.image.load("image/poing/frame-1.gif")]*4]  #chargement image de base des armes
armeStatus = [0,False,False,False,1]  #[arme, animation, tirer, toucher, frame]
armeTaille = [[(int(armeImage[0][0].get_width()*screenX/2000),int(armeImage[0][0].get_height()*screenY/1000))]*12,
              [(int(armeImage[1][0].get_width()*screenX/400),int(armeImage[1][0].get_height()*screenY/200))]*4]  #taille de chaque arme sur l'écran
armeParrametre = [[10,1.25,1000000,1,15, pygame.mixer.Sound("sound/gunSound.wav")],
                  [4,0.5,100,0,25, pygame.mixer.Sound("sound/punch.wav")]]
                #[nbFrame, avancement de chaque frame en animation, distMax à laquel on peut toucher, son quand on appuie]
posArme = [[(screenX/2-armeTaille[0][0][0]/2,screenY-armeTaille[0][0][1])]*12, [(screenX*3/4-armeTaille[1][0][0]/2,screenY-armeTaille[1][0][1])]*4]
armeParrametre[0][5].set_volume(0.3)
armeParrametre[1][5].set_volume(0.3)

viseur = pygame.image.load("image/viseur.png")
posViseur = ((screenX-viseur.get_width())/2,(screenY-viseur.get_height())/2)

sang = [pygame.image.load("image/sang.gif")]*12 # image de base du sang
sangLongX = sang[0].get_width()     #taille X de l'image du sang
sangLongY = sang[0].get_height()    #taille Y de l'image du sang
newSangLong = (0,0)  #taille sang fait en fonction de ladistance du monstre toucher
posSang = (int((screenX-sangLongX)/2),int((screenY-sangLongY)/2)) #position sang
sangCurrentFrame = 0  #frame actuel du sang

nbmedkit = 0  # nombre de medkit que porte le joueur
imageRocket = [pygame.image.load("image/rocket/face.png"),
               pygame.image.load("image/rocket/coteFace.png"),pygame.image.load("image/rocket/coteFaceReverse.png"),
               pygame.image.load("image/rocket/cote.png"),pygame.image.load("image/rocket/coteReverse.png"),            #chargement de toute les images de la rocket en fonction de où on la regarde
               pygame.image.load("image/rocket/coteBack.png"),pygame.image.load("image/rocket/coteBackReverse.png"),
               pygame.image.load("image/rocket/Back.png")]
imagePortal = []
for x in  range(1,7):

    nameFrame = "image/portal/frame-"+str(x)+".gif"
    imagePortal.append(pygame.image.load(nameFrame))

listeImageOBJ = [[pygame.image.load("image/demon.gif")],
                 [pygame.image.load("image/kit.png")],
                 [pygame.image.load("image/door.gif")],                 #liste des image de tout les objets
                 [pygame.image.load("image/doorReverse.png")],
                 imageRocket,
                 [pygame.image.load("image/munitions.png")],
                 imagePortal]  # image Objet

for x in range(1,11):
    nameFrame = "image/cyberdemon/death/frame-" + str(x) + ".gif"  #chargement des frames des monstres quand ils meurent
    listeImageOBJ[0].append(pygame.image.load(nameFrame))
for x in range(1,3):
    nameFrame = "image/cyberdemon/tir/frame-" + str(x) + ".gif"     #chargment des frames des monstre quand ils tirent
    listeImageOBJ[0].append(pygame.image.load(nameFrame))

font = pygame.font.SysFont('freesansbold.ttf', 90)  # Police pour les textes
temps = pygame.time.Clock()  # Initialisation temps

nbcharg = (screenX/3.2,screenY/2,screenX/3,screenY/12)
pygame.draw.rect(screen,(255,255,255),(0,0,screenX,screenY))
pygame.draw.rect(screen,(0,0,0),nbcharg,10)
charg = font.render("CHARGEMENT", True,(0,0,0))
screen.blit(charg,(screenX/2-300,screenY/2-100))
pygame.mixer.music.load('sound/music.mp3')
pygame.mixer.music.play(-1)
pygame.display.flip()
listeRectLarge, listeRectPos = chargement.calculPlaceRayonSurEcran()        #utilisation d'une fonction qui va calculer la position et la largeur de chaque rectangle affiché sur l'écran pour chaque rayon
rectSombre = [] # liste des rectangle sombre qui vont être superposé au mur pour donné une impression de profondeur
pause = False  # si le jeu est en pause
for x in range (screenY):
    rectSombre.append([])
    for i in range(math.ceil(max(listeRectLarge)+1)):       # initialisation de la liste de rectangle sombre
        rectSombre[x].append(0)
chargement.charg()  #chargement de beacoup d'image
"""for x in range(3500,6000,500):

    listeImage[x]=(pygame.transform.scale(murBrique, (int(x), int(x))))
    for y in range(1,500):
        listeImage[x+y]=listeImage[x]"""

