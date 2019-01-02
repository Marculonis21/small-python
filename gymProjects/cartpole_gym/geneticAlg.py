#!/usr/bin/env python3

import random as R

class genPop:
    def __init__(self, popSize, genSize, mutRate):
        self.popSize = popSize
        self.mutRate = mutRate
        self.genSize = genSize

        self.genCounter = 1
        self.bestFitness = -1

        self.species = [[] for size in range(popSize)]
        self.fitness = [-1 for size in range(popSize)]
        self.parents = []
        self.children = []

    def genCount(self):
        return self.genCounter

    def avgFit(self):
        sFitness = sum(self.fitness)
        nFitness = len(self.fitness)
        return sFitness/nFitness

    def newGen(self):
        self.parents = []
        self.bestFitness = {self.fitness.index(max(self.fitness)) : max(self.fitness)}

        nMax = sum(self.fitness)

        for i in range(self.popSize):
            x = R.randint(0,nMax)

            nTest = 0
            for loop in range(len(self.fitness)):
                nTest += self.fitness[loop]

                if(x <= nTest):
                    self.parents.append(self.species[loop])
                    break

        self.children = []

        for loop in range(int(self.popSize/2)):
            p1 = R.choice(self.parents)
            self.parents.remove(p1)
            p2 = R.choice(self.parents)
            self.parents.remove(p2)

            ch1 = []
            ch2 = []
            for i in range(len(self.species[0])):
                x = R.choice([0,1])

                if(x == 0):
                    ch1.append(p1[i])
                    ch2.append(p2[i])
                elif(x == 1):
                    ch1.append(p2[i])
                    ch2.append(p1[i])

            self.children.append(ch1)
            self.children.append(ch2)

        for ch in self.children:
            for i in range(len(ch)):
                if(R.random() <= (self.mutRate/100)):
                    ch[i] = 2*R.random()-1

        self.species = self.children
        self.genCounter += 1
