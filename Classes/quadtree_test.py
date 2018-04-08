import pygame
import quadtree as qtr
import random

if __name__ == "__main__":
    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    dd = [1000, 1000]
    game_display = pygame.display.set_mode(dd)
    pygame.display.set_caption('Quad Tree Test')
    pygame.display.update()

    game_exit = False
    clock = pygame.time.Clock()
    fps = 100
    one_pressed = False
    three_pressed = False
    state = True
    counter = 0
    boundary = qtr.Boundary(0, 0, dd[0], dd[1])
    quadtree = qtr.QuadTree(boundary, 4)
    rectangle = None
    points_in_range = []
    points = []
    # for i in range(1000):
    #     p = qtr.Point(random.gauss(dd[0]/2, dd[0]/8), random.gauss(dd[1]/2, dd[1]/8))
    #     quadtree.insert(p)
    #     points.append(p)
    # for j in range((dd[0]/2)-10, (dd[0]/2)+10):
    #     for k in range((dd[1]/2)-10, (dd[1]/2)+10):
    #         p = qtr.Point(j, k)
    #         points.append(p)
    #         quadtree.insert(p)

    while not game_exit:
        # boundary = qtr.Boundary(0, 0, dd[0], dd[1])
        quadtree = qtr.QuadTree(boundary, 4)
        points = []
        for i in range(1000):
            p = qtr.Point(random.gauss(dd[0]/2, dd[0]/8), random.gauss(dd[1]/2, dd[1]/8))
            quadtree.insert(p)
            points.append(p)
        game_display.fill(WHITE)
        quadtree.show(game_display)
        for event in pygame.event.get():
            # print event.__dict__
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                game_exit = True
            elif event.type == pygame.MOUSEMOTION:
                target = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.__dict__['button'] == 1:
                    one_pressed = True
                elif event.__dict__['button'] == 3:
                    three_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.__dict__['button'] == 1:
                    one_pressed = False
                elif event.__dict__['button'] == 3:
                    pass

        if one_pressed:
            width = 100
            height = 100
            rectangle = qtr.Boundary(target[0] - width/2, target[1] - height/2, target[0] + width/2, target[1] + height/2)
            points_in_range = quadtree.query_range(rectangle)
            pygame.draw.rect(game_display, GREEN, (rectangle.x1, rectangle.y1, rectangle.x2 - rectangle.x1, rectangle.y2 - rectangle.y1), 1)
            for point in points_in_range:
                pygame.draw.circle(game_display, GREEN, (int(point.x), int(point.y)), 2, 0)

        if three_pressed:
            p = qtr.Point(target[0], target[1])
            quadtree.insert(p)
            points.append(p)
            three_pressed = False

        for point in points:
            if point not in points_in_range:
                pygame.draw.circle(game_display, BLACK, (int(point.x), int(point.y)), 2, 0)

        pygame.display.update()
        clock.tick(fps)
        counter += 1
        # print "Frame: {}".format(counter)
        print clock.get_fps()
    pygame.quit()
    quit()
