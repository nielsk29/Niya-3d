
import globalVariable as glb
import Rayon
import Map2d
import test
import objet
import Draw3d
import pygame
import sys
import math
import time


def f_all(murBrique):  # fonction qui regroupe tout pour créer une image
    glb.process2 = 0
    debut=time.time()  # debut du temps pour calculer les fps
    pygame.draw.rect(glb.screen, glb.Grey, (0, 0, glb.screenX*2, glb.screenY / 2)) # créer un rectangle pour le ciel
    pygame.draw.rect(glb.screen, glb.darkGrey, (0, glb.screenY / 2, glb.screenX*2, glb.screenY / 2)) # créer un rectangle pour le sol
    Rayon.rays(murBrique)  # utilise la fonction qui envoie les rayons et puis créer les murs

    #objet(listeObjet)
    #drawObjet2d(objet2d)
    glb.objet2d=[]
    if glb.afficherMap:  # pour savoir si la MiniMap doit être affiché
        Map2d.drawMap2D(glb.sizeMmap, glb.sizeMmap)  # utilise la fonction qui créer la MiniMap
    glb.process = time.time() - debut    #fin chronomètre pour savoir le temps que prend une seul image à être affiché
    textFPS = font.render(str(int(1/glb.process)), True,(0,0,0)) # créer l'image du chiffre des fps
    temps3d = font.render(str(glb.process2), True, (0, 0, 0))
    frame = font.render(str(glb.process), True,(0,0,0))
    glb.screen.blit(textFPS, (10, 30))
    glb.screen.blit(frame,(10,100)) # affiche l'image des FPS
    glb.screen.blit(temps3d, (10, 170))

murBrique = pygame.image.load("wall_bricks4.jpg")  # image des murs
tauneau = pygame.image.load("tauneau.png")  # image Objet

font = pygame.font.SysFont('freesansbold.ttf', 90)  # Police pour les textes
temps = pygame.time.Clock()  # Initialisation temps
f_all(murBrique)  # créer la 1ère image
while True:  # boucle infinie jusqu'a qu'on quitte le jeu
    f_all(murBrique)  # création de l'image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                                # Si on quitte le jeu
            sys.exit()

    keys = pygame.key.get_pressed()  # variable des touches presser
    if keys[pygame.K_d]:  # si on appuie sur le "d"
        glb.playerAngle = (glb.playerAngle+0.1)%glb.pi2  # on augmente l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
    if keys[pygame.K_q]: # si on appuie sur le q
        glb.playerAngle = (glb.playerAngle-0.1)%glb.pi2 # on réduit l'angle à la quel regarde le joueur et on le fait rester plus petit que 2pi
    if keys[pygame.K_s]: # si on appuie sur le "s"
        playerCol = int((glb.playerX + math.cos(glb.playerAngle) * glb.vitesse*3) / glb.rectSizeX)  # on regarde la colonne ou va aller le joueur s'il recule
        playerLigne = int((glb.playerY + math.sin(glb.playerAngle) * glb.vitesse*3) / glb.rectSizeY)  # on regarde la ligne ou va aller le joueur s'il recule
        playerCarre = playerLigne * glb.carteSize[0] + playerCol  # grâce à la colonne et la ligne on peut savoir le carré ou il va aller
        if glb.Carte[playerCarre] != "1":  # si le carré où il va aller n'est pas un mur
            # on augmente la position X du joueur du cosinus de son angle (* la vitesse) ou il regarde donc s'il regarde vers la droite le cosinus sera négatif donc le X va baisser
            glb.playerX += math.cos(glb.playerAngle) * glb.vitesse
            # on fait la même chose pour le Y mais on l'augmente avec le sinus de l'angle à la quel regarde le joueur
            glb.playerY += math.sin(glb.playerAngle) * glb.vitesse
    if keys[pygame.K_z] : # si on appuie sur le "z"

        # On fait la même chose sauf qu'au lieu d'augmenter du cosinus ou le sinus on le soustraie le cosinus ou le sinus

        playerCol=int((glb.playerX-math.cos(glb.playerAngle) * glb.vitesse*3)/glb.rectSizeX)
        playerLigne=int((glb.playerY-math.sin(glb.playerAngle) * glb.vitesse*3)/glb.rectSizeY)
        playerCarre=playerLigne*glb.carteSize[0] + playerCol
        if glb.Carte[playerCarre]!="1":
            glb.playerX -= math.cos(glb.playerAngle) * glb.vitesse
            glb.playerY -= math.sin(glb.playerAngle) * glb.vitesse
    if keys[pygame.K_TAB]:  # Si la touche "TAB" est pressé

            glb.afficherMap = not glb.afficherMap  # on inverse le boléen qui permet d'afficher la Minimap

    mapplayerX = glb.playerX * glb.minimap / glb.screenX  # calcul de la position X du joueur dans la MiniMap
    mapplayerY = glb.playerY * glb.minimap / glb.screenY  # calcul de la position Y du joueur dans la MiniMap
    pygame.display.flip()  # mets à jour la fenêtre donc affiche la frame


