import pygame


class Point(object):
    """docstring for point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Boundary(object):
    """docstring for rectangle"""
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def contains(self, p):
        return self.x1 <= p.x <= self.x2 and self.y1 <= p.y <= self.y2

    def intersects(self, rectangle):
        return ((self.x2 > rectangle.x1) and
                (self.x1 < rectangle.x2) and
                (self.y1 < rectangle.y2) and
                (self.y2 > rectangle.y1))


class QuadTree(object):
    """docstring for Quad_Tree"""
    def __init__(self, boundary, capacity):
        if 1 < capacity:
            self.NODE_CAPACITY = capacity
        else:
            raise ValueError("Capacity cannot equal 1")

        self.boundary = boundary
        self.points = []
        self.north_east = None
        self.north_west = None
        self.south_east = None
        self.south_west = None
        self.divided = False

    def subdivide(self):
        x1 = self.boundary.x1
        y1 = self.boundary.y1
        x2 = self.boundary.x2
        y2 = self.boundary.y2

        ne = Boundary(x1+(x2-x1)/2, y1, x2, y1+(y2-y1)/2)
        self.north_east = QuadTree(ne, self.NODE_CAPACITY)
        nw = Boundary(x1, y1, x1+(x2-x1)/2, y1+(y2-y1)/2)
        self.north_west = QuadTree(nw, self.NODE_CAPACITY)
        se = Boundary(x1+(x2-x1)/2, y1+(y2-y1)/2, x2, y2)
        self.south_east = QuadTree(se, self.NODE_CAPACITY)
        sw = Boundary(x1, y1+(y2-y1)/2, x1+(x2-x1)/2, y2)
        self.south_west = QuadTree(sw, self.NODE_CAPACITY)

        for point in self.points:
            if self.north_east.insert(point):
                continue
            if self.north_west.insert(point):
                continue
            if self.south_east.insert(point):
                continue
            if self.south_west.insert(point):
                continue

        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            # print "point [{}, {}] outside boundary [{}, {}, {}, {}]".format(point.x, point.y, self.boundary.x1, self.boundary.y1, self.boundary.x2, self.boundary.y2)
            return False

        if len(self.points) < self.NODE_CAPACITY:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        if self.north_east.insert(point) or self.north_west.insert(point) or self.south_east.insert(point) or self.south_west.insert(point):
            return True

        print "Could not add point [{}, {}]".format(point.x, point.y)
        return False

    def query_range(self, rectangle):
        points_in_range = []
        if not (self.boundary.intersects(rectangle)):
            return points_in_range

        for point in self.points:
            if rectangle.contains(point):
                points_in_range.append(point)

        if not self.divided:
            return points_in_range

        points_in_range += self.north_east.query_range(rectangle)
        points_in_range += self.north_west.query_range(rectangle)
        points_in_range += self.south_east.query_range(rectangle)
        points_in_range += self.south_west.query_range(rectangle)

        return points_in_range

    def show(self, frame):
        for point in self.points:
            pygame.draw.circle(frame, (255, 0, 0), (int(point.x), int(point.y)), 2, 0)
        pygame.draw.rect(frame, (0, 255, 0), (self.boundary.x1, self.boundary.y1, self.boundary.x2 - self.boundary.x1, self.boundary.y2 - self.boundary.y1), 1)
        if self.divided:
            self.north_east.show(frame)
            self.north_west.show(frame)
            self.south_east.show(frame)
            self.south_west.show(frame)
