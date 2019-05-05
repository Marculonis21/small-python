#!usr/bin/env python3

import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def deriv(x):
    return (x*(1-x))

x = np.array([[1,1],[1,0],[0,1],[0,0]])

y = np.array([[1],[0],[0],[1]])

w1 = 2*np.random.random((2,3)) - 1
w2 = 2*np.random.random((3,1)) - 1
print("w1" + str(w1))
print("w2" + str(w2))

b1 = 2*np.random.random((3)) - 1
b2 = 2*np.random.random((1)) - 1
print("b1" + str(b1))
print("b2" + str(b2))

print()

for i in range(10000):
    l1 = x
    print(l1)
    print(len(l1))
    mid1 = (np.dot(l1,w1)-b1)
    l2 = sigmoid(mid1)
    mid2 = (np.dot(l2,w2)-b2)
    l3 = sigmoid(mid2)
    print(l3)
    quit()

    l3_error = y - l3
    l3_delta = l3_error*deriv(l3)
    l2_error = l3_delta.dot(w2.T)
    l2_delta = l2_error*deriv(l2)

    w2 += l2.T.dot(l3_delta)
    w1 += l1.T.dot(l2_delta)

print("after training: " + str(l3))
