import pygame
import gridtree as gt
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
    pygame.display.set_caption('Grid Tree Test')
    pygame.display.update()

    game_exit = False
    clock = pygame.time.Clock()
    fps = 60
    one_pressed = False
    three_pressed = False
    state = True
    counter = 0
    # gridtree = gt.GridTree([0, 0, dd[0], dd[1]], 20)
    rectangle = None
    points_in_range = []
    points = []
    # for i in range(1000):
    #     p = gt.Point(random.gauss(dd[0]/2, dd[0]/8), random.gauss(dd[1]/2, dd[1]/8))
    #     gridtree.insert(p)
    #     points.append(p)
    # for j in range((dd[0]/2)-10, (dd[0]/2)+10):
    #     for k in range((dd[1]/2)-10, (dd[1]/2)+10):
    #         p = qtr.Point(j, k)
    #         points.append(p)
    #         quadtree.insert(p)

    while not game_exit:
        # boundary = qtr.Boundary(0, 0, dd[0], dd[1])
        gridtree = gt.GridTree([0, 0, dd[0], dd[1]], 10)
        points = []
        for i in range(1000):
            p = gt.Point(random.gauss(dd[0]/2, dd[0]/8), random.gauss(dd[1]/2, dd[1]/8))
            gridtree.insert(p)
            points.append(p)
        game_display.fill(WHITE)
        gridtree.show(game_display)
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
                    if state:
                        state = False
                        three_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.__dict__['button'] == 1:
                    one_pressed = False
                elif event.__dict__['button'] == 3:
                    if not state:
                        three_pressed = False
                        state = True

        if one_pressed:
            width = 100
            height = 100
            rectangle = gt.Cell(target[0] - width/2, target[1] - height/2, target[0] + width/2, target[1] + height/2)
            points_in_range = gridtree.query_range(rectangle)
        if three_pressed:
            pass
            # p = qtr.Point(target[0], target[1])
            # quadtree.insert(p)
            # three_pressed = False

        if rectangle is not None:
            pygame.draw.rect(game_display, (0, 255, 0), (rectangle.x1, rectangle.y1, rectangle.x2 - rectangle.x1, rectangle.y2 - rectangle.y1), 1)

        for point in points_in_range:
            pygame.draw.circle(game_display, (0, 255, 0), (int(point.x), int(point.y)), 2, 0)

        # for point in points:
        #     if point not in points_in_range:
        #         pygame.draw.circle(game_display, (0, 0, 0), (int(point.x), int(point.y)), 2, 0)

        pygame.display.update()
        clock.tick(fps)
        # counter += 1
        # print "Frame: {}".format(counter)
        print clock.get_fps()
    pygame.quit()
    quit()
