#!/usr/bin/env python3

import curses as C
import random as R
import time
import math

playMap = ["#######",
           "#     #",
           "#     #",
           "#  .  #",
           "#     #",
           "#     #",
           "#######"]

WALL = "#"
#WALL_h = 50

pieceSize = 50
playerPos = {}
playerDir = 0

#moveSpeed
PMS = 5
#viewDistance
PVD = 200
#fieldOfView
FOV = 80
#rayCastFidelity
RCF = 100 


def displaying(_pos,_dir):

    rayOutput = []

    #for every FOV point send out a ray
    for loop in range(FOV):
        testDir = _dir - (FOV/2) + loop

        if(testDir < 0):
            testDir = 360 + testDir

        rayX = []
        rayY = []
        
        #submodules of ray
        #works as number guessing game (lower/higher)
        #separate ray into many with different lengths 
        #to higher fidelity of view determination
        for testLength in range(1,RCF+1):
            _PVDP = PVD/RCF
            _PVD = testLength*_PVDP

            rayX.append(int(_PVD*math.sin(math.radians(testDir))))
            rayY.append(int(_PVD*math.cos(math.radians(testDir))))

        #print(rayX,rayY)

        collision, distance = rayCast(rayX,rayY,_pos)
        #print(collision,distance)
        rayOutput.append([collision,distance])

    return rayOutput


def rayCast(_rayX,_rayY,_pos):
    #Test ray XY coordinates
    '''
    x = int(PVD*math.sin(math.radians(_dir)))
    y = int(PVD*math.cos(math.radians(_dir)))
    print(x,y)
    '''

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


def getCollision(x,y, rayX, rayY):
    lowerBoundX = pieceSize*x 
    upperBoundX = pieceSize*x + pieceSize

    lowerBoundY = pieceSize*y
    upperBoundY = pieceSize*y + pieceSize

     
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

def animation():
    win = C.initscr()

    C.start_color()
    C.use_default_colors()

    # hide cursor
    C.noecho()
    C.curs_set(0)

    '''
    #testArea
    winX = win.getmaxyx()[1]
    winY = win.getmaxyx()[0]
    maxX = winX - 3
    maxY = winY - 3
    C.endwin()

    LPR = (maxX - 1) / FOV
    print(maxX - 1)
    lastValue = 0
    for rayIndex in range(FOV):

        actualValue = int(LPR*rayIndex)
        #print("rayIndex {}".format(rayIndex))
        #print(lastValue)
        #print(int(LPR*rayIndex))

        for i in range(actualValue-lastValue):
            #print("ray {}".format(rayIndex))

        lastValue = actualValue

    quit()
    #testArea
    '''

    win.clear()
    win.refresh()
    try:
        while True:
            #clear screen
            win.clear()

            winX = win.getmaxyx()[1]
            winY = win.getmaxyx()[0]
            maxX = winX - 3
            maxY = winY - 3

            #get view output from displaying(reycasting)
            view = displaying(playerPos,playerDir)

            #clear screen
            win.clear()

            #displayBorder draw
            borderDraw(win,winX,winY)
            
            #linePerRay
            LPR = (maxX - 1) / FOV
            lastValue = 0
            for rayIndex in range(FOV):
                actualValue = int(LPR*rayIndex)

                for i in range(actualValue-lastValue):
                    #print("ray {}".format(rayIndex))
                    for z in range(int(view[rayIndex][1] / 10)):
                        xxx = lastValue + i
                        if(z >= maxY/2):
                            break

                        win.addstr(int(maxY/2) + z, xxx, '#')
                        win.addstr(int(maxY/2) - z, xxx, '#')


                lastValue = actualValue

            #timeDelta frame draw time
            sTime = time.time()
            while(time.time() - sTime < 1/10):
                pass


            win.refresh()
    except KeyboardInterrupt:
        pass
    C.endwin()

playerPos["x"] = -1
for i in playMap:
    if('.' in i):
        playerPos["y"] = (pieceSize*playMap.index(i)) + pieceSize/2
        xxx = list(i)
        playerPos["x"] = (pieceSize*xxx.index('.')) + pieceSize/2

#displaying(playerPos,playerDir)

animation()
