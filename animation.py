import time

import globalVariable as glb

import chargement
import pygame
import math
import random
import image
import menu
import objet
import sys

def anim():
    if glb.armeStatus[1] == True and glb.armeStatus[4]<(glb.armeParrametre[glb.armeStatus[0]][0]-glb.armeParrametre[glb.armeStatus[0]][1]): # si on est en animation est que la frame est plus petite que la dernière frame possible à augmenter
        if glb.armeStatus[4]==0: # si on est à la frame 0
            pygame.mixer.Sound.play(glb.armeParrametre[glb.armeStatus[0]][5])  # on joue le son de l'arme
        glb.armeStatus[4] += glb.armeParrametre[glb.armeStatus[0]][1] # on ajoute a la frame l'avancement pour cette arme
        glb.armeStatus[2] = False  # on ne tire plus
    else : #
        glb.armeStatus[4] = 0  # on reste à la frame 0
        glb.armeStatus[2] = False  # on ne tire pas
        glb.armeStatus[1] = False  # on n'est pas en animation
    if glb.armeStatus[3] and glb.sangCurrentFrame<10:  # on à toucher un monstre et qu'on n'est pas à la dernière frame
        glb.sangCurrentFrame += 2 # on ajoute 2 a la frame
        newFrame = pygame.transform.scale(glb.sang[glb.sangCurrentFrame],glb.newSangLong)  # nouvelle image a affiché
        glb.screen.blit(newFrame,glb.posSang)  # affichage de l'image
    else:
        glb.sangCurrentFrame = 0  # on reste à la frame 0
        glb.armeStatus[3] = False  # on ne touche personne
    nb=0
    for element in glb.lObjAnim:  # on parcour la liste des indice des objets  a animé
        frame = glb.listeMonstre[element][3]
        if frame<10:  # si l'animation ne doit pas se terminer
            glb.listeMonstre[element][3] += 0.2  # on ajoute 0.2 à la frame
        else:
            if random.choice([False,False,False,True]):  # 1/4
                glb.listeObjet.append([random.choice([1,5]),glb.listeMonstre[element][1]-5,glb.listeMonstre[element][2]-5,0])  # on drop à l'endroit où est mort le monstre soit un medkit ou une boite de munition
            del glb.lObjAnim[nb] # on suprime l'indice des objets à animé
    nb=0
    for element in glb.statusPorte:  # on parcourt tous les carres sur la carte mais surtout utile pour les porte
        if element[2]:  # si la porte doit être animé
            if element[1] or element[3]:  # si on est entrain de la fermé
                if glb.statusPorte[nb][0] == glb.rectSizeX:  # au 1er ajout de position
                    pygame.mixer.Sound.play(glb.CloseDoorSound)  # on joue le son de la porte qui se ferme
                glb.statusPorte[nb][0] -= 3  # on baisse l'augmentation de la position de 3
                glb.statusPorte[nb][3] = True  # on est entrain de la fermée
                glb.statusPorte[nb][1] = False # on ne peut pas passer
                if glb.statusPorte[nb][0] <= 0: # si on a fini de la fermé
                    glb.statusPorte[nb][0] = 0 # on met l'augmentation de position à 0
                    glb.statusPorte[nb][1] = False  # on ne peut pas passer
                    glb.statusPorte[nb][2] = False  # on arrête de l'animer
                    glb.statusPorte[nb][3] = False  # on n'est plus entrain de la fermée
            else:  # si on veut l'ouvrir
                if glb.statusPorte[nb][0] == 0: # si on est au tout début de l'ouvrir
                    pygame.mixer.Sound.play(glb.OpenDoorSound)  # on joue le son de la porte qui s'ouvre
                glb.statusPorte[nb][0] += 3  # on ajoute 3 à l'augmentation de la position
                if glb.statusPorte[nb][0] >= glb.rectSizeX:  # si on a fini de l'ouvrir
                    glb.statusPorte[nb][0] = glb.rectSizeX
                    glb.statusPorte[nb][1] = True  # on peut passer
                    glb.statusPorte[nb][2] = False  # on arrête de l'animée

        nb+=1
    nb=0

    for element in glb.listeBall:  # on parcourt la liste des rockets
        cosBalle =  math.cos(element[4])  # cosinus de l'angle sur lequel ce déplace la rocket
        sinBalle =  math.sin(element[4])  # sinus de l'angle sur lequel ce déplace la rocket
        anglePlayer = objet.calculAngleObj(element[1]-glb.playerX, element[2]-glb.playerY)  # angle du joueur vers la rocket
        glb.listeBall[nb][1] =glb.listeBall[nb][1]-cosBalle*20  # on calcul sa nouvelle position X dans la direction de l'angle
        glb.listeBall[nb][2] =glb.listeBall[nb][2]-sinBalle*20  # on calcul sa nouvelle position Y dans la direction de l'angle
        ligne = int(glb.listeBall[nb][2] / glb.rectSizeY)  # on calcul la ligne de la rocket
        col = int(glb.listeBall[nb][1] / glb.rectSizeX)  # on calcul la colonne de la rocket
        carre = ligne * glb.carteSize[0] + col  # carre de la rocket
        diffAngle = abs(anglePlayer-element[4])  # différence entre l'angle du joueur vers la Rocket et celui de l'angle
        if diffAngle>glb.pi :  # si la diff est plus grande que pi
            reverse = anglePlayer < element[4]  # si l'angle du joueur est plus petite que celui de la rocket alors on doit renversé l'image
        else :
            reverse = anglePlayer > element[4]  # si l'angle du joueur est plus grande que celui de la rocket alors on doit renversé l'image
        if glb.pi8*9 > diffAngle > glb.pi8*7:  # si on est en face de la rocket
            glb.listeBall[nb][3] = 0  # on met la frame à l'image corespondante
        if glb.pi8*7 > diffAngle > glb.pi8*5 or glb.pi8*11 > diffAngle > glb.pi8*9:  # si on est sur le coté devant de la rocket
            glb.listeBall[nb][3] = 1 + reverse
        if glb.pi8*5 > diffAngle > glb.pi8*3 or glb.pi8*13 > diffAngle > glb.pi8*11:  # si on est sur le coté de la rocket
            glb.listeBall[nb][3] = 3 + reverse
        if glb.pi8*3 > diffAngle > glb.pi8 or glb.pi8*15 > diffAngle > glb.pi8*13: # si on est sur le coté derière de la rocket
            glb.listeBall[nb][3] = 5 + reverse
        if glb.pi8 > diffAngle or glb.pi8*15 < diffAngle:  # si on est derrière la rocket
            glb.listeBall[nb][3] = 7
        if (abs(element[1]-glb.playerX)<25 and abs(element[2]-glb.playerY)<15) \
                or (abs(glb.playerX - (element[1]+cosBalle*20)) < 15 and abs(glb.playerY - (element[2]+sinBalle*20)) < 15) \
                or (abs(glb.playerX - (element[1]+cosBalle*10)) < 15 and abs(glb.playerY - (element[2]+sinBalle*10)) < 15) :
                # verifie si on est touché par la rocket
            glb.playerVie -= 30 # enlève 30 à la vie du joueur
            if glb.playerVie>0: # si on ne meurt pas
                pygame.mixer.Sound.play(glb.injuredSound)  # son de blesssure
            else:
                pygame.mixer.Sound.play(glb.deathSound) # son de mort
            del glb.listeBall[nb] # on suprime la rocket
        elif glb.Carte[carre]=="1":  # si elle touche un mur
            del glb.listeBall[nb]   # suprime la rocket
        nb+=1

    nb = 0
    for element in glb.statusMonstre :  # on parcourt la liste des status de chaque monstre
        if glb.vieMonstre[nb]>0 :  # si il est vivant
            if element[0] and not(element[1]):  # si on est visible du monstre et que il est pas entrain de tirer
                diffTemps = time.time()-element[2]  # calcul le temps depuis le dernier tir
                if diffTemps>element[4] and element[5]==False:  # si il est assez long il tire
                    glb.statusMonstre[nb][1] = True  # en animation de tire
                    glb.statusMonstre[nb][4] = random.randint(2,6)  # aléatoire d'un nouveau temps avant de pouvoir tirer
                    glb.statusMonstre[nb][2] = time.time()  # prend le temps à la quelle il a tiré
            if glb.statusMonstre[nb][1]:  # s'il est entrain de tiré
                frame = glb.listeMonstre[nb][3]
                if frame >=13:  # si on est à la dernière frame
                    glb.statusMonstre[nb][3] = False  # alors on ne tire plus
                    glb.statusMonstre[nb][1] = False  # on arrête l'animation du de tire
                    glb.listeMonstre[nb][3] = 0  # on met la frame à 0
                elif math.floor(frame) == 12 and element[3] == False:  # si il vient de tirer
                    angle = objet.calculAngleObj((glb.playerX - glb.listeMonstre[nb][1]),
                                                 (glb.playerY - glb.listeMonstre[nb][2]))
                                                # calcul angle du monstre jusqu'a nous
                    glb.shootMonstreSound.play()  # joue le son du monstre qui tire
                    glb.listeBall.append([4, glb.listeMonstre[nb][1], glb.listeMonstre[nb][2], 0, angle])  # on ajoute une rocket qui par de la position du monstre avec l'angle calculé
                    glb.statusMonstre[nb][3] = True  # il a tirer
                elif frame==0 :  # si la frame est 0
                    glb.listeMonstre[nb][3] = 11 # on met la frame à celle où il tire
                else:
                    glb.listeMonstre[nb][3] += 0.5 # ajoute 0.5 à la frame
            if element[5] :
                if time.time()-element[2]>2:
                    glb.listeMonstre[nb][1] += element[6][0] * 3
                    glb.listeMonstre[nb][2] += element[6][1] * 3
                    if abs(glb.listeMonstre[nb][1]-element[7][0])<3 and abs(glb.listeMonstre[nb][2]-element[7][1])<3:
                        glb.statusMonstre[nb][5] = False
            else :
                col = int(glb.listeMonstre[nb][1]/glb.rectSizeX)
                ligne = int(glb.listeMonstre[nb][2]/glb.rectSizeY)
                carreBon = True
                while carreBon :
                    carreVerif = True
                    ajoutCol = random.randint(-1, 1)
                    ajoutligne = random.randint(-1, 1)
                    nvoCol = col + ajoutCol
                    nvoLigne = ligne + ajoutligne
                    nvoCarre = int(nvoLigne* glb.carteSize[0] + nvoCol)
                    if ajoutligne != 0 and ajoutCol != 0:
                        carreVerif1 = int(nvoLigne* glb.carteSize[0] + col)
                        carreVerif2 = int(ligne * glb.carteSize[0] + nvoCol)
                        if glb.Carte[carreVerif1] == "1" or glb.Carte[carreVerif1] == "2" or glb.Carte[carreVerif2] != "1" or glb.Carte[carreVerif2] != "2":
                            carreVerif = False
                    if glb.Carte[nvoCarre] != "1" and glb.Carte[nvoCarre] != "2" and carreVerif:
                        carreBon = False
                pointAriver = (nvoCol * glb.rectSizeX + glb.rectSizeX/2, nvoLigne * glb.rectSizeY + glb.rectSizeX/2)
                angle = objet.calculAngleObj(glb.listeMonstre[nb][1]-pointAriver[0], glb.listeMonstre[nb][2]-pointAriver[1])
                glb.statusMonstre[nb][7] = pointAriver
                glb.statusMonstre[nb][5] = True
                glb.statusMonstre[nb][6] = (math.cos(angle), math.sin(angle))
        nb += 1


    if glb.nbMonstreMort == len(glb.listeMonstre):  # si on a tué tout les monstres
        glb.statutPortal[0] = True # alors le portail est actif
    if glb.statutPortal[0]: # si le portail est actif
        glb.statutPortal[1] = (glb.statutPortal[1]+0.5)%5 # on augmente la frame du portal mais reste < 5
    else :
        glb.statutPortal[1] = 6  # mais la frame à 6 donc celle ou il est pas actif
    if glb.playerVie<=0:  # si on meurt
        mort()  # animation mort

def mort():  # animation mort
    listeRectNoir = []  # liste des rectangles pour animation
    for i in range(int(glb.screenX/4)):  # pour le maximum de rayon de 4 pixel
        listeRectNoir.append([i*4,0,4,0])  # pos X,pos Y , largeur, longueur
    verif=True
    nbTerminer = [False]*len(listeRectNoir)  # liste des rectangle dont l'animation est terminé
    while verif:

        for x in range(len(listeRectNoir)):  # pour chaque rectangle
            if listeRectNoir[x][3]<glb.screenY: # si il est plus petit que la taille Y de l'écran
                listeRectNoir[x][3] += random.randint(0,20)  # on ajoute la longueur aléatoirement entre 0 et 20
            else :
                nbTerminer[x] = True  # l'animation est terminé
            pygame.draw.rect(glb.screen, (50,0,0), listeRectNoir[x]) # dissine le rectangle
        for event in pygame.event.get(): # au cas où on veut quitter le jeu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glb.exit = True
                    pygame.quit()  # Si on quitte le jeu
                    sys.exit()
            if event.type == pygame.QUIT:
                print(glb.maxlong)
                pygame.quit()  # Si on quitte le jeu
                sys.exit()
        glb.temps.tick(60)  # met les fps à 60
        pygame.display.flip()  # met à jour l'écran
        if not(False in nbTerminer):  # si il y n'y a pas de False dans la liste
            verif=False  # on arrète l'animation
    pygame.mouse.set_visible(True)  # on fait que la souris soit visible
    verif=True
    while verif:
        quitter = glb.screen.blit(glb.imageQuit,
                                  ((glb.screenX - glb.imageQuit.get_width()) / 2, glb.screenY * 2 / 3 - glb.imageQuit.get_height() / 2))
                                  # on affiche l'image de l'écriture quitter
        restart = glb.screen.blit(glb.imageRestart,
                                  ((glb.screenX - glb.imageRestart.get_width()) / 2, glb.screenY / 3 - glb.imageRestart.get_height() / 2))
                                  # on affiche l'image de l'écriture restart
        for event in pygame.event.get():  # recupère tout les évenement
            if event.type == pygame.MOUSEBUTTONDOWN: # si on a cliqué
                x, y = event.pos # on recupère la position du clic
                if quitter.collidepoint(x, y):  # on regarde si on a cliqué sur quitter
                    glb.exit = True
                    pygame.quit()  # Si on quitte le jeu
                    sys.exit()
                if restart.collidepoint(x, y):  # si on cliqué sur restart
                    chargement.restart()  # on remet à 0 toute les variables
                    nbTerminer = [False] * len(listeRectNoir)  # on met que tout les rectangle on pas fini leur animation
                    while verif :
                        image.f_all(glb.murBrique)  # affiche l'image 3d
                        menu.afficher()  # affiche le HUD
                        for x in range(len(listeRectNoir)):  # pour tout les rectangles
                            if listeRectNoir[x][3] > 0 : # on verifie si il a pas fini leur animation
                                listeRectNoir[x][3] -= random.randint(0, 30)  # on baisse le longueur aléatoirement
                            else:
                                nbTerminer[x] = True  # il a fini so animation
                            pygame.draw.rect(glb.screen, (50, 0, 0), listeRectNoir[x])  # affichage des rectangle au deçu de l'image 3d
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    glb.exit = True
                                    pygame.quit()  # Si on quitte le jeu
                                    sys.exit()
                            if event.type == pygame.QUIT:
                                pygame.quit()  # Si on quitte le jeu
                                sys.exit()
                        pygame.display.flip()
                        if not (False in nbTerminer):  # si tout les rectangle on fini leur animation
                            verif = False  # on termine la boucle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    glb.exit = True
                    pygame.quit()  # Si on quitte le jeu
                    sys.exit()
            if event.type == pygame.QUIT:
                print(glb.maxlong)
                pygame.quit()  # Si on quitte le jeu
                sys.exit()
        glb.temps.tick(60)
        pygame.display.flip()
