import cv2
import numpy as np
import sys
import random

class Canvas():
    """docstring for Canvas"""
    def __init__(self):
        numberOfCells = 1000
        depth         = 800
        canvas        = np.zeros((depth, numberOfCells)); canvas.fill(255)
        self.canvas   = canvas
        self.ca       = CA(self.canvas, numberOfCells)
        self.update()

    def update(self):
        self.ca.display()
        if self.ca.generation < self.canvas.shape[0]/self.ca.w:
            self.ca.generate()
            self.update()
        cv2.imshow("CA", self.ca.frame)
        if cv2.waitKey(0) & 0xFF == 27:
            cv2.destroyAllWindows()
            sys.exit()

class CA():
    """docstring for CA"""
    def __init__(self, frame, numberOfCells):
        self.frame = frame
        self.ruleset                      = [random.randint(0,1) for i in range(8)]
        # self.ruleset                      = [0, 1, 1, 1, 0, 1, 1, 0]
        print self.ruleset
        self.w                            = self.frame.shape[1]/numberOfCells
        # print self.w
        self.cells                        = np.zeros(numberOfCells)
        self.cells[self.cells.shape[0]/2] = 1
        self.generation                   = 0

    def generate(self):
        nextGen = np.zeros(self.cells.shape[0])
        for i in range(len(nextGen)):
            if i == 0:
                left       = self.cells[len(nextGen)-1]
                me         = self.cells[i]
                right      = self.cells[i+1]
            elif i == len(nextGen)-1:
                left       = self.cells[i-1]
                me         = self.cells[i]
                right      = self.cells[0]
            else:
                left       = self.cells[i-1]
                me         = self.cells[i]
                right      = self.cells[i+1]
            nextGen[i] = self.rules(left, me, right)
        self.cells = nextGen
        self.generation += 1


    def display(self):
        for i in range(len(self.cells)):
            if self.cells[i] == 1:
                # print i
                self.frame[(self.generation*self.w):((self.generation*self.w) + self.w), i*self.w:((i*self.w) + self.w)].fill(0)
            else:
                self.frame[(self.generation*self.w):((self.generation*self.w) + self.w), i*self.w:(i*self.w) + self.w].fill(255)
        cv2.imshow("CA", self.frame)
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            sys.exit()

    def rules(self, a, b, c):
        if (a == 0 and b == 0 and c == 0):
                                            return self.ruleset[0]
        if (a == 0 and b == 0 and c == 1):
                                            return self.ruleset[1]
        if (a == 0 and b == 1 and c == 0):
                                            return self.ruleset[2]
        if (a == 0 and b == 1 and c == 1):
                                            return self.ruleset[3]
        if (a == 1 and b == 0 and c == 0):
                                            return self.ruleset[4]
        if (a == 1 and b == 0 and c == 1):
                                            return self.ruleset[5]
        if (a == 1 and b == 1 and c == 0):
                                            return self.ruleset[6]
        if (a == 1 and b == 1 and c == 1):
                                            return self.ruleset[7]
        return 0

Canvas()
