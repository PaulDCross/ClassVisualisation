import pygame
import quadtree as qtr
import random

if __name__ == "__main__":

    pygame.init()

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    RED   = (255,0,0)
    GREEN = (0,255,0)
    BLUE  = (0,0,255)

    dd = [600, 600]
    game_display = pygame.display.set_mode(dd)
    pygame.display.set_caption('Quad Tree Test')
    pygame.display.update()

    game_exit = False
    clock = pygame.time.Clock()
    fps = 30
    one_pressed = False
    three_pressed = False


    boundary = qtr.Boundary(300, 300, 300, 300)
    quadtree = qtr.Quad_Tree(boundary, 1)
    points_in_range = []
    rectangle = None
    for i in range(10000):
        p = qtr.Point(int(random.gauss(dd[0]/2, dd[0]/8)), int(random.gauss(dd[1]/2, dd[1]/8)))
        quadtree.insert(p)


    while not game_exit:
        game_display.fill(WHITE)
        quadtree.show(game_display)
        for event in pygame.event.get():
            # print event.__dict__
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                game_exit = True
            # elif event.type == pygame.MOUSEMOTION:
                # mousex, mousey = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.__dict__['button'] == 1:
                    one_pressed = True
                elif event.__dict__['button'] == 3:
                    three_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.__dict__['button'] == 1:
                    one_pressed = False
                elif event.__dict__['button'] == 3:
                    three_pressed = False

        try:
            target = event.__dict__["pos"]
        except:
            pass
        if one_pressed:
            width = 50
            height = 50
            rectangle = qtr.Boundary(target[0], target[1], width/2, height/2)
            points_in_range = quadtree.query_range(rectangle)
        if three_pressed:
            p = qtr.Point(target[0], target[1])
            quadtree.insert(p)

        if not rectangle == None:
            pygame.draw.rect(game_display, (0, 255, 0), (rectangle.x - rectangle.w, rectangle.y - rectangle.h, rectangle.w*2, rectangle.h*2), 1)

        for point in points_in_range:
            pygame.draw.circle(game_display, (0, 255, 0), (point.x, point.y), 2, 0)

        pygame.display.update()
        clock.tick(fps)
        print clock.get_fps()
    pygame.quit()
    quit()
