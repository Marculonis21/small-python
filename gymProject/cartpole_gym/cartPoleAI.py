#!/usr/bin/env python3

import gym

env = gym.make('CartPole-v0')

observation = env.reset()

for i in range(1000):

    env.render()
    print(observation)
    action = env.action_space.sample()

    observation, reward, done, info = env.step(action)

