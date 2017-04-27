import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
import pygame
import numpy as np
import random
import Classes.Particle as P

pygame.init()

white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

displayWidth  = 1200
displayHeight = 1000
gameDisplay   = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Particles')
pygame.display.update()

gameExit     = False
onePressed   = False
threePressed = False
clock        = pygame.time.Clock()
fps          = 60
systems      = [P.ParticalSystem(gameDisplay, [random.randint(50, displayHeight-50), random.randint(50, displayWidth-50)]) for i in range(0)]

while not gameExit:
    for event in pygame.event.get():
        print event.__dict__
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            gameExit = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.__dict__['button'] == 1:
                onePressed = True
            if event.__dict__['button'] == 3:
                threePressed = True
            if event.__dict__['button'] == 2:
                systems.append(P.ParticalSystem(gameDisplay, np.array(event.__dict__['pos'])))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.__dict__['button'] == 1:
                onePressed = False
            if event.__dict__['button'] == 3:
                threePressed = False


    number = 0
    gameDisplay.fill(white)
    for system in systems:
        if onePressed == True:
            system.addForce(np.array([0.05, 0]))
        if threePressed:
            system.addForce(np.array([-0.05, 0]))
        system.addParticle()
        system.run()
        number += system.numberofparticles
    # print number
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
