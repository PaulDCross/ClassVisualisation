import pygame

pygame.init()


white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

displayWidth = 600
displayHeight = 600


gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Slither')
pygame.display.update()

clock = pygame.time.Clock()


gameExit = False
width  = 10
height = width
lead_x = displayWidth/2
lead_y = displayHeight/2
lead_x_change = 0
lead_y_change = 0
step = width
portalWalls = 0
hardWalls = not portalWalls
fps = 10


while not gameExit:
    for event in pygame.event.get():
        # print event
        if event.type == pygame.QUIT:
            gameExit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_change = -step
                lead_y_change = 0
            if event.key == pygame.K_RIGHT:
                lead_x_change = step
                lead_y_change = 0
            if event.key == pygame.K_UP:
                lead_y_change = -step
                lead_x_change = 0
            if event.key == pygame.K_DOWN:
                lead_y_change = step
                lead_x_change = 0
            if event.key == pygame.K_ESCAPE:
                gameExit = True

    lead_x += lead_x_change
    lead_y += lead_y_change

    if hardWalls:
        if lead_x >= displayWidth or lead_x < 0 or lead_y >= displayHeight or lead_y < 0:
            gameExit = True

    if portalWalls:
        if lead_x <= 0:
            lead_x = displayWidth
        if lead_x >= displayWidth:
            lead_x = 0
        if lead_y <= 0:
            lead_y = displayHeight
        if lead_y >= displayHeight:
            lead_y = 0


    # print lead_y, lead_x

    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, width, height])
    # gameDisplay.fill(black, [lead_x, lead_y, width, height])



    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
