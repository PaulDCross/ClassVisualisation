import numpy as np
import random
import cv2
import sys
import pygame

class ParticalSystem(object):
    """docstring for ParticalSystem"""
    def __init__(self, frame, origin):
        self.frame     = frame
        self.origin    = origin
        # self.Particles = [Particle(self.origin) if random.random() < 0.5 else Particle(self.origin) for i in range(50)]
        self.Particles = []
        self.gravity   = np.array([0, 0.05])
        # self.addForce(self.gravity)

    def addParticle(self):
        self.Particles.append(Particle(self.origin))

    def addForce(self, force):
        for particle in self.Particles:
            particle.addForce(force)

    def run(self):
        for particle in self.Particles:
            if particle.isDead():
                del self.Particles[self.Particles.index(particle)]
            particle.update()
            particle.display(self.frame)
            particle.acc = self.gravity
        self.numberofparticles = len(self.Particles)

class Particle(object):
    """docstring for Particle"""
    def __init__(self, pos):
        random.seed()
        # The partical's location
        self.pos  = np.array(pos)
        # The partical's velocity
        self.vel  = np.array([np.random.normal(0, 0.3), -abs(np.random.normal(0, 1))])
        # The partical's acceleration
        self.acc  = np.array([0, 0.05])
        # The lifespan of the partical
        self.life = random.randint(200, 300)

    def update(self):
        self.vel = self.vel.__add__(self.acc)
        self.pos = self.pos.__add__(self.vel)
        self.life -= 2
        # This if statement stops the program crashing.
        if self.life < 1:
            self.life = 0

    def addForce(self, force):
        self.acc = self.acc.__add__(np.array(force))

    def isDead(self):
        if self.life <= 0:
            return True
        else:
            return False

    def display(self, frame):
        print e.colourise(self.life, 0, 1)
        pygame.draw.rect(frame, (255-self.life, 255-self.life, 255-self.life), [self.pos[0], self.pos[1], 5, 5])




class CircleSystem_cv2(ParticalSystem):
    def addParticle(self):
        self.Particles.append(Circle_cv2(self.origin))

class Square_cv2(Particle):
    def display(self, frame):
        cv2.rectangle(frame, tuple(map(int, self.pos-5)), tuple(map(int, self.pos+5)), (255-self.life, 255-self.life, 255-self.life), -1)

class Circle_cv2(Particle):
    def display(self, frame):
        cv2.circle(frame, tuple(map(int, self.pos)), 5, (255-self.life, 255-self.life, 255-self.life), -1)








if __name__ == '__main__':
    frame   = np.zeros((500, 500, 3), 'uint8')
    systems = [CircleSystem_cv2(frame, np.array([random.randint(50, frame.shape[1]-50), random.randint(50, frame.shape[0]-50)])) for i in range(1)]

    for i in range(1000):
        frame.fill(255)
        for system in systems:
            system.addParticle()
            system.run()
        cv2.imshow("frame", frame)
        if cv2.waitKey(2) & 0xFF == 27:
            cv2.destroyAllWindows()
            sys.exit()
