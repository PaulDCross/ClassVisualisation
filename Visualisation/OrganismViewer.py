import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
import pygame
import numpy as np
import random
import Classes.VehicleClass as v
import Classes.OrganismClass as o

pygame.init()

white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

dd = [600,600]
gameDisplay   = pygame.display.set_mode(dd)
pygame.display.set_caption('Vehicles')
pygame.display.update()

gameExit     = False
onePressed   = False
threePressed = False
clock        = pygame.time.Clock()
fps          = 30
system       = o.Organisms(gameDisplay, [0, dd[0], 0, dd[1]])
foodlist     = o.Foodlist(gameDisplay, 0, dd)
while not gameExit:
    for event in pygame.event.get():
        # print event.__dict__
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            gameExit = True
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.__dict__['button'] == 1:
                onePressed = True
            elif event.__dict__['button'] == 3:
                threePressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.__dict__['button'] == 1:
                onePressed = False
            elif event.__dict__['button'] == 3:
                threePressed = False
    try:
        target = event.__dict__['pos']
    except:
        pass
    if threePressed:
        if system.numVehicles<500:
            system.addVehicle(o.Organism, np.array(event.__dict__['pos']))

    gameDisplay.fill(white)

    system.update(foodlist)
    foodlist.update()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
