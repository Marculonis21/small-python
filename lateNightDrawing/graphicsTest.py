#!/usr/bin/env python3

import turtle as t
inp = [6.5,8,10,5,3,2.2,1,0.3,2,0.1,1,0]
scale = 20

t.setup(1000,400)
t.hideturtle()
t.up()
t.setx(t.Screen().window_width()/2)
t.down()
t.setx(-t.Screen().window_width()/2)
t.setx(-t.Screen().window_width()/2 + 20)

t.up()
t.left(90)
t.forward(inp[0]*scale)
t.right(90)
t.down()

actual = inp[0]
for i in range(1,len(inp)):
    if(inp[i]>inp[i-1]):
        t.left(80)
        t.forward(abs(inp[i]-actual)*scale)
        actual = inp[i]
        t.right(80)
        t.dot(3)
    else:
        t.right(80)
        t.forward(abs(inp[i]-actual)*scale)
        actual = inp[i]
        t.left(80)
        t.dot(3)
