#!/usr/bin/env python3
#https://www.kaggle.com/vitorgamalemos/multilayer-perceptron-from-scratch

import numpy as np
import random 
import matplotlib.pyplot as plt

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
l2 = np.array([0.0 for x in range(4)]) # hidden1
l3 = np.array([0.0 for x in range(1)]) # output

w1 = np.array([[2*random.random() - 1 for TO in range(4)] for FROM in range(2)])
b1 = np.array([2*random.random() - 1 for TO in range(4)])

w2 = np.array([[2*random.random() - 1 for TO in range(1)] for FROM in range(4)])
b2 = np.array([2*random.random() - 1 for TO in range(1)])

all_outs = []
for iterations in range(10000):
    outs = []
    for learning_loop in range(4):
        INPUT = X[learning_loop]
        OUTPUT = Y[learning_loop]

        # zero out layers
        l1 = np.array(INPUT)                   # input
        l2 = np.array([0.0 for x in range(4)]) # hidden1
        l3 = np.array([0.0 for x in range(1)]) # output

        for TO in range(4):
            for FROM in range(2):
                l2[TO] += l1[FROM]*w1[FROM][TO]
            l2[TO] += b1[TO]
            l2[TO] = sigmoid(l2[TO])

        for TO in range(1):
            for FROM in range(4):
                l3[TO] += l2[FROM]*w2[FROM][TO]
            l3[TO] += b2[TO]
            l3[TO] = sigmoid(l3[TO])

        outs.append(l3[0])
        learn_rate = 0.1

        error_output = OUTPUT - l3
        delta_output = (-1)*error_output * sigmoid(l3, deriv=True)

        error_l2 = w2.T * delta_output
        delta_l2 = error_l2 * sigmoid(l2, deriv=True)

        # output to l2
        for FROM in range(4):
            for TO in range(1):
                w2[FROM][TO] -= (delta_output[TO]*l2[FROM]) * learn_rate

                b2[TO] -= delta_output[TO] * learn_rate

        # l2 to l1
        for FROM in range(2):
            for TO in range(4):
                w1[FROM][TO] -= (delta_l2[0][TO]*l1[FROM]) * learn_rate

                b1[TO] -= delta_l2[0][TO] * learn_rate

    all_outs.append(outs)

plt.figure()
plt.plot(range(10000), [MSE(all_outs[x],Y) for x in range(10000)],
         "m-",color="b", marker=',')
plt.xlabel("Iterace")
plt.ylabel("Error (MSE) ");
plt.title("Error decrease")
plt.show()

for learning_loop in range(4):
    INPUT = X[learning_loop]
    OUTPUT = Y[learning_loop]

    # zero out layers
    l1 = np.array(INPUT)                   # input
    l2 = np.array([0.0 for x in range(4)]) # hidden1
    l3 = np.array([0.0 for x in range(1)]) # output

    for TO in range(4):
        for FROM in range(2):
            l2[TO] += l1[FROM]*w1[FROM][TO]
        l2[TO] += b1[TO]
        l2[TO] = sigmoid(l2[TO])

    for TO in range(1):
        for FROM in range(4):
            l3[TO] += l2[FROM]*w2[FROM][TO]
        l3[TO] += b2[TO]
        l3[TO] = sigmoid(l3[TO])

    print(l3)
