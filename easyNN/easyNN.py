#!/usr/bin/env python3
# https://www.youtube.com/watch?v=262XJe2I2D0&ab_channel=HackingEDU

import numpy as np
import time

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sig_deriv(x):
    return sigmoid(x)*(1-sigmoid(x))

def MSE(output, result):
    return np.square(result - output).mean()

X = np.array([[1,1],
              [1,0],
              [0,1],
              [0,0]])

Y = np.array([[0],
              [1],
              [1],
              [0]])

w1 = 2*np.random.random((2,3)) - 1
w2 = 2*np.random.random((3,1)) - 1

b1 = 2*np.random.random((3)) - 1
b2 = 2*np.random.random((1)) - 1

for i in range(10000):
    l1 = X
    l2 = sigmoid(np.dot(l1,w1)) + b1
    l3 = sigmoid(np.dot(l2,w2)) + b2

    error_output = MSE(l3, Y)
    delta_output = error_output * sig_deriv(l3)

    learn_rate = 0.1
    #output
    w2 += learn_rate*(l2.T.dot(delta_output))
    b2 += learn_rate*(np.mean(delta_output))

    #hidden
    delta_h1 = w2.T*delta_output
    print(delta_h1)

    # w1 += 
    # b1 +=

    quit()


    # II_error = III_delta.dot(w2)
    # II_delta = II_error * sig_deriv(l2)

    # I_error = II_delta.dot(w1)
    # I_delta = I_error * sig_deriv(l1)

    w2 += l2.T.dot(II_delta) * learn_rate
    w1 += l1.T.dot(I_delta) * learn_rate

l1 = x_
l2 = sigmoid((np.dot(l1,w1)))
l3 = sigmoid((np.dot(l2,w2)))
print("after training: \n" + str(l3))
