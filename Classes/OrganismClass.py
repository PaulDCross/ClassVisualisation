import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../..")
import VehicleClass as vc
import commonLibraries.Vector as v
import commonLibraries.extras as e
import numpy as np
import pygame
import random


class Food(object):
    """docstring for food"""
    def __init__(self, pos, value):
        self.pos = v.Vector(pos)
        self.value = value
        self.radius = 3
        if np.sign(self.value) > 0:
            self.colour = (0, 255, 0)
        elif np.sign(self.value) < 0:
            self.colour = (255, 0, 0)
        else:
            self.colour = (0, 0, 255)

    def display(self, frame):
        pygame.draw.circle(frame, self.colour, (int(self.pos.x), int(self.pos.y)), self.radius, 0)


class DNA(object):
    """docstring for DNA"""
    def __init__(self, genes=None):
        if genes is not None:
            self.genes = genes
        else:
            self.genes = [random.random(),          # Radius
                          random.uniform(-1, 1),    # Food weight
                          random.uniform(-1, 1),    # Poison weight
                          random.random(),          # Food perception
                          random.random(),          # Poison perception
                          random.random(),          # Max speed
                          random.random()           # Max force
                          ]

    def mutate(self, chance=0.1):
        new_genes = []
        for i, gene in enumerate(self.genes):
            if random.random() < chance:
                if i < 1:
                    new_gene = gene + random.uniform(-0.5, 0.5)
                    if new_gene < 0:
                        new_gene = 0
                    elif new_gene > 1:
                        new_gene = 1
                elif i < 3:
                    # Weights
                    new_gene = gene + random.uniform(-0.5, 0.5)
                elif i < 5:
                    # Perception
                    new_gene = gene + random.uniform(-0.5, 0.5)
                    if new_gene < 0:
                        new_gene = 0
                    elif new_gene > 1:
                        new_gene = 1
                else:
                    # Max speed and force
                    new_gene = gene + random.uniform(-0.5, 0.5)
                    if new_gene < 0:
                        new_gene = 0
                    elif new_gene > 1:
                        new_gene = 1
            else:
                new_gene = gene
            new_genes.append(new_gene)
        # print [gene-new_gene for gene, new_gene in zip(self.genes, new_genes)]
        return DNA(new_genes)


class Organisms(vc.Vehicles):
    """docstring for Organisms"""
    def __init__(self, display, walls):
        vc.Vehicles.__init__(self, display, walls)
        self.record = 0

    def reset(self):
        self.vehicles = []
        self.numVehicles = 0
        self.record = 0

    def update(self, foodlist, poisonlist):
        new_vehicles = []
        for vehicle in self.vehicles:
            vehicle.behaviours(foodlist, poisonlist)
            vehicle.applyWalls(self.walls)
            vehicle.update()

            if vehicle.age > self.record:
                self.record = vehicle.age
                vehicle.colour = (255, 255, 255)
                vehicle.inspect()

            vehicle.display(self.gameDisplay, self.debugging)

            # Reproduce
            new_organism = vehicle.reproduce()
            if new_organism is not None:
                new_vehicles.append(new_organism)

            if vehicle.dies:
                if vehicle.isDead():
                    self.removeVehicle(vehicle)
                    foodlist.append(Food(vehicle.pos.pos, 0.2))
        for vehicle in new_vehicles:
            self.addVehicle(vehicle)


class Organism(vc.Vehicle):
    def __init__(self, pos, dna=None):
        vc.Vehicle.__init__(self, pos)
        self.numSides = 3
        if dna is None:
            self.dna = DNA()
        else:
            self.dna = dna
        self.radius = int(e.mapValue(self.dna.genes[0], 0, 1, 1, 10))
        self.goodWeight = self.dna.genes[1]
        self.badWeight = self.dna.genes[2]
        self.foodPerception = int(e.mapValue(self.dna.genes[3], 0, 1, 0, 100))
        self.poisonPerception = int(e.mapValue(self.dna.genes[4], 0, 1, 0, 100))
        self.max_speed = e.mapValue(self.dna.genes[5], 0, 1, 0, 20)
        self.max_force = e.mapValue(self.dna.genes[6], 0, 1, 0.3, 2)
        # self.max_speed = e.mapValue(self.dna.genes[0], 0, 1, 20, 3)
        # self.max_force = e.mapValue(self.dna.genes[0], 0, 1, 0.5, 2)
        self.age = 0
        self.health = 1.0
        self.dies = True
        self.colour = e.lerpColour((255, 0, 0), (0, 255, 0), e.upperLimit(self.health, 1.0))

    def inspect(self):
        print "-------------------"
        print "\tHealth:\t{}".format(self.health)
        print "\tAge:\t{}".format(self.age)
        print "\n\tDNA: {}".format(self.dna.genes)
        print "\t\tSize:\t\t\t\t{}".format(self.radius)
        print "\t\tGood weight:\t\t{}".format(self.goodWeight)
        print "\t\tBad weight:\t\t\t{}".format(self.badWeight)
        print "\t\tFood perception:\t{}".format(self.foodPerception)
        print "\t\tPoison perception:\t{}".format(self.poisonPerception)
        print "\t\tMaximum speed:\t\t{}".format(self.max_speed)
        print "\t\tMaximum force:\t\t{}".format(self.max_force)

    def update(self):
        self.vel.x = random.gauss(self.vel.x, 0.1)
        self.vel.y = random.gauss(self.vel.y, 0.1)

        self.vel.add(self.acc)
        if e.upperLimit(self.vel.mag(), self.max_speed) == self.max_speed:
            self.vel = self.vel.unit().mulScalar(self.max_speed)
        self.pos.add(self.vel)
        self.acc = self.acc.mulScalar(0)

        if self.dies:
            self.age += 0.001
            self.health -= 0.005
            # This if statement stops the program crashing.
            self.health = e.limit(self.health, 0.0, 1.0)
            if self.health < 0.001:
                self.health = 0
        self.colour = e.lerpColour((255, 0, 0), (0, 255, 0), e.upperLimit(self.health, 1.0))

    def reproduce(self, chance=0.0025):
        if random.random() < chance:
            self.dna.mutate()
            return Organism(self.pos.pos, self.dna)
        else:
            return None

    def behaviours(self, good, bad):
        steer_g = self.eat(good, self.foodPerception)
        steer_b = self.eat(bad, self.poisonPerception)
        steer_g = steer_g.mulScalar(self.goodWeight)
        steer_b = steer_b.mulScalar(self.badWeight)
        self.addForce(steer_g)
        self.addForce(steer_b)

    def eat(self, flist, perception):
        record = float("inf")
        closest = None
        for item in flist:
            d = v.sub(self.pos, item.pos).mag()

            if d < self.radius:
                flist.remove(item)
                self.health += item.value
            elif d<record and d<perception:
                # Update the record
                record = d
                closest = item
        if closest is not None:
            return self.seek(closest.pos.pos)
        return v.Vector([0,0])

    def seek(self, target):
        desired = v.sub(v.Vector(target), self.pos)
        desired = desired.unit().mulScalar(self.max_speed)
        desired.sub(self.vel)
        if e.upperLimit(desired.mag(), self.max_force) == self.max_force:
            desired = desired.unit().mulScalar(self.max_force)
        return desired
