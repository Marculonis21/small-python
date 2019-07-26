#!/usr/bin/env python3

import curses as C

import pyglet

import random as R
import time
import math

playMap = ["WWWWWWW",
           "W     W",
           "W     W",
           "W  .  W",
           "W     W",
           "W     W",
           "WWWWWWW"]

WALL = "W"
#WALL_h = 50

pieceSize = 50
playerPos = {}
playerDir = 0

#playerInputLag
#num of frames
PIL = 20
#actualInputLag
AIL = -1

#moveSpeed
PMS = 5
#viewDistance
PVD = 150
#fieldOfView
FOV = 80
#rayCastFidelity
RCF = 20



def displaying(_pos,_dir):
    rayOutput = []

    #for every FOV point send out a ray
    #+1 - fine number of rays (symetry)
    for loop in range(FOV+1):
        testDir = _dir - (FOV/2) + loop

        if(testDir < 0):
            testDir = 360 + testDir

        #submodules of ray
        #works as number guessing game (lower/higher)
        #separate ray into many with different lengths 
        #to higher fidelity of view determination
        #PVD part
        _PVDP = PVD/RCF
        collided = False
        for testLength in range(1,RCF+1):
            #test PVD
            _PVD = testLength*_PVDP

            rayX = (int(_PVD*math.sin(math.radians(testDir))))
            rayY = (int(_PVD*math.cos(math.radians(testDir))))
            collision = rayCast(rayX,rayY,_pos)

            if(collision == WALL):
                collided = True
                rayOutput.append([collision, _PVD])
                break

        if not (collided):
            rayOutput.append([' ', PVD])
            

    return rayOutput

'''
def OLDrayCast(_rayX,_rayY,_pos):
    #Test ray XY coordinates

    rayX = _rayX
    rayY = _rayY

    #scan map for all pieces
    for y in range(len(playMap)):
        _y = list(playMap[y])

        for x in range(len(_y)):
            if(_y[x] != ' ' and _y[x] != '.'):
                xPos = x
                yPos = y

                #Test each part of ray against all objects till collision
                #and save first collided ray part
                #(also add playerPos to ray pos to get where the ray really ends! :D)
                for test in range(RCF):
                    if(getCollision(xPos, yPos, _pos['x']+rayX[test], _pos['y']+rayY[test])):
                        if(_y[x] == WALL):
                            return WALL, test*(PVD/RCF)
'''

def rayCast(_rayX,_rayY,_pos):
    #Test ray XY coordinates

    rayX = _rayX
    rayY = _rayY

    #scan map for all pieces
    for y in range(len(playMap)):
        _y = list(playMap[y])

        for x in range(len(_y)):
            if(_y[x] != ' ' and _y[x] != '.'):
                xPos = x
                yPos = y

                #Test each part of ray against all objects till collision
                #and save first collided ray part
                #(also add playerPos to ray pos to get where the ray really ends! :D)
                if(getCollision(xPos, yPos, _pos['x']+rayX, _pos['y']+rayY)):
                    if(_y[x] == WALL):
                        return WALL 

    return ' '

def getCollision(x,y, rayX, rayY):
    lowerBoundX = pieceSize*x - pieceSize/2
    upperBoundX = pieceSize*x + pieceSize/2

    lowerBoundY = pieceSize*y - pieceSize/2
    upperBoundY = pieceSize*y + pieceSize/2
     
    collision = False
    if(rayX >= lowerBoundX and rayX <= upperBoundX):
        if(rayY >= lowerBoundY and rayY <= upperBoundY):
            collision = True

    return collision

def borderDraw(win,winX,winY):
    win.addstr(0,0,"#")
    win.addstr(winY-2,winX-2,"#")
    for x in range(0,winX-2):
        win.addstr(0,x,"#")
        win.addstr(winY-2,x,"#")
    for y in range(0,winY-2):
        win.addstr(y,0,"#")
        win.addstr(y,winX-2,"#")

def viewPrinting(win,winX,winY,view):
    screenWidth = int(winX-1)
    midY = int(winY/2)

    #linePerRay
    LPR = screenWidth / FOV

    lastValue = 0
    lastC = 1
    for rayIndex in range(FOV):
        actualValue = int(LPR*rayIndex)

        for i in range(actualValue-lastValue):
            for z in range(int(view[rayIndex][1] / 10)):
                xxx = lastValue + i

                #strop??
                if(z >= midY):
                    break
                
                if(view[rayIndex][0] == WALL):
                    win.addstr(int(midY) + z, xxx+1, WALL, C.color_pair(lastC))
                    win.addstr(int(midY) - z, xxx+1, WALL, C.color_pair(lastC))
                else:
                    win.addstr(int(midY) + z, xxx+1, ' ', C.color_pair(lastC))
                    win.addstr(int(midY) - z, xxx+1, ' ', C.color_pair(lastC))

        if(lastC == 1):
            lastC = 2
        else:
            lastC = 1

        lastValue = actualValue

def animation():
    global AIL,PIL

    win = C.initscr()

    C.start_color()
    C.use_default_colors()
    
    #color pairs
    C.init_pair(1,C.COLOR_GREEN, -1)
    C.init_pair(2,C.COLOR_RED, -1)

    # hide cursor
    C.noecho()
    C.cbreak()
    C.curs_set(0)

    win.clear()
    win.refresh()
    

    ### DRAWING LOOP
    try:
        while True:
            #clear screen
            win.clear()

            winX = win.getmaxyx()[1]
            winY = win.getmaxyx()[0]

            #displayBorder draw
            borderDraw(win,winX,winY)
            
            #get view output from displaying(raycasting)
            view = displaying(playerPos,playerDir)

            #display all from rayCast (walls and stuff)
            viewPrinting(win,winX,winY,view)

            if(AIL == -1):
                key = ''
                key = win.getch()
                win.addstr(10,R.randint(10,20),str(key))
                if(key != None):
                    AIL = 0

            win.addstr(20,R.randint(10,20), "x")

            
            #window draw delta
            startT = time.time()
            while time.time() - startT >= 1/20:
                break
            
            if(AIL == PIL):
                AIL = -1
            elif(AIL != -1):
                AIL += 1

            win.refresh()
    ### DRAWING LOOP

    except KeyboardInterrupt:
        C.echo()
        C.endwin()
        pass

for y in range(len(playMap)):
    _y = list(playMap[y])

    for x in range(len(_y)):
        if(_y[x] == '.'):
            playerPos['y'] = (pieceSize*y)
            playerPos['x'] = (pieceSize*x)

#displaying(playerPos,playerDir)

animation()
