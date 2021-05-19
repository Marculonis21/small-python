#!/usr/bin/env python3

import numpy as np
import random 

def sigmoid(x, deriv=False):
    if(deriv):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def MSE(layer_output, desired_output):
    return np.mean(np.square(np.subtract(desired_output,layer_output)))

def forwardPropagation(layer1, layer2, weights, bias):
    for TO in range(weights.shape[1]):
        for FROM in range(weights.shape[0]):
            layer2[TO] += layer1[FROM]*weights[FROM][TO]
        layer2[TO] += bias[TO]
        layer2[TO] = sigmoid(layer2[TO])

    return layer2

def errorBackPropagation(previousDelta, layer, weights):
    layerError = weights.T * previousDelta
    newDelta = layerError * sigmoid(layer, deriv=True)

    return newDelta

def weightUpdate(layer,weights,bias,delta,learnRate):
    delta = np.atleast_1d(delta.squeeze())
    for FROM in range(weights.shape[0]):
        for TO in range(weights.shape[1]):
            weights[FROM][TO] -= (delta[TO]*layer[FROM]) * learnRate

            bias[TO] -= delta[TO] * learnRate

    return weights, bias


X = [[1,1],[1,0],[0,1],[0,0]]
Y = [0,1,1,0]
learnRate = 0.1

random.seed(12345)

l1 = np.array(X[0])                    # input
l2 = np.array([0.0 for x in range(4)]) # hidden1
l3 = np.array([0.0 for x in range(1)]) # output

w1 = np.array([[2*random.random() - 1 for TO in range(4)] for FROM in range(2)])
b1 = np.array([2*random.random() - 1 for TO in range(4)])

w2 = np.array([[2*random.random() - 1 for TO in range(1)] for FROM in range(4)])
b2 = np.array([2*random.random() - 1 for TO in range(1)])

for iterations in range(10000):
    if(iterations % 2000 == 0):
        print()
    for learning_loop in range(4):
        INPUT = X[learning_loop]
        OUTPUT = Y[learning_loop]

        # zero out layers
        l1 = np.array(INPUT)                   # input
        l2 = np.array([0.0 for x in range(4)]) # hidden1
        l3 = np.array([0.0 for x in range(1)]) # output

        l2 = forwardPropagation(l1,l2,w1,b1)
        l3 = forwardPropagation(l2,l3,w2,b2)

        outputError = OUTPUT - l3
        if(iterations % 2000 == 0):
            print(MSE(l3,OUTPUT))
        deltaOutput = (-1) * outputError * sigmoid(l3, deriv=True)

        deltaL2 = errorBackPropagation(deltaOutput, l2, w2)

        w2,b2 = weightUpdate(l2, w2, b2, deltaOutput, learnRate)
        w1,b1 = weightUpdate(l1, w1, b1, deltaL2, learnRate)


for learning_loop in range(4):
    INPUT = X[learning_loop]
    OUTPUT = Y[learning_loop]

    # zero out layers
    l1 = np.array(INPUT)                   # input
    l2 = np.array([0.0 for x in range(4)]) # hidden1
    l3 = np.array([0.0 for x in range(1)]) # output

    l2 = forwardPropagation(l1,l2,w1,b1)
    l3 = forwardPropagation(l2,l3,w2,b2)

    print(l3)
