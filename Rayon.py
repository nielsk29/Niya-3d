
import globalVariable as glb
import test
import Draw3d
import objet
import math

def rays(murBrique):
    global listeRay, listeRond, test
    print(test.test)
    test.test+=1
    glb.listeRay = []
    dlisteRond = []
    diffRay = (glb.angleRegard*2 / glb.nbRay) // glb.precision * glb.precision
    angleRay = (glb.playerAngle-glb.angleRegard) // glb.precision * glb.precision
    for i in range(glb.nbRay):
        distanceRay=0
        angleRay=(angleRay +diffRay) // glb.precision * glb.precision
        posRayX=glb.playerX
        posRayY=glb.playerY
        pente = -math.tan(angleRay) // glb.precision * glb.precision
        diffPiSur2 = angleRay % (glb.pi / 2)
        cosAngle = math.cos(angleRay) // glb.precision * glb.precision
        sinAngle = math.sin(angleRay) // glb.precision * glb.precision
        for nbCar in range(glb.diagCarre):
            distCarre, posRayX, posRayY, cote = car_affine(pente,cosAngle,sinAngle,diffPiSur2, posRayX, posRayY)
            if cote ==False:
                pixelparpixel(angleRay,i, murBrique)
                break
            distanceRay+=distCarre

            colPosRay = math.floor(posRayX/glb.rectSizeX)
            lignePosRay = math.floor(posRayY/glb.rectSizeY)
            carre=int(lignePosRay*glb.carteSize[0] + colPosRay)

            listeRond.append((posRayX * glb.minimap / glb.screenX, posRayY * glb.minimap / glb.screenY))
            if glb.Carte[carre] == "1":
                glb.listeRay.append((posRayX * glb.minimap / glb.screenX, posRayY * glb.minimap / glb.screenY))
                Draw3d.rect3d(i,angleRay,distanceRay,cote,posRayX,posRayY,murBrique)
                objet.SaveObjet(i, pente, distanceRay, cosAngle, sinAngle)
                break
            """if Carte[carre] == "2":
                if (carre in objCarre) == False:
                    listeObjet.append((i,distanceRay))
                    objCarre.append(carre)"""

def pixelparpixel(angleRay,i, murBrique):
    for nb in range(glb.diagonal):

        posRayX = glb.playerX - math.cos(angleRay) * nb
        posRayY = glb.playerY - math.sin(angleRay) * nb

        colPosRay = math.floor(posRayX / glb.rectSizeX)
        lignePosRay = math.floor(posRayY / glb.rectSizeY)
        carre = int(lignePosRay * glb.carteSize[0] + colPosRay)


        if glb.Carte[carre] == "1":
            if -0.05<(posRayX%glb.rectSizeX)<0.05:
                cote=1
            else:
                cote=2
            Draw3d.rect3d(i, angleRay, nb , cote, posRayX, posRayY, murBrique)
            break
def car_affine(pente,cosAngle,sinAngle,diffPiSur2,posX, posY):

    if diffPiSur2<0.0001 or diffPiSur2>(glb.pi/2 - 0.0001 ):
        return 0,0,0,False

    def f_affine(x):
        return pente*x
    if cosAngle > 0:
        dizainePosX = posX % glb.rectSizeX
        posXtest1 = posX - dizainePosX - 0.05

    else:
        dizainePosX = glb.rectSizeX - posX % glb.rectSizeX
        posXtest1 = posX + dizainePosX + 0.05
    if sinAngle < 0:
        dizainePosY = glb.rectSizeY -posY % glb.rectSizeY
        posYtest2=posY + dizainePosY + 0.05
    else:
        dizainePosY = posY % glb.rectSizeY
        posYtest2 = posY - dizainePosY - 0.05
    fx = dizainePosY / pente // glb.precision * glb.precision
    fy = (f_affine(dizainePosX) // glb.precision) * glb.precision
    #print(fx,fy)
    if cosAngle*sinAngle > 0:
        if sinAngle > 0:
            posXtest2 = posX + fx -0.05
            posYtest1 = posY + fy -0.05
        else:
            posXtest2 = posX - fx +0.05
            posYtest1 = posY - fy +0.05
    else:
        if sinAngle > 0:
            posXtest2 = posX + fx +0.05
            posYtest1 = posY - fy -0.05
        else:
            posXtest2 = posX - fx -0.05

            posYtest1 = posY + fy +0.05


    test1= math.sqrt(fy**2 + dizainePosX**2)
    test2= math.sqrt(fx**2 + dizainePosY**2)
    if test1<test2:
        return test1,posXtest1, posYtest1,1
    else:
        return test2, posXtest2, posYtest2,2

