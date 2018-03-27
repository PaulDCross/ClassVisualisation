import commonLibraries.Vector as v
import commonLibraries.extras as e
import random
import pygame

class Point(object):
    """docstring for point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Boundary(object):
    """docstring for rectangle"""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, p):
        return (self.x - self.w <= p.x <= self.x + self.w and
                self.y - self.h <= p.y <= self.y + self.h)

    def intersects(self, rectangle):
        return (((self.x + self.w) > (rectangle.x - rectangle.w)) and ((self.x - self.w) < (rectangle.x + rectangle.w)) and
                ((self.y - self.h) < (rectangle.y + rectangle.h) and (self.y + self.h) > (rectangle.y - rectangle.h)))


class Quad_Tree(object):
    """docstring for Quad_Tree"""
    def __init__(self, boundary, capacity):
        self.NODE_CAPACITY = capacity
        self.boundary = boundary
        self.points = []
        self.divided = False


    def subdivide(self):
        ne = Boundary(self.boundary.x + (self.boundary.w/2),
                      self.boundary.y - (self.boundary.h/2),
                      self.boundary.w/2, self.boundary.h/2)
        nw = Boundary(self.boundary.x - (self.boundary.w/2),
                      self.boundary.y - (self.boundary.h/2),
                      self.boundary.w/2, self.boundary.h/2)
        se = Boundary(self.boundary.x + (self.boundary.w/2),
                      self.boundary.y + (self.boundary.h/2),
                      self.boundary.w/2, self.boundary.h/2)
        sw = Boundary(self.boundary.x - (self.boundary.w/2),
                      self.boundary.y + (self.boundary.h/2),
                      self.boundary.w/2, self.boundary.h/2)

        self.north_east = Quad_Tree(ne, self.NODE_CAPACITY)
        self.north_west = Quad_Tree(nw, self.NODE_CAPACITY)
        self.south_east = Quad_Tree(se, self.NODE_CAPACITY)
        self.south_west = Quad_Tree(sw, self.NODE_CAPACITY)

        self.divided = True


    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.NODE_CAPACITY:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.north_east.insert(point):
                return True
            if self.north_west.insert(point):
                return True
            if self.south_east.insert(point):
                return True
            if self.south_west.insert(point):
                return True

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
            pygame.draw.circle(frame, (255, 0, 0), (point.x, point.y), 2, 0)
        if self.divided:
            self.north_east.show(frame)
            self.north_west.show(frame)
            self.south_east.show(frame)
            self.south_west.show(frame)
