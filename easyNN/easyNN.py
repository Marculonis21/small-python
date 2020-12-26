#!usr/bin/env python3

import numpy as np
import time

def sigmoid(x):
    return 1/(1+np.exp(-x))

def relu(x):
    return np.maximum(0,x)

def linear(x):
    return x

def deriv(x):
    return x*(1-x)

x_ = np.array([[1,1],[1,0],[0,1],[0,0]])

y_ = np.array([[1],[0],[0],[1]])

w1 = 2*np.random.random((2,3)) - 1
w2 = 2*np.random.random((3,1)) - 1

b1 = 2*np.random.random((3)) - 1
b2 = 2*np.random.random((1)) - 1

print()

for i in range(10000):
    l1 = x_
    l2 = sigmoid(np.dot(l1,w1))
    l3 = sigmoid(np.dot(l2,w2))

    I_error = y_ - l3
    I_delta = I_error * deriv(l3)
    II_error = np.dot(I_delta, w2.T)
    II_delta = II_error * deriv(l2)

    learn_rate = 0.5
    print(I_delta.shape)
    print(l2.T.shape)
    quit()
    w2 += (np.dot(l2.T, I_delta) * learn_rate)
    w1 += (np.dot(l1.T, II_delta) * learn_rate)


l1 = x_
l2 = sigmoid((np.dot(l1,w1)))
l3 = sigmoid((np.dot(l2,w2)))
print("after training: \n" + str(l3))
