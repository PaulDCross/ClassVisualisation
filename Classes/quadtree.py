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
    def __init__(self, boundary, capacity, parent=None):
        if 1 < capacity:
            self.NODE_CAPACITY = capacity
        else:
            raise ValueError("Capacity cannot equal 1")

        self.boundary = boundary
        self.parent = parent
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1
            print self.depth
        self.points = []
        self.children = []
        self.divided = False

    def subdivide(self):
        x1 = self.boundary.x1
        y1 = self.boundary.y1
        x2 = self.boundary.x2
        y2 = self.boundary.y2
        if (x2 - x1) <= 1 or (y2 - y1) <= 1:
            return False

        north_east = QuadTree(Boundary(x1+(x2-x1)/2, y1, x2, y1+(y2-y1)/2), self.NODE_CAPACITY, self)
        north_west = QuadTree(Boundary(x1, y1, x1+(x2-x1)/2, y1+(y2-y1)/2), self.NODE_CAPACITY, self)
        south_east = QuadTree(Boundary(x1+(x2-x1)/2, y1+(y2-y1)/2, x2, y2), self.NODE_CAPACITY, self)
        south_west = QuadTree(Boundary(x1, y1+(y2-y1)/2, x1+(x2-x1)/2, y2), self.NODE_CAPACITY, self)

        # Children added based on clockwise rotation.
        self.children = [north_east, south_east, south_west, north_west]

        for point in self.points:
            for child in self.children:
                if child.insert(point):
                    continue

        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.NODE_CAPACITY:
            self.points.append(point)
            return True

        if not self.divided:
            if not self.subdivide():
                self.points.append(point)
                return True

        for child in self.children:
            if child.insert(point):
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

        for child in self.children:
            points_in_range += child.query_range(rectangle)

        return points_in_range

    def show(self, frame):
        for point in self.points:
            pygame.draw.circle(frame, (255, 0, 0), (int(point.x), int(point.y)), 2, 0)
        pygame.draw.rect(frame, (0, 255, 0),
                         (self.boundary.x1, self.boundary.y1,
                          self.boundary.x2 - self.boundary.x1, self.boundary.y2 - self.boundary.y1), 1)
        if self.divided:
            for child in self.children:
                child.show(frame)
