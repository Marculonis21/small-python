#!/usr/bin/env python3

import gym
import numpy as np
import random
from matplotlib import pyplot as plt 
import copy
import time


def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return x*(1 - x)

def tanh(x):
    return np.tanh(x)

def tanh_derivative(x):
    return (1-np.square(x))

def relu(x):
    return np.maximum(0, x)

def relu_derivative(x):
    x[x<=0] = 0
    x[x>0] = 1
    return x


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
        self.layout = net_layers

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
            if(i+1 == len(net.layerW)):
                l = tanh(np.dot(self.layers[i], net.layerW[i]))
            else:
                l = tanh(np.dot(self.layers[i], net.layerW[i]))
            self.layers.append(l)

        end = list(self.layers[-1])


        if not full_out:
            return end.index(max(end))
        
        else:
            return end

    def get_current_qValues(self, state, action):
        #exp = [state, action, reward, next_state]
        pairs = []
        for i in range(len(state)):
            pairs += [self.out_action(state[i], True)[action[i]]]

        return pairs

    def get_next_qValues(self, next_state):
        values = []
        for i in range(len(next_state)):
            values += [max(self.out_action(next_state[i], True, "target"))]

        return values

    def backprop(self, loss, learning_rate, experience, batch_size):
        net = copy.copy(self.policy_net)

        net_len = len(self.layout)
        w_change =  [[] for x in range(net_len)]

        w3_change = []
        w2_change = []
        w1_change = []

        errors = []
        errors.append(loss)
        deltas = []

        for state,a,_,_,_ in experience:
            out = self.out_action(state, True)

            I_error = loss
            I_delta = I_error * tanh_derivative(self.layers[-1])
            II_error = np.dot(I_delta, net.layerW[-1].T)
            II_delta = II_error * tanh_derivative(self.layers[-2])
            III_error = np.dot(II_delta, net.layerW[-2].T)
            III_delta = III_error * tanh_derivative(self.layers[-3])

            #for I in range(1, net_len):
            #    deltas.append(errors[I-1] * derivative(self.layers[-I]))
            #    errors.append(np.dot(deltas[I-1], net.layerW[-I].T))

            #print(np.transpose([self.layers.flat[-2]]))

            
            #print(np.atleast_2d(self.layers[-2]).T.shape)
            #print(np.atleast_2d(self.layers[-2]).T)
            #print(self.layers[-2][None, :].T)
            #print(type(self.layers[-2][None, :]))
            #print(I_delta)
            #print(np.atleast_2d(I_delta).shape)
            #print(np.atleast_2d(I_delta))

            w3_change.append(np.dot(self.layers[-2][None, :].T, I_delta[None, :]))
            w2_change.append(np.dot(self.layers[-3][None, :].T, II_delta[None, :]))
            w1_change.append(np.dot(self.layers[-4][None, :].T, III_delta[None, :]))

            #for i in range(1, net_len):
            #    w_change[i].append(np.dot(self.layers[-net_len+i-1].T, deltas[-i]))

        #for i in range(1, net_len):
        #    self.policy_net.layerW[-net_len+i] += np.mean(w_change[i] * learn_rate, axis=0)
            
        self.policy_net.layerW[-1] += np.mean(w3_change, axis=0) * learning_rate
        self.policy_net.layerW[-2] += np.mean(w2_change, axis=0) * learning_rate
        self.policy_net.layerW[-3] += np.mean(w1_change, axis=0) * learning_rate

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

    def sample_min(self, buffer_size):
        return (len(self.memory) > buffer_size)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def unzip(self, batch):
        _state = []
        _action = []
        _reward = []
        _state_next = []
        _terminal = []

        for state, action, reward, state_next, terminal in batch:
            _state.append(state)
            _action.append(action)
            _reward.append(reward)
            _state_next.append(state_next)
            _terminal.append(terminal)

        return _state,_action,_reward,_state_next,_terminal

def plot(values, moving_avg_period, epsilon):
    plt.figure(1)
    plt.clf()
    plt.title('Training..')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(values, label='time-steps')

    x = []
    moving_avg = []
    moving_avg_index = []
    loop = 0
    for i in range(len(values)):
        x += [values[i]]
        if(i % moving_avg_period == 0):
            moving_avg += [np.mean(x)]
            moving_avg_index += [loop*moving_avg_period]
            loop += 1
            x = []

    if(moving_avg != []):
        plt.plot(moving_avg_index, moving_avg, label='average')
    
    plt.legend(loc='upper left', fontsize=9)

    plt.tight_layout()

    plt.pause(0.01)

def sub_plot(values, moving_avg_period, epsilon):
    plt.clf()
    plt.title('Training..')

    plt.subplot(2, 1, 1)
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(values, label='time-steps')

    x = []
    moving_avg = []
    moving_avg_index = []
    loop = 0
    for i in range(len(values)):
        x += [values[i]]
        if(i % moving_avg_period == 0):
            moving_avg += [np.mean(x)]
            moving_avg_index += [loop*moving_avg_period]
            loop += 1
            x = []

    if(moving_avg != []):
        plt.plot(moving_avg_index, moving_avg, label='average')
    plt.legend(loc='upper left', fontsize=9)
    plt.tight_layout()
    
    plt.subplot(2, 1, 2)
    plt.xlabel('Episode')
    plt.ylabel('Epsilon-decay')
    plt.plot(epsilon, label='epsilon')

    plt.legend(loc='upper left', fontsize=9)
    plt.tight_layout()

    plt.pause(0.0001)

if __name__ == "__main__":
    plt.style.use('ggplot')

    HYPER_PARAM_TEST = True
    HYPER_PARAM_TEST_VALUES = [{'agent':[4,32,32,2],
                                'memory_size':100000,
                                'max_steps':250,
                                'batch_size':200,
                                'buffer_size':500,
                                'target_update':50,
                                'learning_rate':0.001,
                                'gamma':0.95,
                                'epsilon':1.0,
                                'epsilon_decay':0.999,
                                'epsilon_end':0.02},
                                {'agent':[4,64,32,2],
                                'memory_size':100000,
                                'max_steps':250,
                                'batch_size':200,
                                'buffer_size':500,
                                'target_update':100,
                                'learning_rate':0.001,
                                'gamma':0.95,
                                'epsilon':1.0,
                                'epsilon_decay':0.999,
                                'epsilon_end':0.02},
                                {'agent':[4,64,64,2],
                                'memory_size':100000,
                                'max_steps':250,
                                'batch_size':200,
                                'buffer_size':500,
                                'target_update':150,
                                'learning_rate':0.001,
                                'gamma':0.95,
                                'epsilon':1.0,
                                'epsilon_decay':0.999,
                                'epsilon_end':0.02}]

    episode_count = 1000
    memory_size = 100000

    max_steps = 250
    batch_size = 128
    buffer_size = 500 
    target_update = 100
    learning_rate = 0.001
    gamma = 0.95
    epsilon = 1.0
    epsilon_decay = 0.999
    epsilon_end = 0.02

    env = gym.make('CartPole-v0')
    env._max_episode_steps = max_steps

    agent = Agent([4,32,16,2])
    reMemory = ReplayMemory(memory_size)

    training_cycle = -1
    while True:
        if(HYPER_PARAM_TEST):
            training_cycle += 1
            if(training_cycle == len(HYPER_PARAM_TEST_VALUES)):
                print("----- END OF TRAINING CYCLE ----- ")
                break

            print("\n\n\nTraining Cycle: {}".format(training_cycle))
            test = HYPER_PARAM_TEST_VALUES[training_cycle]

            agent = Agent(test['agent'])
            reMemory = ReplayMemory(test['memory_size'])
            max_steps = test['max_steps']
            batch_size = test['batch_size']
            buffer_size = test['buffer_size']
            target_update = test['target_update']
            learning_rate = test['learning_rate']
            gamma = test['gamma']
            epsilon = test['epsilon']
            epsilon_decay = test['epsilon_decay']
            epsilon_end = test['epsilon_end']
            print("Max Episodes: {}\nAgent: {}".format(episode_count, test['agent']))
    
        print("\nHyper-Parameters:\nMax sim steps: {}\nBatch size: {}\nBuffersize: {}\nTarget update: {}\nLearning rate: {}\nGamma value: {}\nEpsilon: {}\nEpsilon decay: {}\nEpsilon end: {}\n#####################".format(max_steps,batch_size,buffer_size,target_update,learning_rate,gamma,epsilon,epsilon_decay,epsilon_end))

        env = gym.make('CartPole-v0')
        env._max_episode_steps = max_steps

        episode_durations = []
        epsilon_mem = []

        for episodes in range(episode_count):
            loss_counter = 0

            if(episodes % target_update == 0):
                #print("Episode count: " + str(episodes))
                agent.copy_net()

            state = env.reset()
            for time in range(1000):
                env.render()

                # EXPLORE / EXPLOIT
                if(random.random() <= epsilon):
                    action = env.action_space.sample()
                else: 
                    action = agent.out_action(state)

                if(epsilon > epsilon_end):
                    epsilon *= epsilon_decay

                next_state, reward, terminal, info = env.step(action)
            
                reward = reward if not terminal else -reward

                #exp = [state, action, reward, next_state, terminal]
                experience = [state, action, reward, next_state, terminal]
                reMemory.add(experience)
                state = next_state

                if(terminal):
                    episode_durations.append(time)
                    epsilon_mem.append(epsilon)
                    #plot(episode_durations, 10)
                    sub_plot(episode_durations, target_update, epsilon_mem)

                    break

                if(reMemory.sample_min(buffer_size)):
                    batch = reMemory.sample(batch_size)
                    m_state, m_action, m_reward, m_next_state, m_terminal = reMemory.unzip(batch)
                    
                    current_q_values = agent.get_current_qValues(m_state,m_action)
                    next_q_values = agent.get_next_qValues(m_next_state)
                    target_q_values = (np.array(next_q_values) * gamma) + m_reward

                    for i, done in enumerate(m_terminal):
                        if(done):
                            target_q_values.flat[i] = m_reward[i]

                    #LOSS = MSE
                    loss = np.mean((target_q_values - current_q_values)**2)
                    
                    agent.backprop(loss, learning_rate, batch, batch_size)

        #sub_plot(episode_durations, target_update, epsilon_mem)
        plt.savefig("train_data/graphs/Graph_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_{}_end.png".format(agent.layout,
