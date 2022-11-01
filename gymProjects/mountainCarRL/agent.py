#!/usr/bin/env python

import gym
import matplotlib.pyplot as plt
import numpy as np

class Agent:
    def __init__(self, env, agentSettings, bucketsNum, EPISODES):
        self.env = env
        self.LR = agentSettings[0]
        self.GAMMA = agentSettings[1]
        self.EPSILON = agentSettings[2]
        self.EPSILON_END_DECAYING = agentSettings[3]

        self.EPISODES = EPISODES

        START_EPSILON_DECAYING = 1
        self.EPSILON_DECAY = self.EPSILON/(self.EPSILON_END_DECAYING - 1)

        self.discrete_size = (env.observation_space.high - env.observation_space.low)/bucketsNum
        self.q_table = np.random.uniform(low=-2, high=-1,
                                         size=(bucketsNum[0], bucketsNum[1], env.action_space.n))

    def observation2state(self, obs, env):
        nDiscreteState = (obs - env.observation_space.low)/self.discrete_size
        return tuple(nDiscreteState.astype(np.int))

