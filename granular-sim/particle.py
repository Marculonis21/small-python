#!/usr/bin/env python3

class Particle:
    def __init__(self, x, y, pType):
        self.x = x
        self.y = y
        self.pType = pType

        self.mass = 0
        self.temp = 0

        self.static = False
