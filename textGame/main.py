#!/usr/bin/env python3

import curses as C
import random as R
import time
import math

playMap = ["#####",
           "#   #",
           "# . #",
           "#   #",
           "#####"]

WALL = "#"
WALL_h = 50

pieceSize = 50
playerPos = {}
playerDir = 0

#moveSpeed
PMS = 5
#viewDistance
PVD = 200
#fieldOfView
FOV = 1
#rayCastFidelity
RCF = 5


def displaying(_pos,_dir):

    #for every FOV point send out a ray
    for loop in range(FOV):
        testDir = _dir - (FOV/2) + loop
        testDir = 0
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

        print(rayX,rayY)

        collision, distance = rayCast(rayX,rayY,_pos)
        print(collision,distance)

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


def animation():
    win = C.initscr()

    C.start_color()
    C.use_default_colors()

    # hide cursor
    C.noecho()
    C.curs_set(0)

    win.clear()
    win.refresh()
    try:
        while True:
            winX = win.getmaxyx()[1]
            winY = win.getmaxyx()[0]
            win.clear()

            sTime = time.time()
            win.addstr(0,0,"#")
            win.addstr(winY-2,winX-2,"#")
            for x in range(0,winX-2):
                win.addstr(0,x,"#")
                win.addstr(winY-2,x,"#")
            for y in range(0,winY-2):
                win.addstr(y,0,"#")
                win.addstr(y,winX-2,"#")

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
#quit()

animation()
