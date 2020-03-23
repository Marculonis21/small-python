#!/usr/bin/env python3

import pyglet as P
from pyglet.gl import *
import math
import time

winWidth = 800
pieceSize = 20
drawSpeed = 0.01

mousePressed = False
xPress = -1
yPress = -1

#MODES
MODE = 0 
MODELIST={0:"wall",1:"start",2:"end",4:"show",5:"process"}

#BOARDLIST
wallList = []
startPos = []
endPos = []
PATH = []

#PATHFINDING LIST
openL = []
closeL = []
lastPos = []

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

def showStats(sX,sY,pieceSize, openL,closeL):
    fontsize = 10
    for o in openL:
        if(sX == o[0] and sY == o[1]):
            try:
                label1 = P.text.Label(str(o[2]),
                                    font_size=fontsize,
                                    x=o[0]*pieceSize+5,
                                    y=o[1]*pieceSize+5,
                                    anchor_x='center',
                                    anchor_y='center')

                label2 = P.text.Label(str(o[3]),
                                    font_size=fontsize,
                                    x=o[0]*pieceSize+pieceSize-5,
                                    y=o[1]*pieceSize+5,
                                    anchor_x='center',
                                    anchor_y='center')

                label3 = P.text.Label(str(o[4]),
                                    font_size=fontsize,
                                    x=o[0]*pieceSize+5,
                                    y=o[1]*pieceSize+pieceSize-5,
                                    anchor_x='center',
                                    anchor_y='center')
                label1.draw()
                label2.draw()
                label3.draw()
            except:
                pass


    for c in closeL:
        if(sX == c[0] and sY == c[1]):
            try:
                label1 = P.text.Label(str(c[2]),
                                    font_size=fontsize,
                                    x=c[0]*pieceSize+5,
                                    y=c[1]*pieceSize+5,
                                    anchor_x='center',
                                    anchor_y='center')

                label2 = P.text.Label(str(c[3]),
                                    font_size=fontsize,
                                    x=c[0]*pieceSize+pieceSize-5,
                                    y=c[1]*pieceSize+5,
                                    anchor_x='center',
                                    anchor_y='center')

                label3 = P.text.Label(str(c[4]),
                                    font_size=fontsize,
                                    x=c[0]*pieceSize+5,
                                    y=c[1]*pieceSize+pieceSize-5,
                                    anchor_x='center',
                                    anchor_y='center')
                label1.draw()
                label2.draw()
                label3.draw()
            except:
                pass

def checkerBoard(size):
    for i in range(int(winWidth/size)):
        drawLine(i*size,0,i*size,win.height)
        drawLine(0,i*size,win.width,i*size)

def drawQUADS(size):
    global wallList,startPos,endPos
    
    for quad in wallList:
        drawSquare(quad[0]*size,quad[1]*size,size, [0.1,0.1,0.1])

    if(startPos != []):
        drawSquare(startPos[0]*size,startPos[1]*size,size, [0.1,1,0.1])
    if(endPos != []):
        drawSquare(endPos[0]*size,endPos[1]*size,size, [0.1,0.1,1])

def drawPATH(size,PATH):
    for p in PATH:
        drawSquare(p[0]*size,p[1]*size,size, [0.6,0.6,0.8])

def drawProgress(size, openL, closeL, last):
    for o in openL:
        drawSquare(o[0]*size,o[1]*size,size, [0.6,1,0.6])
        
    for c in closeL:
        try:
            drawSquare(c[0]*size,c[1]*size,size, [1,0.6,0.6])
        except:
            pass


    drawSquare(last[0]*size,last[1]*size,size, [0.3,0.6,0.9])

"""
def getAroundPoints(act, start, end, wallL, closeL, maxW):
    #x,y,hcost,fcost
    aroundPoint = [[-1+act[0],-1+act[1],999,999,999],
                   [   act[0],-1+act[1],999,999,999],
                   [ 1+act[0],-1+act[1],999,999,999],
                   [-1+act[0],   act[1],999,999,999],
                   [ 1+act[0],   act[1],999,999,999],
                   [-1+act[0], 1+act[1],999,999,999],
                   [   act[0], 1+act[1],999,999,999],
                   [ 1+act[0], 1+act[1],999,999,999]]

    #loop in points
    for point in aroundPoint:
        #boundaries
        if(point[0]>=0 and point[1]>=0):
            if(point[0]<maxW and point[1]<maxW):
                #test all if not colliding with walls/closedL
                found = False
                for w in wallL:
                    if(point[0] == w[0] and point[1] == w[1]):
                        found = True
                        break
                for c in closeL:
                    if(point[0] == c[0] and point[1] == c[1]):
                        found = True
                        break
                
                #if not wall -> process
                if not(found):
                    EdistanceX = abs(point[0]-end[0])
                    EdistanceY = abs(point[1]-end[1])
                    point[3] = math.sqrt(EdistanceX**2+EdistanceY**2)
                    
                    SdistanceX = abs(point[0]-start[0])
                    SdistanceY = abs(point[1]-start[1])
                    point[2] = math.sqrt(SdistanceX**2+SdistanceY**2)

                    point[4] = point[2] + point[3]

    return aroundPoint
"""
def getAroundPoints(act,end,wallL,maxW):
    aroundPoint = [[-1+act[0],-1+act[1],0,0,0,[]],
                   [   act[0],-1+act[1],0,0,0,[]],
                   [ 1+act[0],-1+act[1],0,0,0,[]],
                   [-1+act[0],   act[1],0,0,0,[]],
                   [ 1+act[0],   act[1],0,0,0,[]],
                   [-1+act[0], 1+act[1],0,0,0,[]],
                   [   act[0], 1+act[1],0,0,0,[]],
                   [ 1+act[0], 1+act[1],0,0,0,[]]]

    walkable = []
    for point in aroundPoint:
        #boundaries
        if(point[0]>=0 and point[1]>=0 and point[0]<maxW and point[1]<maxW):
            #test all if not colliding with walls/closedL
            found = False
            for w in wallL:
                if(point[0] == w[0] and point[1] == w[1]):
                    found = True
                    break
            for c in closeL:
                if(point[0] == c[0] and point[1] == c[1]):
                    found = True
                    break

            if not(found):
                #HCOST - point to end
                point[3] = abs(point[0]-end[0]) + abs(point[1]-end[1])
                walkable.append(point)

    return walkable

def pathFinding(parent):
    global winWidth, pieceSize, wallList, startPos, endPos, openL, closeL
    width = int(winWidth/pieceSize)

    if(closeL == []):
        parent.append(0)
        #add actual startpoint to the closeL
        closeL.append([parent[0],parent[1]])

    #get around point and find best in the open list 
    #(with new points as well)
    #arPoints = getAroundPoints(XY_act, startPos, endPos, wallList, closeL, width)

    arPoints = getAroundPoints(parent,endPos,wallList,width)

    best = findBest(arPoints,parent)

    #if best == end: done
    if(best[0] == endPos[0] and best[1] == endPos[1]):
        print("done")
        global PATH
        wantedX = best[0]
        wantedY = best[1]

        FOUND = False
        while not FOUND:
            for c in closeL:
                if(wantedX == c[0] and wantedY == c[1]):
                    PATH.append([c[0],c[1]])
                    try:
                        wantedX = c[3]
                        wantedY = c[4]
                    except:
                        FOUND = True
                        print(PATH)

        return 0

    return best

def pointInList(point, _list):
    found = False
    for item in _list:
        if(point[0] == item[0] and point[1] == item[1]):
            found = True
            break
    return found

def findBest(points,parent):
    global openL, closeL

    #go through all walkable points
    for p in points:
        #if they are in closeL - ignore 
        if not(pointInList(p, closeL)):

            if(p[0] != parent[0] and p[1] != parent[1]):
                G = parent[2]+1.25
            else:
                G = parent[2]+1

            if(pointInList(p, openL)): #if it's already in the list try using actual G to get lower F -> new parent
                for o in openL:
                    if(p[0] == o[0] and p[1] == o[1]):

                        testF = G + p[3]
                        if(testF < o[4]):
                            o[5] = parent
                            o[2] = G

            else: #if not in open list add G from last parent, compute F and add parent
                p[2] = G

                F = p[2]+p[3]
                p[4] = F
                p[5] = parent

                openL.append(p)

        else:
            continue


    ##remove duplicates from list
    #openL = [list(t) for t in set(tuple(x) for x in openL)]

    #find best point in o
    fBest = sorted(openL, key=lambda x: x[4])
    openL.remove(fBest[0])
    closeL.append([fBest[0][0],fBest[0][1],fBest[0][2], fBest[0][5][0], fBest[0][5][1]])

    return fBest[0]

win = P.window.Window(winWidth,winWidth,caption="PathFinder")
glClearColor(0.4,0.4,0.4, 1)

@win.event
def tick(t):
    pass

@win.event
def on_draw():
    global drawSpeed, pieceSize, xPress, yPress, wallList,startPos,endPos, MODE, openL, closeL, lastPos, mousePressed

    win.clear()
    glColor3f(1,1,1)

    checkerBoard(pieceSize)
    
    if(MODE != 4):
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

        showMode(15,win.height-15,10)

    if(MODE == 5):
        #actPos nothing
        actPos = 0

        #if start -> act = start | else act = lastpost
        if(lastPos == []):
            actPos = startPos
        else:
            actPos = lastPos

        best = pathFinding(actPos)

        if(best == 0): #END
            MODE = 4
        else: #CONTINUE
            lastPos = best

        drawProgress(pieceSize, openL,closeL,lastPos)
        time.sleep(drawSpeed)

    if(MODE == 4):
        drawProgress(pieceSize, openL,closeL,lastPos)
        if(mousePressed):
            xPos = math.floor(xPress/pieceSize)
            yPos = math.floor(yPress/pieceSize)
            showStats(xPos,yPos,pieceSize, openL,closeL)
            xPress = yPress = -1

        global PATH
        drawPATH(pieceSize,PATH)

    drawQUADS(pieceSize)

@win.event
def on_mouse_drag(x,y,dx,dy,c,d):
    global xPress, yPress 
    xPress = x
    yPress = y

@win.event
def on_mouse_press(x,y ,c,d):
    global xPress, yPress
    if(c == 4):
        global mousePressed
        mousePressed = True
        xPress = x
        yPress = y

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
        MODE = 5

<<<<<<< HEAD
P.clock.schedule_interval(tick, 1/60)
=======

P.clock.schedule_interval(tick, 1/120)
>>>>>>> 25e98168699025546c7c98e1f7ea50d89c411bb2
P.app.run()
