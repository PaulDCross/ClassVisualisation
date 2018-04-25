import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
import commonLibraries.Vector as v

LEAF_SIZE = 4


class Point(object):
    """docstring for point"""
    def __init__(self, x, y):
        self.pos = v.Vector([x, y])


class Boundary(object):
    """docstring for rectangle"""
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def contains(self, point):
        return self.x1 <= point.pos.x <= self.x2 and self.y1 <= point.pos.y <= self.y2

    def intersects(self, rectangle):
        return ((self.x2 > rectangle.x1) and
                (self.x1 < rectangle.x2) and
                (self.y1 < rectangle.y2) and
                (self.y2 > rectangle.y1))


class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.rSquared = r * r

    def contains(self, point):
        d = pow((point.pos.x - self.x), 2) + pow((point.pos.y - self.y), 2)
        return d <= self.rSquared

    def intersects(self, b):
        width = (b.x2 - b.x1)
        height = (b.y2 - b.y1)

        x_dist = abs((b.x1 + (width/2)) - self.x)
        y_dist = abs((b.y1 + (height/2)) - self.y)

        # Radius of the circle
        r = self.r

        edges = pow((x_dist - width), 2) + pow((y_dist - height), 2)

        # no intersection
        if (x_dist > (r + width)) or (y_dist > (r + height)):
            return False

        # intersection within the circle
        if (x_dist <= width) or (y_dist <= height):
            return True

        # Intersection on the edge of the circle
        return edges <= self.rSquared


class QuadTree(object):
    """docstring for Quad_Tree"""
    def __init__(self, boundary, capacity, depth=0):
        if 1 < capacity:
            self.NODE_CAPACITY = capacity
        else:
            raise ValueError("Capacity cannot equal 1")

        self.boundary = boundary
        self.depth = depth
        # print self.depth
        self.leaf = self.is_leaf()
        self.points = []
        self.children = []
        self.divided = False

    def is_leaf(self):
        return (self.boundary.x2 - self.boundary.x1) <= LEAF_SIZE or (self.boundary.y2 - self.boundary.y1) <= LEAF_SIZE

    def subdivide(self):
        x1 = self.boundary.x1
        y1 = self.boundary.y1
        x2 = self.boundary.x2
        y2 = self.boundary.y2
        depth = self.depth + 1
        north_east = QuadTree(Boundary(x1+(x2-x1)/2, y1, x2, y1+(y2-y1)/2), self.NODE_CAPACITY, depth)
        north_west = QuadTree(Boundary(x1, y1, x1+(x2-x1)/2, y1+(y2-y1)/2), self.NODE_CAPACITY, depth)
        south_east = QuadTree(Boundary(x1+(x2-x1)/2, y1+(y2-y1)/2, x2, y2), self.NODE_CAPACITY, depth)
        south_west = QuadTree(Boundary(x1, y1+(y2-y1)/2, x1+(x2-x1)/2, y2), self.NODE_CAPACITY, depth)

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

        if self.is_leaf() or len(self.points) < self.NODE_CAPACITY:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        for child in self.children:
            if child.insert(point):
                return True

        print "Could not add point [{}, {}]".format(point.x, point.y)
        return False

    def query_range(self, rectangle):
        points_in_range = []
        if not (rectangle.intersects(self.boundary)):
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
            pygame.draw.circle(frame, (255, 0, 0), (int(point.pos.x), int(point.pos.y)), 2, 0)
        pygame.draw.rect(frame, (0, 255, 0), (self.boundary.x1, self.boundary.y1,
                                              self.boundary.x2 - self.boundary.x1,
                                              self.boundary.y2 - self.boundary.y1), 1)
        if self.divided:
            for child in self.children:
                child.show(frame)
