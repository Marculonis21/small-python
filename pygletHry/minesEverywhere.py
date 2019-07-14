#!/usr/bin/env python3
import pyglet
from pyglet.gl import *
import random as R

window = pyglet.window.Window(500,500, "MINES", resizable = False)

pieceSize = 50
numX = int(window.width/pieceSize) + 1
numY = int(window.height/pieceSize) + 1

playField = [[0 for x in range(numX)] for y in range(numY)]
mineCount = 30


def startField():
    global playField

    for i in range(mineCount):
        while True:
            _x = R.randint(0,numX)
            _y = R.randint(0,numY)

            if(playField[_x][_y] == 0):
                break

        playField[_x][_y] = -1


def drawLine(startX, startY, endX, endY, r=1,g=1,b=1):
    glBegin(GL_LINES)
    glColor3f(r,g,b)
    glVertex2f(int(startX), int(startY))
    glVertex2f(int(endX), int(endY))
    glEnd()

def drawRect(x,y,sizeX,sizeY, r=1,g=1,b=1):
    glBegin(GL_QUADS)
    glColor3f(r,g,b)
    glVertex2f(int(x), int(y))
    glVertex2f(int(x+sizeX), int(y))
    glVertex2f(int(x+sizeX), int(y+sizeY))
    glVertex2f(int(x), int(y+sizeY))
    glEnd()

def drawNum(posX,posY,num):
    posX += setSize/2
    posY += setSize/2
    label = pyglet.text.Label(str(num),
                              font_size=pieceSize,
                              anchor_x='center',
                              anchor_y='center')

    label.x = posX
    label.y = posY

    label.draw()

def drawSpot(posX,posY,free):
    posX += setSize/2
    posY += setSize/2

    if(free):
        label = pyglet.text.Label("",
                                  font_size=pieceSize,
                                  anchor_x='center',
                                  anchor_y='center')
    else:
        label = pyglet.text.Label("#",
                                  font_size=pieceSize,
                                  anchor_x='center',
                                  anchor_y='center')

    label.x = posX
    label.y = posY

    label.draw()

def gridDraw():
    for x in range(numX):
        drawLine(x*pieceSize,0,x*pieceSize,window.height)

    for y in range(numY):
        drawLine(0,y*pieceSize,window.width,y*pieceSize)

def tickFunc(t):
    pass

@window.event
def on_draw():
    glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    gridDraw()

    pass


pyglet.clock.schedule_interval(tickFunc,1/60)
pyglet.app.run()
