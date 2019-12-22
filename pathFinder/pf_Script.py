#!/usr/bin/env python3

import pyglet as P
from pyglet.gl import *
import math

def drawLine(sX,sY,eX,eY):
    glBegin(GL_LINES)
    glVertex2f(sX,sY)
    glVertex2f(eX,eY)
    glEnd()

def drawSquare(sX,sY,size,color):
    glBegin(GL_QUADS)
    glColor3f(color[0],color[1],color[2])
    glVertex2f(sX,sY)
    glVertex2f(sX+size,sY)
    glVertex2f(sX+size,sY+size)
    glVertex2f(sX,sY+size)
    glEnd()

def showMode(sX,sY,size):
    global MODE,MODELIST
    label = P.text.Label(MODELIST[MODE],
                         font_size=size,
                         x=sX,
                         y=sY,
                         anchor_x='center',
                         anchor_y='center')
    label.draw()


def checkerBoard(size):
    for i in range(int(winWidth/size)):
        drawLine(i*size,0,i*size,win.height)
        drawLine(0,i*size,win.width,i*size)

def drawQUADS(pieceSize):
    global wallList,startPos,endPos
    for quad in wallList:
        drawSquare(quad[0]*pieceSize,quad[1]*pieceSize, pieceSize, [0.1,0.1,0.1])

    if(startPos != []):
        drawSquare(startPos[0]*pieceSize,startPos[1]*pieceSize, pieceSize, [0.1,1,0.1])
    if(endPos != []):
        drawSquare(endPos[0]*pieceSize,endPos[1]*pieceSize, pieceSize, [1,0.1,0.1])


def process():

    
    

winWidth = 600

mousePressed = False
xPress = -1
yPress = -1

MODE = 0 
MODELIST={0:"wall",1:"start",2:"end"}

wallList = []
startPos = []
endPos = []


win = P.window.Window(winWidth,winWidth,caption="PathFinder")
glClearColor(0.4,0.4,0.4, 1)

@win.event
def tick(t):
    pass

@win.event
def on_draw():
    win.clear()
    glColor3f(1,1,1)

    pieceSize = 50

    checkerBoard(pieceSize)
    
    global xPress, yPress, wallList,startPos,endPos, MODE
    if(xPress != -1):
        xPos = math.floor(xPress/pieceSize)
        yPos = math.floor(yPress/pieceSize)
        if(MODE == 0):
            wallList += [[xPos,yPos]]
        if(MODE == 1):
            startPos = [xPos,yPos]
        if(MODE == 2):
            endPos = [xPos,yPos]
        xPress = yPress = -1

    drawQUADS(pieceSize)

    showMode(15,win.height-15,10)

@win.event
def on_mouse_drag(x,y,dx,dy,c,d):
    global xPress, yPress 
    xPress = x
    yPress = y

@win.event
def on_mouse_press(x,y ,c,d):
    global xPress, yPress
    xPress = x
    yPress = y

@win.event
def on_key_press(s,mod):
    global MODE
    if(s == P.window.key.S):
        MODE = 1
    if(s == P.window.key.E):
        MODE = 2
    if(s == P.window.key.W):
        MODE = 0

    if(s == P.window.key.ENTER):
        process()


P.clock.schedule_interval(tick, 1/60)
P.app.run()
