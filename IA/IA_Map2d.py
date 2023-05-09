import IA_globalVariable as glb
import pygame
import math

def drawMap2D(sizeX,sizeY):
    pygame.draw.rect(glb.screen, (0, 0, 0), pygame.Rect(0, 0, sizeX *glb.carteSize[0], sizeY * glb.carteSize[1]))
    glb.mapPlayerX = glb.playerX * glb.minimap[0] / glb.gameX
    glb.mapPlayerY = glb.playerY * glb.minimap[1] / glb.gameY
    for y in range(glb.carteSize[1]):
        for x in range(glb.carteSize[0]):
            rect = y*glb.carteSize[0]+x

            rectX = x * sizeX
            rectY = y * sizeY
            if glb.Carte[rect] == '1':
                pygame.draw.rect(glb.screen, glb.Grey, pygame.Rect(rectX, rectY, sizeX-1, sizeY-1))
            elif glb.Carte[rect] == '2':
                pygame.draw.rect(glb.screen, (0,0,255), pygame.Rect(rectX, rectY, sizeX - 1, sizeY - 1))
            else:
                pygame.draw.rect(glb.screen, glb.darkGrey, pygame.Rect(rectX, rectY, sizeX-1, sizeY-1))
    for r in glb.listeRay:
        pygame.draw.line(glb.screen, (255, 1, 0), r[0],r[1], 1)
    for rond in glb.listeRond:
        if glb.v_2d:
            pygame.draw.circle(glb.screen, rond[1], rond[0], 10)
        else:

            pygame.draw.circle(glb.screen, rond[1], rond[0], 2)
        #pygame.draw.line(glb.screen, (255, 0, 255), rond, (rond[0]+cos(glb.playerAngle+pi/2)*10,rond[1]+sin(glb.playerAngle+pi/2)*10), 1)
        #pygame.draw.line(glb.screen, (0, 255, 255), rond, (rond[0] - cos(glb.playerAngle+pi/2) * 10, rond[1] - sin(glb.playerAngle+pi/2) * 10), 1)
    pygame.draw.circle(glb.screen, (255, 0, 0), (int(glb.mapPlayerX), int(glb.mapPlayerY)), 2)
    pygame.draw.line(glb.screen, (0, 0, 255), (glb.mapPlayerX, glb.mapPlayerY),(glb.mapPlayerX - math.cos(glb.playerAngle) * 10, glb.mapPlayerY - math.sin(glb.playerAngle) * 10),1)
    pygame.draw.line(glb.screen, (0, 255, 255), (glb.mapPlayerX, glb.mapPlayerY), (glb.mapPlayerX - math.cos(glb.playerAngle - glb.angleRegard) * 10,glb.mapPlayerY - math.sin(glb.playerAngle - glb.angleRegard) * 10), 1)
    pygame.draw.line(glb.screen, (0, 0, 255), (glb.mapPlayerX, glb.mapPlayerY), (glb.mapPlayerX - math.cos(glb.playerAngle + glb.angleRegard) * 10,glb.mapPlayerY - math.sin(glb.playerAngle + glb.angleRegard) * 10), 1)


