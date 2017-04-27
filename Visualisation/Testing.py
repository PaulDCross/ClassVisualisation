import pygame, random

pygame.init()


white = (255,255,255)
black = (0,0,0)
red   = (255,0,0)
green = (0,255,0)
blue  = (0,0,255)

displayWidth = 600
displayHeight = 600


gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Square')
pygame.display.update()

class squareClass(object):
    """docstring for square"""
    def __init__(self, displayWidth=600, displayHeight=600):
        random.seed()
    def square(self):
        self.width  = 5
        self.height = 5
        self.x = random.randint(0, displayWidth)
        self.y = random.randint(0, displayHeight)
        return (self.x, self.y, self.width, self.height)

    def listOfSquares(self, number=100):
        listed = []
        for a in xrange(100):
            listed.append(self.square())
        return listed

    def squareUpdate(self):
        listed = self.listOfSquares()
        for squares in listed:
            gameDisplay.fill(black, [squares[0], squares[1], squares[2], squares[3]])

def update():
    # gameExit = False
    clock = pygame.time.Clock()
    fps = 1

    gameDisplay.fill(white)
    for event in pygame.event.get():
        # print event
        if event.type == pygame.QUIT:
            break
            # gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
                # gameExit = True

    # pygame.draw.rect(gameDisplay, black, [x, y, width, height])
    squareClass().squareUpdate()

    pygame.display.update()
    clock.tick(fps)

update()
pygame.quit()
quit()
