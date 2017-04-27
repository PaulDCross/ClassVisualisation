import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
import pygame
import numpy as np
import random
import Classes.VehicleClass as v
import Classes.BoidsClass as b

pygame.init()

white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

dd = [600,600]
gameDisplay   = pygame.display.set_mode(dd)
pygame.display.set_caption('Boids')
pygame.display.update()

gameExit     = False
onePressed   = False
threePressed = False
clock        = pygame.time.Clock()
fps          = 30
system       = b.Boids(gameDisplay, [100, dd[0]-100, 100, dd[1]-100])

while not gameExit:
    for event in pygame.event.get():
        # print event.__dict__
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            gameExit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.__dict__['button'] == 1:
                onePressed = True
            if event.__dict__['button'] == 3:
                threePressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.__dict__['button'] == 1:
                onePressed = False
            if event.__dict__['button'] == 3:
                threePressed = False
    globalTarget = None
    if onePressed == True:
        globalTarget = event.__dict__['pos']
    elif threePressed:
        if system.numVehicles<500:
            system.addVehicle(b.Boid, np.array(event.__dict__['pos']))

    gameDisplay.fill(white)

    system.update(globalTarget)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
