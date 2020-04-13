#!/usr/bin/env python3

import gym
import numpy as np
import random
import matplotlib.pyplot as plt 
import copy

def sigmoid(x):
    return 1/(1+np.exp(-x))

def derivative(x):
    return (x*(1-x))

#def sigmoid_derivative(x):
#    return sigmoid(x) * (1 - sigmoid(x))


class NN:
    def __init__(self, layers):
        self.layerW = []
        self.biases = []

        for l in range(len(layers)-1):
            w = 2*np.random.random((layers[l], layers[l+1])) - 1
            #b = 2*np.random.random((layers[l+1])) - 1

            self.layerW.append(w)
            #self.biases.append(b)

class Agent:
    def __init__(self, net_layers):
        self.policy_net = NN(net_layers)
        self.target_net = copy.copy(self.policy_net)

    def copy_net(self):
        self.target_net = copy.copy(self.policy_net)

    def out_action(self, inp, full_out = False, net_type="policy"):
        if net_type == "policy":
            net = self.policy_net
        elif net_type == "target":
            net = self.target_net

        self.layers = []
        self.layers.append(inp)

        for i in range(len(net.layerW)):
            l = sigmoid(np.dot(self.layers[i], net.layerW[i]))
            self.layers.append(l)

        end = list(self.layers[-1])

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

    def backprop(self, loss, learning_rate, experience, batch_size):
        net = copy.copy(self.policy_net)

        w2_change = []
        w1_change = []

        for state,a,_,_ in experience:
            out = self.out_action(state, True)

            I_error = loss
            I_delta = I_error * derivative(self.layers[-1])
            II_error = np.dot(I_delta, net.layerW[-1].T)
            II_delta = II_error * derivative(self.layers[-2])

            w2_change.append(np.array(learning_rate * np.array([I_delta]).T * self.layers[-2]).T)
            w1_change.append(np.array(learning_rate * np.array([II_delta]).T * self.layers[-3]).T)


        self.policy_net.layerW[-1] += np.mean(w2_change, axis=0)
        self.policy_net.layerW[-2] += np.mean(w1_change, axis=0)


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

def plot(values, moving_avg_period):
    plt.figure(2)
    plt.clf()
    plt.title('Training..')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(values)

    #moving_avg = get_moving_average(moving_avg_period, values)
    #plt.plot(moving_avg)
    plt.pause(0.001)
    #print("Episode", len(values), "\n", \
            #    moving_avg_period, "episode moving avg:", moving_avg[-1])
    #if is_ipython: display.clear_output(wait=True)

if __name__ == "__main__":
    max_steps = 500
    batch_size = 50 
    target_update = 10 
    learning_rate = 0.001
    gamma = 0.999
    #epsilon + decay

    np.random.seed(0)

    agent = Agent([4,5,2])
    reMemory = ReplayMemory(100000)

    env = gym.make('CartPole-v0')
    env._max_episode_steps = max_steps

    #print(env.action_space) # 2
    #print(env.observation_space) # 4

    episode_durations = []
    episodes = 0 
    while True:
        episodes += 1

        if(episodes % target_update == 0):
            print("Episode count: " + str(episodes))
            #START NEW + copy net
            agent.copy_net()

        state = env.reset()
        for time in range(1000):
            #if(episodes % 100 == 0):
            env.render()

            action = agent.out_action(state)
            next_state, reward, done, info = env.step(action)
        
            if(done):
                if(time == max_steps-1):
                    print("solved")
                    reward = 10
                else:
                    reward = -50

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
                target_q_values = (np.array(next_q_values) * gamma) + rewards

                #LOSS = MSE => print((1/200)*sum((target_q_values - current_q_values)**2))
                loss = np.mean((current_q_values - target_q_values)**2)
                
                agent.backprop(loss, learning_rate, exp_batch, batch_size)

            if done:
                episode_durations.append(time)
                #if(episodes % 100 == 0):
                plot(episode_durations, 100)
                break

