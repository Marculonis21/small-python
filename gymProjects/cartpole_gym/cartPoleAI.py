#!/usr/bin/env python3

import gym
import numpy as np
from tqdm import tqdm
import geneticAlg as ga

def nonlin(x, deriv=False):
    if(deriv):
        return(x*(1-x))

    return 1/(1+np.exp(-x))

def controller(player, obs):
    p = population.species[player]

    w = []
    for y in range(4):
        w.append([])
        for x in range(5):
            w[y].append(p[x+(4*y)])

    w1 = np.array(w)

    w = []
    for i in range(5):
        w.append(p[20+i])

    w2 = np.array(w)

    l1 = obs
    l2 = nonlin(np.dot(l1,w1))
    l3 = nonlin(np.dot(l2,w2))
    end = round(l3)

    return int(end)

env = gym.make('CartPole-v0')

population = ga.genPop(50, 25, 3)

for item in population.species:
    w1 = 2*np.random.random([4,5]) - 1
    w2 = 2*np.random.random([5,1]) - 1

    _w1 = list(w1)
    for y in range(len(w1)):
        for x in range(len(w1[0])):
            item.append(_w1[y][x])

    _w2 = list(w2)
    for y in range(len(w2)):
        for x in range(len(w2[0])):
            item.append(_w2[y][x])

while True:
    for genIter in range(population.popSize):
        print("GenNumber: {} ;Specie {}".format(population.genCount(), genIter))

        observation = env.reset()

        rew = 0

        for i in tqdm(range(200)):
            env.render()
            action = controller(genIter,observation)
            # print("action \n{}".format(action))
            observation, reward, done, info = env.step(action)

            rew += reward

            if(done):
                print(rew)
                population.fitness[genIter] = rew
                print("\nEnd after {} timestaps".format(i))
                break


    if(sum(population.fitness)/len(population.fitness)>150):
        print("THE POPULATION HAS BEEN LEARNED")
        print("Done in {} gens".format(population.genCounter))
        break

    population.newGen()
    print("Average Fit: {}".format(population.avgFit()))
    print("\n#\n#\n#\nLast gen best fitness: {}\nAverage fitness: {}\n#\n#\n#\n".format(population.bestFitness, population.avgFit()))
    quit()
