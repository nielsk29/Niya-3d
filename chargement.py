import globalVariable as glb
import pygame
import math
import sys

def charg():
    """for x in range(1,int(glb.screenX/2)):
        glb.listeImage[x]=(pygame.transform.scale( glb.murBrique, (int(x), int(x))))
        longCharg = x * ( glb.nbcharg[2]-30)/  glb.lenTotal
        pygame.draw.rect( glb.screen,(0,0,150),( glb.nbcharg[0]+15, glb.nbcharg[1]+15,longCharg, glb.nbcharg[3]-30))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( glb.maxlong)
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
    for x in range(int(glb.screenX/2), glb.screenX*2,20):
        longCharg = x * ( glb.nbcharg[2] - 30) /  glb.lenTotal
        pygame.draw.rect( glb.screen, (0, 0, 150), ( glb.nbcharg[0] + 15,  glb.nbcharg[1] + 15, longCharg,  glb.nbcharg[3] - 30))
        pygame.display.flip()
        glb.listeImage[x]=(pygame.transform.scale( glb.murBrique, (int(x), int(x))))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( glb.maxlong)
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
        for y in range(1,20):
            glb.listeImage[x+y]= glb.listeImage[x]
    for x in range(glb.screenX*2, glb.lenListe,int( glb.screenX/8)):
        longCharg = x * ( glb.nbcharg[2] - 30) /  glb.lenTotal
        pygame.draw.rect( glb.screen, (0, 0, 150), ( glb.nbcharg[0] + 15,  glb.nbcharg[1] + 15, longCharg,  glb.nbcharg[3] - 30))
        pygame.display.flip()
        glb.listeImage[x]=(pygame.transform.scale( glb.murBrique, (int(x), int(x))))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( glb.maxlong)
                pygame.quit()                                # Si on quitte le jeu
                sys.exit()
        for y in range(1,int( glb.screenX/8)):
             glb.listeImage[x+y]= glb.listeImage[x]
    for x in range(0,1000,3):
        nb = 0
        for element in  glb.listeImageOBJ:
            tailleY = element.get_height()*x/element.get_width()
            longCharg = (x+ glb.lenListe) * ( glb.nbcharg[2] - 30) /  glb.lenTotal
            pygame.draw.rect( glb.screen, (0, 0, 150), ( glb.nbcharg[0] + 15,  glb.nbcharg[1] + 15, longCharg,  glb.nbcharg[3] - 30))
            pygame.display.flip()
            glb.listeDiffImageOBJ[nb][x]=(pygame.transform.scale(element, (int(x), int(tailleY))))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print( glb.maxlong)
                    pygame.quit()                                # Si on quitte le jeu
                    sys.exit()
            for y in range(1,3):
                 glb.listeDiffImageOBJ[nb][x+y]= glb.listeDiffImageOBJ[nb][x]
            nb += 1
    for x in range(1000, glb.lenListeOBJ,50):
        nb = 0
        for element in  glb.listeImageOBJ:
            tailleY = element.get_height()*x/element.get_width()
    
            longCharg = (x+ glb.lenListe) * ( glb.nbcharg[2] - 30) /  glb.lenTotal
            pygame.draw.rect( glb.screen, (0, 0, 150), ( glb.nbcharg[0] + 15,  glb.nbcharg[1] + 15, longCharg,  glb.nbcharg[3] - 30))
            pygame.display.flip()
            glb.listeDiffImageOBJ[nb][x]=(pygame.transform.scale(element, (int(x), int(tailleY))))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print( glb.maxlong)
                    pygame.quit()                                # Si on quitte le jeu
                    sys.exit()
            for y in range(1,50):
                 glb.listeDiffImageOBJ[nb][x+y]= glb.listeDiffImageOBJ[nb][x]
            nb += 1"""
    for x in range(0,int( glb.screenY/1.5)):
        sombre = pygame.Surface(( glb.RectLarg, x))
        sombre.set_alpha(int(abs(x*200/( glb.screenY/1.5)-200)))
        sombre.fill((0, 0, 0))
        glb.rectSombre[x] = (sombre,(x,int(abs(x*150/( glb.screenY/1.5)-150)), glb.screenY))
    for x in range(0,17):
        nameFrame = "image/gun/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.gunImage[x] = pygame.transform.scale(image,glb.tailleGun)
    for x in range(0,12):
        nameFrame = "image/sang/frame-"+str(x+1)+".gif"
        image = pygame.image.load(nameFrame)
        glb.sang[x] = pygame.transform.scale(image,(glb.sangLongX,glb.sangLongY))
