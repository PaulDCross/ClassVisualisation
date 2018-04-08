import pygame

LEAF_SIZE = 4
DEPTH_LIMIT = 50

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


class KDTree(object):
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
        return (self.boundary.x2 - self.boundary.x1) <= LEAF_SIZE or (self.boundary.y2 - self.boundary.y1) <= LEAF_SIZE or self.depth == DEPTH_LIMIT

    def subdivide(self):
        x1 = self.boundary.x1
        y1 = self.boundary.y1
        x2 = self.boundary.x2
        y2 = self.boundary.y2
        depth = self.depth + 1
        # Assumes two dimensions (x, y)
        if self.depth % 2:
            # Cut by y
            y = median([p.y for p in self.points])
            left_child = KDTree(Boundary(x1, y1, x2, y), self.NODE_CAPACITY, depth)
            right_child = KDTree(Boundary(x1, y, x2, y2), self.NODE_CAPACITY, depth)
        else:
            # Cut by x
            x = median([p.x for p in self.points])
            left_child = KDTree(Boundary(x1, y1, x, y2), self.NODE_CAPACITY, depth)
            right_child = KDTree(Boundary(x, y1, x2, y2), self.NODE_CAPACITY, depth)

        self.children = [left_child, right_child]

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


def median(numbers):
    n = len(numbers)
    if n < 1:
        return None
    if n % 2:
        return sorted(numbers)[n//2]
    else:
        return sum(sorted(numbers)[(n//2)-1:(n//2)+1])//2



