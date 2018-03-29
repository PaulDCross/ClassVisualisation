import pygame
import random


class GridTree(object):
    """ """
    def __init__(self, space, cell_width):
        # space is given as a list of the coordinates that make up a rectangle
        # [x1, y1, x2, y2]
        self.space = space
        # cell_width is the number of cells per 100 pixels.
        # A cell_width of 10 would create cells of size 10x10
        self.cell_width = cell_width
        self.cells = []
        self.Xs = []
        self.Ys = []

        self.initialise_tree()

    def initialise_tree(self):
        number_of_cells_x = (self.space[2]-self.space[0])/self.cell_width
        number_of_cells_y = (self.space[3]-self.space[1])/self.cell_width

        self.cells = [[Cell(self.cell_width*i, self.cell_width*j, self.cell_width*i+self.cell_width, self.cell_width*j+self.cell_width)
                       for i in range(number_of_cells_y)] for j in range(number_of_cells_x)]

    def insert(self, point):
        for line in self.cells:
            for cell in line:
                if cell.contains(point):
                    return True

    def query_range(self, query_cell):
        points_in_range = []
        for line in self.cells:
            for cell in line:
                if not cell.intersects(query_cell):
                    continue
                else:
                    for point in cell.points:
                        if query_cell.contains(point):
                            points_in_range.append(point)
        return points_in_range

    def show(self, frame):
        for line in self.cells:
            for cell in line:
                cell.show(frame)


class Cell(object):
    def __init__(self, x1, y1, x2, y2):
        # self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.colour = (0, 0, 0)
        # self.point_colour = [255-c for c in self.colour]
        self.point_colour = (255, 0, 0)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.points = []

    def contains(self, p):
        if self.x1 <= p.x <= self.x2 and self.y1 <= p.y <= self.y2:
            self.points.append(p)
            return True
        else:
            return False

    def intersects(self, rectangle):
        return ((self.x2 > rectangle.x1) and
                (self.x1 < rectangle.x2) and
                (self.y1 < rectangle.y2) and
                (self.y2 > rectangle.y1))

    def show(self, frame):
        pygame.draw.rect(frame, self.colour, (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1), 1)
        for point in self.points:
            pygame.draw.circle(frame, self.point_colour, (int(point.x), int(point.y)), 2, 0)


class Point(object):
    """docstring for point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

