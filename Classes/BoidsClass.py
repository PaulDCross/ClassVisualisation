import numpy as np
import math
import random
import commonLibraries.Vector as v
import commonLibraries.extras as e
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
import Classes.VehicleClass as vc
import pygame

class Boids(vc.Vehicles):
    """docstring for Boids"""
    def __init__(self, display, walls):
        vc.Vehicles.__init__(self, display, walls)

    def update(self, globalTarget):
        for boid in self.vehicles:
            boid.applyWalls(self.walls)
            boid.seek(globalTarget)
            boid.flock(self.vehicles)
            boid.update()
            boid.display(self.gameDisplay)

class Boid(vc.Vehicle):
    def __init__(self, pos):
        vc.Vehicle.__init__(self, pos)
        self.radius = 10
        self.desiredSeparation = self.radius*2
        self.neighbourhoodDist = 4*self.desiredSeparation

    def seek(self, globalTarget):
        self.Centre            = v.add(self.pos, self.vel.mulScalar(self.radius/2))
        self.theta             = random.uniform(self.theta-0.3, self.theta+0.3)
        randomPointOnCircle    = v.Vector([self.radius*math.cos(self.theta), self.radius*math.sin(self.theta)])
        self.randomLocalTarget = v.add(self.Centre, randomPointOnCircle)

        if globalTarget == None:
            desired = v.sub(self.randomLocalTarget, self.pos).unit().mulScalar(self.maxspeed)
        else:
            globalTarget = v.Vector(globalTarget)
            desired = v.sub(v.sub(globalTarget, self.pos).unit().mulScalar(self.maxspeed), v.sub(self.randomLocalTarget, self.pos).unit().mulScalar(self.maxspeed).mulScalar(0.4))

        desired.sub(self.vel)
        if e.upperLimit(desired.mag(), self.maxforce) == self.maxforce:
            desired = desired.unit().mulScalar(self.maxforce)
        self.addForce(desired)

    def flock(self, boids):
        Dictionary = self.rules(boids)
        try:
            separationForce = Dictionary['Separation'].mulScalar(1.0)
            self.addForce(separationForce)
        except KeyError:
            pass
        try:
            cohesionForce   = Dictionary['Cohesion'].mulScalar(1.1)
            self.addForce(cohesionForce)
        except KeyError:
            pass
        try:
            directionForce  = Dictionary['Direction'].mulScalar(1)
            self.addForce(directionForce)
        except KeyError:
            pass

    def rules(self, boids):
        separationCount        = 0
        cohesionCount          = 0
        summedSeparationVector = v.Vector([0, 0])
        summedCohesionVector   = v.Vector([0, 0])
        summedDirectionVector  = v.Vector([0, 0])
        Dictionary             = {}

        for boid in boids:
            d = v.sub(self.pos, boid.pos).mag()
            if 0<d<self.desiredSeparation:
                summedSeparationVector.add(v.sub(self.pos, boid.pos).unit())
                separationCount += 1
            if 0<d<self.neighbourhoodDist:
                summedCohesionVector.add(v.sub(self.pos, boid.pos).unit())
                summedDirectionVector.add(boid.vel)
                cohesionCount += 1

        if separationCount>0:
            separationSteering = v.sub(summedSeparationVector.mulScalar(1.0/separationCount).unit().mulScalar(self.maxspeed), self.vel)
            if e.upperLimit(separationSteering.mag(), self.maxforce) == self.maxforce:
                separationSteering = separationSteering.unit().mulScalar(self.maxforce)
            Dictionary['Separation'] = separationSteering

        if cohesionCount>0:
            cohesionSteering = v.sub(summedCohesionVector.mulScalar(1.0/cohesionCount).unit().mulScalar(-self.maxspeed), self.vel)
            if e.upperLimit(cohesionSteering.mag(), self.maxforce) == self.maxforce:
                cohesionSteering = cohesionSteering.unit().mulScalar(self.maxforce)
            Dictionary['Cohesion'] = cohesionSteering

            directionSteering = v.sub(summedDirectionVector.mulScalar(1.0/cohesionCount).unit().mulScalar(self.maxspeed), self.vel)
            if e.upperLimit(directionSteering.mag(), self.maxforce) == self.maxforce:
                directionSteering = directionSteering.unit().mulScalar(self.maxforce)
            Dictionary['Direction'] = directionSteering

        return Dictionary

    def display(self, frame):
        debugging      = False
        triangle       = e.polygon(self.numSides, self.radius)
        theta          = math.atan2(self.vel.x, self.vel.y)
        rotationMatrix = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        triangle       = [v.add(v.Vector(np.matmul(pair, rotationMatrix)), self.pos).pos for pair in triangle]
        pygame.draw.lines(frame, (0,0,0), True, triangle, 1)
        if debugging:
            pygame.draw.circle(frame, (255,0,0), map(int, self.pos.pos), int(2))
            pygame.draw.circle(frame, (150,150,150), map(int, self.Centre.pos), int(self.radius), 1)
            pygame.draw.circle(frame, (0,0,255), map(int, self.randomLocalTarget.pos), int(2))
            pygame.draw.line(frame, (0,0,255), self.Centre.pos, self.randomLocalTarget.pos, 1)
