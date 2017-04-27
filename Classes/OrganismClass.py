import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
import Classes.VehicleClass as vc
import commonLibraries.Vector as v
import commonLibraries.extras as e
import math
import numpy as np
import pygame
import random


class Foodlist():
    def __init__(self, gameDisplay, amount, dd):
        self.foodlist    = [Food([random.randint(0, dd[0]), random.randint(0, dd[1])]) for i in xrange(amount)]
        self.gameDisplay = gameDisplay

    def update(self):
        for food in self.foodlist:
            food.display(self.gameDisplay)

class Food(object):
    """docstring for food"""
    def __init__(self, pos):
        self.pos      = v.Vector(pos)
        self.value    = 100
        self.numSides = 4
        self.radius   = 4

    def display(self, frame):
        triangle = e.polygon(self.numSides, self.radius)
        triangle = [v.add(v.Vector(pair), self.pos).pos for pair in triangle]
        pygame.draw.lines(frame, (0,0,0), True, triangle, 1)


class DNA(object):
    """docstring for DNA"""
    def __init__(self):
        self.genes = [random.randint(1,15) for i in xrange(1)]


class Organisms(vc.Vehicles):
    """docstring for Organisms"""
    def __init__(self, display, walls):
        vc.Vehicles.__init__(self, display, walls)

    def update(self, foodlist):
        for vehicle in self.vehicles:
            vehicle.eat(foodlist)
            vehicle.applyWalls(self.walls)
            vehicle.update()
            vehicle.display(self.gameDisplay)
            if vehicle.dies:
                if vehicle.isDead():
                    self.removeVehicle(vehicle)


class Organism(vc.Vehicle):
    def __init__(self, pos):
        vc.Vehicle.__init__(self, pos)
        self.numSides = 6
        self.dna      = DNA()
        self.radius   = int(self.dna.genes[0])
        self.maxspeed = 15/self.radius
        self.health   = 255
        self.dies     = True

    def update(self):
        self.vel.x = random.gauss(self.vel.x, 0.3)
        self.vel.y = random.gauss(self.vel.y, 0.3)

        self.vel.add(self.acc)
        if e.upperLimit(self.vel.mag(), self.maxspeed) == self.maxspeed:
            self.vel = self.vel.unit().mulScalar(self.maxspeed)
        self.pos.add(self.vel)
        self.acc = self.acc.mulScalar(0)

        if self.dies:
            self.health -= 1
            # This if statement stops the program crashing.
            if self.health < 1:
                self.health = 0

        print self.health

    def eat(self, foodlist):
        for item in foodlist.foodlist:
            d = v.sub(self.pos, item.pos).mag()
            if d<self.radius:
                self.health += item.value
                foodlist.foodlist.remove(item)
