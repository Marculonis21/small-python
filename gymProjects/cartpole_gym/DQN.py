#!/usr/bin/env python3

import gym
import numpy as np
import random

def sigmoid(x):
    return 1/(1+np.exp(-x))

def deriv(x):
    return (x*(1-x))

class NN:
    def __init__(self, layers):
        self.layerW = []
        self.biases = []

        for l in range(len(layers)-1):
            w = 2*np.random.random((layers[l], layers[l+1])) - 1
            b = 2*np.random.random((layers[l+1])) - 1

            self.layerW.append(w)
            self.biases.append(b)

class Agent:
    def __init__(self, net_layers):
        self.policy_net = NN(net_layers)
        self.target_net = self.policy_net

    def out_action(self, inp, full_out = False, net_type="policy"):
        if net_type == "policy":
            net = self.policy_net
        elif net_type == "target":
            net = self.target_net

        layers = []
        layers.append(inp)

        for i in range(len(net.layerW)):
            l = sigmoid(np.dot(layers[i], net.layerW[i]) + net.biases[i])
            layers.append(l)

        end = list(layers[-1])

        if not full_out:
            return end.index(max(end))
        
        else:
            return end

    def get_current_qValues(self, exp_batch):
        #exp = [state, action, reward, next_state]
        pairs = []
        for state,a,_,_ in exp_batch:
            pairs += [self.out_action(state, True)[a]]

        return pairs

    def get_next_qValues(self, exp_batch):
        values = []
        for _,_,_,next_state in exp_batch:
            values += [max(self.out_action(next_state, True, "target"))]

        return values

    def backprop(self, loss):
        net = self.policy_net
        error = loss
        l3_delta = error * deriv(net.layerW[-1])
        l2_error = l3_delta.dot(net.layerW[-2])

        '''
        for i in range(len(net.layerW)):

            if(i != 0):
                error =

            delta = error * deriv(net.layerW[-(i+1)])
        
        '''

            
class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.push_count = 0

    def add(self, exp):
        if(self.capacity > len(self.memory)):
            self.memory.append(exp)
        else:
            self.memory[self.push_count % self.capacity] = exp
            self.push_count += 1

    def sample_min(self, batch_size):
        return (len(self.memory) > batch_size)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

if __name__ == "__main__":
    batch_size = 200
    update_interval = 1000

    agent = Agent([4,5,2])
    reMemory = ReplayMemory(10000)

    env = gym.make('CartPole-v0')

    #print(env.action_space) # 2
    #print(env.observation_space) # 4

    iterations = 0
    while True:
        state = env.reset()
        for time in range(200):
            env.render()
            iterations += 1

            action = agent.out_action(state)
            next_state, reward, done, info = env.step(action)

            #exp = [state, action, reward, next_state]
            experience = [state, action, reward, next_state]
            reMemory.add(experience)

            state = next_state

            if(reMemory.sample_min(batch_size)):
                ### learn policy + maybe change target ###

                exp_batch = reMemory.sample(batch_size)

                rewards = []
                for _,_,reward,_ in exp_batch:
                    rewards.append(reward)

                current_q_values = agent.get_current_qValues(exp_batch)
                next_q_values = agent.get_next_qValues(exp_batch)
                target_q_values = (np.array(next_q_values) * 0.99) + rewards

                loss = np.mean((target_q_values - current_q_values)**2)

                agent.backprop(loss)

                pass

            if done:
                break
