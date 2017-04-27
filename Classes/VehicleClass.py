
import commonLibraries.Vector as v
import commonLibraries.extras as e
import math
import numpy as np
import pygame
import random

class Vehicles(object):
    """docstring for Vehicles"""
    def __init__(self, display, walls):
        self.vehicles    = []
        self.gameDisplay = display
        self.walls       = walls
        self.numVehicles = 0

    def addVehicle(self, cls, pos):
        self.vehicles.append(cls(pos))
        self.numVehicles += 1

    def removeVehicle(self, vehicle):
        # Where vehicle is the class object
        self.vehicles.remove(vehicle)
        self.numVehicles -= 1

    def update(self):
        for vehicle in self.vehicles:
            vehicle.applyWalls(self.walls)
            vehicle.update()
            vehicle.display(self.gameDisplay)
            if vehicle.dies:
                if vehicle.isDead():
                    self.removeVehicle(vehicle)


class Vehicle(object):
    """docstring for Vehicle"""
    def __init__(self, pos):
        random.seed()
        self.acc      = v.Vector([0,0])
        self.vel      = v.Vector([np.random.normal(0, 1),np.random.normal(0, 1)])
        self.pos      = v.Vector(pos)
        self.theta    = random.uniform(-math.pi, math.pi)
        self.numSides = 3
        self.radius   = 10
        self.maxspeed = 2
        self.maxforce = 0.15
        self.dies     = False
        self.health   = 255

    def update(self):
        ''' Method to update location
        '''
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

    def isDead(self):
        if self.health <= 0:
            return True
        else:
            return False

    def addForce(self, force):
        # Mass could be added A = F/M
        self.acc.add(force)

    def applyWalls(self, walls):
        desired = None
        if self.pos.x < walls[0]:
            desired = v.Vector([self.maxspeed, self.vel.y])
        if self.pos.x > walls[1]:
            desired = v.Vector([-self.maxspeed, self.vel.y])
        if self.pos.y < walls[2]:
            desired = v.Vector([self.vel.x, self.maxspeed])
        if self.pos.y > walls[3]:
            desired = v.Vector([self.vel.x, -self.maxspeed])
        if desired != None:
            desired.sub(self.vel)
            if e.upperLimit(desired.mag(), self.maxforce) == self.maxforce:
                desired = desired.unit().mulScalar(self.maxforce)
            self.acc = desired

    def seek(self, target):
        desired = v.sub(v.Vector(target), self.pos)
        desired = desired.unit().mulScalar(self.maxspeed)
        desired.sub(self.vel)
        if e.upperLimit(desired.mag(), self.maxforce) == self.maxforce:
            desired = desired.unit().mulScalar(self.maxforce)
        self.addForce(desired)

    def avoid(self, target):
        desired = v.sub(v.Vector(target), self.pos)
        desired = desired.unit().mulScalar(self.maxspeed)
        desired.sub(self.vel)
        if e.upperLimit(desired.mag(), self.maxforce) == self.maxforce:
            desired = desired.unit().mulScalar(self.maxforce)
        self.addForce(desired.mulScalar(-1))

    def display(self, frame):
        debugging      = True
        triangle       = e.polygon(self.numSides, self.radius)
        theta          = math.atan2(self.vel.x, self.vel.y)
        rotationMatrix = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        triangle       = [v.add(v.Vector(np.matmul(pair, rotationMatrix)), self.pos).pos for pair in triangle]
        # pygame.draw.lines(frame, (0,0,0), True, triangle, 1)
        pygame.draw.polygon(frame, (e.limit(255-self.health, 0, 255), e.limit(255-self.health, 0, 255), e.limit(255-self.health, 0, 255)), triangle, 0)
        if debugging:
        #     pygame.draw.circle(frame, (255,0,0), map(int, self.pos.pos), int(2))
        #     pygame.draw.circle(frame, (150,150,150), map(int, self.Centre.pos), int(self.radius), 1)
        #     pygame.draw.circle(frame, (0,0,255), map(int, self.randomLocalTarget.pos), int(2))
            pygame.draw.line(frame, (0,0,255), self.pos.pos, v.add(self.pos, self.vel.mulScalar(10)).pos, 1)
