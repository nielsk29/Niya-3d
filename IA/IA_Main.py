import IA_animation
import IA_globalVariable as glb
import IA_mouvement
import IA_menu
import pygame  # permet d'afficher sur dans une fenêtre les elements et de gérer les inputs
import time
import IA_image

# Le programme utilise un algorithme appellé Raycasting pour pouvoir afficher un semblant de 3D mais qui fonctionne
# juste avec la perspective donc que plus un objet est loin plus il est petit. Le Raycasting fonctionne en tirant
# des sortes de rayon qui vont être envoyé à partir de la position de notre joueur et dans la direction de notre
# angle de vision (le 1er sera au plus à gauche de notre angle de vision et le dernier au plus à droite).
# Ils vont se stopper quand ils touchent un mur puis en fonction de la longueur du rayon on peut avoir la distance
# du mur à nous puis en fonction de cette distance on dessine sur l'écran un rectangle très fin qui plus la distance
# est grande plus il est petit on remplie ce rectangle avec une partie de l'image des murs.


while True:  # boucle infinie jusqu'a qu'on quitte le jeu
    debut = time.time()  # debut du temps pour calculer les fps
    IA_mouvement.zqsd()    # change la position et l'angle de vue du joueur si on appuie sur des touches précise
    mapplayerX = glb.playerX * glb.minimap[0] / glb.gameX  # calcul de la position X du joueur dans la MiniMap
    mapplayerY = glb.playerY * glb.minimap[1] / glb.gameY  # calcul de la position Y du joueur dans la MiniMap

    if glb.v_2d:
        IA_image.f_all2d()
    else:
        IA_image.f_all(glb.murBrique)  # création de l'image avec les murs et les objets
        IA_menu.afficher()  # affiche les autres elements de l'image comme la barre de vie ou l'arme du joueur
    IA_animation.anim()  # fait les animations

    glb.process = time.time() - debut  # fin chronomètre pour savoir le temps que prend une seul image à être affiché
    pygame.display.flip()  # mets à jour la fenêtre donc affiche la frame
    glb.temps.tick(30)    # met le maximum de nombre d'images par seconde à 30

