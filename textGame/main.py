#!/usr/bin/env python3

import curses as C 
import math
import pyglet
import queue as Q
import random as R
import threading
import time

playMap = ["WWWWWWW",
           "W     W",
           "W     W",
           "W  .  W",
           "W     W",
           "W     W",
           "WWWWWWW"]

WALL = "W"
#WALL_h = 50

cNum = 1

pieceSize = 50
playerPos = {}
playerDir = 0

#moveSpeed
PMS = 5
#viewDistance
PVD = 150
#fieldOfView
FOV = 80
#rayCastFidelity
RCF = 20

DRAWTIME = 1
#KEYPRESS
kp_key = -1

GAMERUNNING = True


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
    #win.addstr(0,0,"#")
    #win.addstr(winY-2,winX-2,"#")
    
    for x in range(0,winX-2):
        win.addstr(0,x,"#")
        win.addstr(winY-2,x,"#")
    for y in range(0,winY-2):
        win.addstr(y,0,"#")
        win.addstr(y,winX-2,"#")

def viewPrinting(win,winX,winY,view):
    global cNum

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

def inputThread(win,DRAWTIME,drawT_q, kp_key,key_q, GAMERUNNING,run_q):
    DRAWTIME = drawT_q.get()
    win.timeout(1)

    while GAMERUNNING:
        key = -1

        if(key_q.empty()):
            win.addstr(5,R.randint(5,50),str(R.randint(0,9)))
            key = win.getch()

            if(key != -1):
                win.addstr(6,R.randint(5,50),str(R.randint(0,9)))
                kp_key = key
                key_q.put(kp_key)
                time.sleep(1/10)

        else:
            pass

        GAMERUNNING = run_q.get() 

def animation(DRAWTIME, kp_key, GAMERUNNING):
    win = C.initscr()

    key_q = Q.Queue()
    drawT_q = Q.Queue()
    run_q = Q.Queue()

    inpThread = threading.Thread(target=inputThread,
                                 args=(win,DRAWTIME,drawT_q, kp_key,key_q, GAMERUNNING,run_q))

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

    written = False
    
    ### DRAWING LOOP
    while GAMERUNNING:
        run_q.put(GAMERUNNING)

        startTime = time.time()

        #16:9
        #winY = int(win.getmaxyx()[0])
        #winX = int((winY/9) * 16)

        winX = int(win.getmaxyx()[1])
        winY = int(win.getmaxyx()[0])

        #displayBorder draw
        borderDraw(win,winX,winY)
        
        #get view output from displaying(raycasting)
        view = displaying(playerPos,playerDir)

        #display all from rayCast (walls and stuff)
        viewPrinting(win,winX,winY,view)            

        win.addstr(13,13,str(R.randint(0,9)))

        if not(key_q.empty()):
            kp_key = key_q.get()
            win.addstr(15,15,str(R.randint(0,9)))
            written = True

            #if(C.Ke)
        elif(written == True):
            written = False
        
        #DRAWTIME measurement
        endTime = time.time()
        DRAWTIME = endTime-startTime
        drawT_q.put(DRAWTIME)

        if not(inpThread.is_alive()):
            #if not(Tstarted):
            inpThread.start()

        stime = time.time()
        while time.time() - stime <= 1/60:
            pass

        win.refresh()
        ### DRAWING LOOP


    if(inpThread.is_alive()):
        GAMERUNNING = False
        run_q.put(GAMERUNNING)

        inpThread.join()

    C.echo()
    C.endwin()


for y in range(len(playMap)):
    _y = list(playMap[y])

    for x in range(len(_y)):
        if(_y[x] == '.'):
            playerPos['y'] = (pieceSize*y)
            playerPos['x'] = (pieceSize*x)

#displaying(playerPos,playerDir)

animation(DRAWTIME, kp_key, GAMERUNNING)
