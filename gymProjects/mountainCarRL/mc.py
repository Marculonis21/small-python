#!/usr/bin/env python3

import gym
import matplotlib.pyplot as plt
import numpy as np

LR = 0.05
GAMMA = 0.95
EPSILON = 0.95

EPISODES = 5000

START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2

EPSILON_DECAY = EPSILON/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

env = gym.make('MountainCar-v0')

buckets = [20, 20]
discrete_size = (env.observation_space.high - env.observation_space.low)/buckets

q_table = np.random.uniform(low=-2, high=0,
                            size=(buckets[0], buckets[1], env.action_space.n))

def observation2state(obs, env):
    nDiscreteState = (obs - env.observation_space.low)/discrete_size
    return tuple(nDiscreteState.astype(np.int))

rewardList = []
avgRewardList = []

for currEpisode in range(EPISODES):
    # if(currEpisode % 100 == 0):
    #     print(currEpisode)

    if(currEpisode%1000 == 0 or currEpisode == EPISODES-1):
        print(currEpisode)
        render = True
    else:
        render = False

    totalReward = 0

    # X,Y do Q-table
    discreteState = observation2state(env.reset(), env)

    done = False
    while not done:

        # epsilon greedy
        if(np.random.random() < EPSILON): # if smaller then EPS choose on random (=explore)
            action = np.random.randint(0, env.action_space.n)
        else: # otherwise choose by qtable
            action = np.argmax(q_table[discreteState])

        observation, reward, done, _ = env.step(action)
        if(render):
            env.render()

        newDiscreteState = observation2state(observation, env)

        if not done:
            # update q values

            # max possible Q value in future step
            maxQ = np.max(q_table[newDiscreteState])

            # current q value (already performed action)
            currQ = q_table[discreteState + (action,)]

            # newQ calculation
            newQ = (1-LR) * currQ + LR*(reward + GAMMA * maxQ)

            # quality value update
            q_table[discreteState + (action,)] = newQ

        # obs[0] = sim position
        elif(observation[0] >= env.goal_position):
            q_table[discreteState + (action,)] = 0

        # next state
        discreteState = newDiscreteState

        totalReward += reward

    rewardList.append(totalReward)

    if((currEpisode + 1) % (EPISODES//100) == 0):
        avgReward = np.mean(rewardList)
        avgRewardList.append(avgReward)
        rewardList = []

    # EPSILON decay
    if END_EPSILON_DECAYING >= currEpisode >= START_EPSILON_DECAYING:
            EPSILON -= EPSILON_DECAY


env.close()

plt.plot(np.arange(len(avgRewardList))+1,avgRewardList)
plt.xlabel('Episodes')
plt.ylabel('Average Reward')
plt.title('Reward vs Episodes')
plt.show()
