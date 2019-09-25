#!/usr/bin/env python3

import curses as C 
import math
import pyglet
from pyglet.gl import *
import random as R
import time
import sys
import termios
import tty
import os

sys.path.append('./data')
from mapData import *

#import list of levels from data/mapData.py
lvls = LevelList()


test_playMap = ["WWWWWWWWWWWWWW",
                "W            W",
                "W            W",
                "W  .    W    W",
                "W       RG   W",
                "W            W",
                "WWWWWWWWWWWWWW"]

WALL = "RGW"

WC = {'R':1,'G':3,'W':5}

#WALL_h = 50

inputKeys =  {'w':'forward', 
              's':'backward',
              'a':'left',
              'd':'right',
              'P':'exit'}

cNum = 1

pieceSize = 50
cornerSize = 5
playerPos = {}
playerDir = 0

#moveSpeed
PMS = 8
#rotationSpeed
PRS = 5
#viewDistance
PVD = 400
#fieldOfView
FOV = 80#VARIABLE - columns
#rayCastFidelity
RCF = 50


def displaying(_pos,_dir):
    rayOutput = []

    #for every FOV point send out a ray
    #+1 - fine number of rays (symetry)
    for loop in range(FOV+1):
        testDir = _dir - int(FOV/2) + loop

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
            forwardX = math.sin(math.radians(testDir))
            forwardY = math.cos(math.radians(testDir))

            #rayX = int(_PVD*forwardX)
            #rayY = int(_PVD*forwardY)

            #print(testDir-_dir)
            N = int(_PVD/math.cos(math.radians(testDir-_dir)))

            rayX = int(N*math.sin(math.radians(testDir)))
            rayY = int(N*math.cos(math.radians(testDir)))

            #print(rayX,rayY)
            #continue

            collision, corner = rayCast(rayX,rayY,_pos)

            if(collision != ' '):
                collided = True
                rayOutput.append([collision, _PVD, corner])
                break

        if not (collided):
            rayOutput.append([' ', PVD, corner])
            
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
                col, corner = getCollision(xPos, yPos, _pos['x']+rayX, _pos['y']+rayY)
                if(col):
                    #WALL
                    if(_y[x] in WALL):
                        return _y[x], corner


    return ' ', False

def getCollision(x,y, itemX, itemY):
    lowerBoundX = pieceSize*x - pieceSize/2
    upperBoundX = pieceSize*x + pieceSize/2

    lowerBoundY = pieceSize*y - pieceSize/2
    upperBoundY = pieceSize*y + pieceSize/2
     
    collision = False
    corner = False
    if(itemX >= lowerBoundX and itemX <= upperBoundX):
        if(itemY >= lowerBoundY and itemY <= upperBoundY):
            collision = True

            #BlockCorner
            if(lowerBoundX <= itemX <= lowerBoundX+cornerSize):
                if(lowerBoundY <= itemY <= lowerBoundY+cornerSize):
                    corner = True
                #if(upperBoundY >= itemY >= upperBoundY-cornerSize):
                #    corner = True
            if(upperBoundX >= itemX >= upperBoundX-cornerSize):
                #if(lowerBoundY <= itemY <= lowerBoundY+cornerSize):
                #    corner = True
                if(upperBoundY >= itemY >= upperBoundY-cornerSize):
                    corner = True

    return collision, corner

def getPlayerStartPos():
    for y in range(len(playMap)):
        _y = list(playMap[y])

        for x in range(len(_y)):
            if(_y[x] == '.'):
                playerPos['y'] = (pieceSize*y)
                playerPos['x'] = (pieceSize*x)

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

    screenWidth = int(winX+1)
    midY = int(winY/2)

    #linePerRay
    LPR = screenWidth / FOV

    lastValue = 0
    for rayIndex in range(FOV):
        actualValue = int(LPR*rayIndex)

        for i in range(actualValue-lastValue):
            height_HALF = int(midY - view[rayIndex][1]/15)

            xPos = lastValue + i

            for z in range(int(midY - view[rayIndex][1]/15)):
                #strop??
                if(z >= midY):
                    break
                
                if(view[rayIndex][0] in WALL):
                    if(view[rayIndex][1] < 100):
                        #win.addstr(midY + z, xPos+1, '#', C.color_pair(1) + C.A_BOLD)
                        #win.addstr(midY - z, xPos+1, '#', C.color_pair(1) + C.A_BOLD)

                        win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_BOLD)
                        win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_BOLD)
                        #win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_BOLD)

                        if(view[rayIndex][2]):
                            #win.addstr(midY + z, xPos+1, '#', C.color_pair(2) + C.A_BOLD)
                            #win.addstr(midY - z, xPos+1, '#', C.color_pair(2) + C.A_BOLD)

                            win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_BOLD)
                            win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_BOLD)

                    elif(view[rayIndex][1] < 200):
                        #win.addstr(midY + z, xPos+1, '#', C.color_pair(1))
                        #win.addstr(midY - z, xPos+1, '#', C.color_pair(1))

                        win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]))
                        win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]))

                        if(view[rayIndex][2]):
                            #win.addstr(midY + z, xPos+1, '#', C.color_pair(2))
                            #win.addstr(midY - z, xPos+1, '#', C.color_pair(2))

                            win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1))
                            win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1))

                    elif(view[rayIndex][1] < PVD):
                        #win.addstr(midY + z, xPos+1, '#', C.color_pair(1) + C.A_DIM)
                        #win.addstr(midY - z, xPos+1, '#', C.color_pair(1) + C.A_DIM)

                        win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_DIM)
                        win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_DIM)

                        if(view[rayIndex][2]):
                            #win.addstr(midY + z, xPos+1, '#', C.color_pair(2) + C.A_DIM)
                            #win.addstr(midY - z, xPos+1, '#', C.color_pair(2) + C.A_DIM)

                            win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_DIM)
                            win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_DIM)

                else:
                    win.addstr(int(midY) + z, xPos+1, ' ')
                    win.addstr(int(midY) - z, xPos+1, ' ')

            #FLOOR distance from player
            DFP = midY - height_HALF
            for i in range(DFP):
                if(i < 3):
                    win.addstr(winY-3-i, xPos+1, 'O', C.A_DIM)
                elif(i < 9):
                    win.addstr(winY-3-i, xPos+1, '-', C.A_DIM)
                elif(i < 20):
                    win.addstr(winY-3-i, xPos+1, '.', C.A_DIM)
                else:
                    win.addstr(winY-3-i, xPos+1, ' ', C.A_DIM)

        lastValue = actualValue

def getMinMap(playerPos):
    actMap = []
    for y in range(len(playMap)):
        row = []
        _y = list(playMap[y])

        for x in range(len(_y)):
            if(getCollision(x,y,playerPos['x'],playerPos['y'])[0]):
                _playerPX = x
                _playerPY = y
                row += 'O'
            elif(_y[x] == '.'):
                row += ' '
            else:
                row += str(_y[x])

        actMap += [row]

    return actMap

def getch():
    # https://wfww.jonwitts.co.uk/archives/896
    # adapted from https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_keyboard.py
    #
    # Works well better than Curses getch (lag on input - pressing even if no
    # input is being done!)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
    return ch

def getMap(lvlIndex, mapIndex):
    _map = lvls.levels[lvlIndex-1][mapIndex-1]

    _map.remove(_map[0])
    _map.remove(_map[len(_map)-2])

    _trans = _map.pop()
    print(_trans)
    _trans.remove('(') _trans.remove(')')
    print(_trans)
    
    return _map, _trans
    
    
def inputHandling(key):
    global playerPos, playerDir

    oldPos = playerPos.copy()

    if(key in inputKeys):
        if(inputKeys[key] == 'forward'):

            moveX = (int(PMS*math.sin(math.radians(playerDir))))
            moveY = (int(PMS*math.cos(math.radians(playerDir))))

            playerPos['x'] += moveX
            playerPos['y'] += moveY

        if(inputKeys[key] == 'backward'):

            moveX = (int(PMS*math.sin(math.radians(playerDir))))
            moveY = (int(PMS*math.cos(math.radians(playerDir))))

            playerPos['x'] -= moveX
            playerPos['y'] -= moveY

        if(inputKeys[key] == 'left'):

            playerDir -= PRS
            if(playerDir < 0):
                playerDir = 360 + playerDir 

            if(playerDir >= 360):
                playerDir = playerDir - 360

        if(inputKeys[key] == 'right'):
            
            playerDir += PRS
            if(playerDir < 0):
                playerDir = 360 + playerDir 

            if(playerDir >= 360):
                playerDir = playerDir - 360


        for y in range(len(playMap)):
            for x in range(len(playMap[y])):
                if(playMap[y][x] in WALL):
                    if(getCollision(x, y, playerPos['x'], playerPos['y'])[0]):
                        playerPos = oldPos

def mainProgram():
    playMap, transMap = getMap(1,1)

    print(playMap,transMap)
    quit()
    
    getPlayerStartPos()

    win = C.initscr()

    # DRAWPHASE 0
    # INPUTPHASE 1
    PHASE = 0
    GAMERUNNING = True
    
    INPUT = False
    key = ''

    # 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    #color pairs
    C.start_color()
    C.use_default_colors()
    C.init_pair(WC['W'], C.COLOR_WHITE, -1)
    C.init_pair(WC['W']+1, C.COLOR_WHITE, C.COLOR_WHITE)

    C.init_pair(WC['R'], C.COLOR_RED, -1)
    C.init_pair(WC['R']+1, C.COLOR_RED, C.COLOR_RED)

    C.init_pair(WC['G'], C.COLOR_GREEN, -1)
    C.init_pair(WC['G']+1, C.COLOR_GREEN, C.COLOR_GREEN)

    # hide cursor
    C.noecho()
    C.cbreak()
    C.curs_set(0)

    win.clear()
    win.refresh()
    
    while GAMERUNNING:
        if(PHASE == 0):
            ### DRAW LOOP
            win.clear()
            
            #window resolution (not much)
            winX = int(win.getmaxyx()[1])
            winY = int(win.getmaxyx()[0])

            #displayBorder draw
            #borderDraw(win,winX,winY)
            win.box()
            
            #get view output from displaying(raycasting)
            view = displaying(playerPos,playerDir)

            #display all from rayCast (walls and stuff)
            viewPrinting(win,winX,winY,view)            

            #win.addstr(13,13,str(R.randint(0,9)))

            #win.addstr(5,5,"DRAWPHASE")
            win.addstr(3,3,"POS: X:{} Y:{}".format(playerPos['x'],playerPos['y']))
            win.addstr(4,3,"DIR: {}".format(playerDir))
            rootP = 15
    
            #mmmMap = getMinMap(playerPos)
            #for y in range(len(playMap)):
            #    for x in range(len(playMap[y])):
            #        win.addstr(rootP - y, rootP+x, mmmMap[y][x])


            PHASE = 1
            win.refresh()
            ### DRAW LOOP

        elif(PHASE == 1):
            ### INPUT LOOP
            win.addstr(5,5,"INPUTPHASE")
            key = getch()
            inputHandling(key)
            if(key == 'P'):
                GAMERUNNING = False

            #INPUT = True
            PHASE = 0

    C.endwin()
    C.echo()
    C.curs_set(0)

    #if(inpThread.is_alive()):
    #    GAMERUNNING = False
    #    run_q.put(GAMERUNNING)

    #    inpThread.join()

    C.echo()
    C.endwin()


#displaying(playerPos,playerDir)
#quit()

pWindow = pyglet.window.Window(1280,720, "SUMMER 2019", resizable = False)
#screen = pyglet.window.get_platform().get_default_display().get_default_screen()

def tick(t):

    pass

c = 0.0
gradUp=True
@pWindow.event
def on_draw():
    global c
    global gradUp

    #pWindow.set_location(0,0)
    img = pyglet.image.load("data/summer2019_en.jpg")
    tex = img.get_texture()

    if(gradUp and c <= 1.0):
        c+=0.01
        c+=1
        if(c >= 1):
            gradUp = False
    elif(gradUp == False and c > 0):
        c-=0.05
        c-=1
    elif(gradUp == False and c <= 0):
        pyglet.app.exit()

    glColor3f(c,c,c)
    tex.blit(0,0)

pyglet.clock.schedule_interval(tick, 1/60)
pyglet.app.run()
pWindow.close()

mainProgram()
