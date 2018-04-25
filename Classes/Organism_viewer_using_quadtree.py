import pygame
import numpy as np
import random
import OrganismClass as o


def random_position():
    return [random.randint(0 + wall, dd[0] - wall), random.randint(0 + wall, dd[1] - wall)]


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

dd = [1200, 1000]
gameDisplay = pygame.display.set_mode(dd)
pygame.display.set_caption('Vehicles')
pygame.display.update()

gameExit = False
onePressed = False
threePressed = False
fourPressed = False
fivePressed = False
clock = pygame.time.Clock()
fps = 50
wall = 25
system = o.Organisms(gameDisplay, [0 + wall, dd[0] - wall, 0 + wall, dd[1] - wall])
food_list = [o.Food(random_position(), 0.2) for i in xrange(50)]
poison_list = [o.Food(random_position(), -0.5) for j in xrange(50)]

[system.addVehicle(o.Organism(random_position())) for n in xrange(10)]

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            gameExit = True
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.__dict__['button'] == 1:
                onePressed = True
            elif event.__dict__['button'] == 3:
                threePressed = True
            elif event.__dict__['button'] == 4:
                fourPressed = True
                system.debugging = True
            elif event.__dict__['button'] == 5:
                fivePressed = True
                system.debugging = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.__dict__['button'] == 1:
                onePressed = False
            elif event.__dict__['button'] == 3:
                threePressed = False
            elif event.__dict__['button'] == 4:
                fourPressed = False
            elif event.__dict__['button'] == 5:
                fivePressed = False

    if threePressed:
        if system.numVehicles<500:
            system.addVehicle(o.Organism(np.array(event.__dict__['pos'])))

    gameDisplay.fill((51, 51, 51))

    for item in food_list:
        item.display(gameDisplay)
    for item in poison_list:
        item.display(gameDisplay)

    system.update(food_list, poison_list)

    if random.random() < 0.2:
        if random.random() < 0.05:
            poison_list.append(o.Food(random_position(), -0.5))
        else:
            food_list.append(o.Food(random_position(), 0.2))

    if system.numVehicles < 1:
        food_list = [o.Food(random_position(), 0.2) for i in xrange(50)]
        poison_list = [o.Food(random_position(), -0.5) for i in xrange(50)]
        system.reset()
        [system.addVehicle(o.Organism(random_position())) for i in xrange(5)]

    pygame.display.update()
    clock.tick(fps)


pygame.quit()
quit()
