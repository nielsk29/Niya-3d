
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





def f_all(murBrique):
    global process, objet2d,test
    print(test.test)
    test.test += 1
    debut=time.time()
    pygame.draw.rect(glb.screen, glb.Grey, (0, 0, glb.screenX*2, glb.screenY / 2))
    pygame.draw.rect(glb.screen, glb.darkGrey, (0, glb.screenY / 2, glb.screenX*2, glb.screenY / 2))
    Rayon.rays(murBrique)
    #objet(listeObjet)
    #drawObjet2d(objet2d)
    objet2d=[]
    if glb.afficherMap:
        Map2d.drawMap2D(glb.sizeMmap,glb.sizeMmap)
        Map2d.player(glb.sizeMmap)
    process = time.time() - debut
    textAngle = font.render(str(int(1/process)), True,(0,0,0))
    glb.screen.blit(textAngle,(10,30))



murBrique = pygame.image.load("wall_bricks.jpg")
tauneau = pygame.image.load("tauneau.png")

font = pygame.font.SysFont('freesansbold.ttf', 90)
temps = pygame.time.Clock()
f_all(murBrique)
while True:
    f_all(murBrique)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        glb.playerAngle = (glb.playerAngle+0.1)%glb.pi2
    if keys[pygame.K_q]:
        glb.playerAngle = (glb.playerAngle-0.1)%glb.pi2
    if keys[pygame.K_s]:
        playerCol = int((glb.playerX + math.cos(glb.playerAngle) * glb.vitesse*3) / glb.rectSizeX)
        playerLigne = int((glb.playerY + math.sin(glb.playerAngle) * glb.vitesse*3) / glb.rectSizeY)
        playerCarre = playerLigne * glb.carteSize[0] + playerCol
        if glb.Carte[playerCarre] != "1":
            glb.playerX += math.cos(glb.playerAngle) * glb.vitesse
            glb.playerY += math.sin(glb.playerAngle) * glb.vitesse
    if keys[pygame.K_z] :
        playerCol=int((glb.playerX-math.cos(glb.playerAngle) * glb.vitesse*3)/glb.rectSizeX)
        playerLigne=int((glb.playerY-math.sin(glb.playerAngle) * glb.vitesse*3)/glb.rectSizeY)
        playerCarre=playerLigne*glb.carteSize[0] + playerCol
        if glb.Carte[playerCarre]!="1":
            glb.playerX -= math.cos(glb.playerAngle) * glb.vitesse
            glb.playerY -= math.sin(glb.playerAngle) * glb.vitesse
    if keys[pygame.K_TAB]:
        if glb.afficherMap:
            glb.afficherMap=False
        else:
            glb.afficherMap=True
    mapplayerX = glb.playerX * glb.minimap / glb.screenX
    mapplayerY = glb.playerY * glb.minimap / glb.screenY
    pygame.display.flip()
    temps.tick(30)

