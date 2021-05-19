#!/usr/bin/env python3
#https://www.kaggle.com/vitorgamalemos/multilayer-perceptron-from-scratch

import numpy as np
import random 

def sigmoid(x, deriv=False):
    if(deriv):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def MSE(layer_output, desired_output):
    return np.mean(np.square(np.subtract(desired_output,layer_output)))

# X = np.array([[1,1],[1,0],[0,1],[0,0]])
# Y = np.array([[1],[0],[0],[1]])

random.seed(12345)

X = [[1,1],[1,0],[0,1],[0,0]]
Y = [0,1,1,0]

l1 = np.array(X[0])                    # input
l2 = np.array([0.0 for x in range(8)]) # hidden1
l3 = np.array([0.0 for x in range(8)]) # hidden 2
l4 = np.array([0.0 for x in range(1)]) # output

w1 = np.array([[2*random.random() - 1 for TO in range(8)] for FROM in range(2)])
b1 = np.array([2*random.random() - 1 for TO in range(8)])

w2 = np.array([[2*random.random() - 1 for TO in range(8)] for FROM in range(8)])
b2 = np.array([2*random.random() - 1 for TO in range(8)])

w3 = np.array([[2*random.random() - 1 for TO in range(1)] for FROM in range(8)])
b3 = np.array([2*random.random() - 1 for TO in range(1)])

for iterations in range(10000):
    for learning_loop in range(4):
        INPUT = X[learning_loop]
        OUTPUT = Y[learning_loop]

        # zero out layers
        l1 = np.array(INPUT)                   # input
        l2 = np.array([0.0 for x in range(8)]) # hidden1
        l3 = np.array([0.0 for x in range(8)]) # hidden 2
        l4 = np.array([0.0 for x in range(1)]) # output

        for TO in range(8):
            for FROM in range(2):
                l2[TO] += l1[FROM]*w1[FROM][TO]
            l2[TO] += b1[TO]
            l2[TO] = sigmoid(l2[TO])

        for TO in range(8):
            for FROM in range(8):
                l3[TO] += l2[FROM]*w2[FROM][TO]
            l3[TO] += b2[TO]
            l3[TO] = sigmoid(l3[TO])

        for TO in range(1):
            for FROM in range(8):
                l4[TO] += l3[FROM]*w3[FROM][TO]
            l4[TO] += b3[TO]
            l4[TO] = sigmoid(l4[TO])

        learn_rate = 0.1

        error_output = OUTPUT - l4
        # if(iterations % 5000 == 0):
        #     print(MSE(l4, OUTPUT))

        delta_output = (-1)*error_output * sigmoid(l4, deriv=True)

        error_l3 = w3 * delta_output
        delta_l3 = error_l3 * sigmoid(l3, deriv=True)

        error_l2 = w2 * delta_l3
        delta_l2 = error_l2 * sigmoid(l2, deriv=True)

        # output to l3
        for FROM in range(8):
            for TO in range(1):
                w3[FROM][TO] -= (delta_output[TO]*l3[FROM]) * learn_rate

                b3[TO] -= delta_output[TO] * learn_rate

        # l3 to l2
        for FROM in range(8):
            for TO in range(8):
                w2[FROM][TO] -= (delta_l3[0][TO]*l2[FROM]) * learn_rate

                b2[TO] -= delta_l3[0][TO] * learn_rate

        # l2 to l1
        for FROM in range(2):
            for TO in range(8):
                w1[FROM][TO] -= (delta_l2[0][TO]*l1[FROM]) * learn_rate

                b1[TO] -= delta_l2[0][TO] * learn_rate


for learning_loop in range(4):
    INPUT = X[learning_loop]
    OUTPUT = Y[learning_loop]

    # zero out layers
    l1 = np.array(INPUT)                   # input
    l2 = np.array([0.0 for x in range(8)]) # hidden1
    l3 = np.array([0.0 for x in range(8)]) # hidden 2
    l4 = np.array([0.0 for x in range(1)]) # output

    for TO in range(8):
        for FROM in range(2):
            l2[TO] += l1[FROM]*w1[FROM][TO]
        l2[TO] += b1[TO]
        l2[TO] = sigmoid(l2[TO])

    for TO in range(8):
        for FROM in range(8):
            l3[TO] += l2[FROM]*w2[FROM][TO]
        l3[TO] += b2[TO]
        l3[TO] = sigmoid(l3[TO])

    for TO in range(1):
        for FROM in range(8):
            l4[TO] += l3[FROM]*w3[FROM][TO]
        l4[TO] += b3[TO]
        l4[TO] = sigmoid(l4[TO])

    print(l4)
