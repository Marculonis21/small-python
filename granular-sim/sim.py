#!/usr/bin/env python3

from pyglet.gl import *
import pyglet as P

import math

import time
from multiprocessing import Pool
import multiprocessing

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

def drawText(text,sX,sY,size):
    label = P.text.Label(str(text),
                         font_size=size,
                         x=sX,
                         y=sY,
                         anchor_x='center',
                         anchor_y='center')
    label.draw()

def drawMode(sX,sY,size,padX=-1):
    chosen = GRAIN_TYPE_SELECTED
    selSize = size/5

    if(padX == -1):
        padX = (3/2)*size

    loop = 0
    for s in STATELIST.values():
        scolor = s.split('|')[1]
        cColor = scolor.split(',')
        modeColor = [float(cColor[0]),float(cColor[1]),float(cColor[2])]

        if(chosen == loop+1):
            drawSquare(sX+(padX*loop) - selSize/2, sY - selSize/2, size+selSize, [0.5,0.5,0.5])
        drawSquare(sX+(padX*loop), sY, size, modeColor)

        loop += 1

def checkerBoard(size):
    for i in range(int(WIN_WIDTH/size)):
        drawLine(i*size,0,i*size,win.height)
        drawLine(0,i*size,win.width,i*size)

def cursorDrawing():
    global xMouse,yMouse,mouseWheel,BLOCK_SIZE

    radius = ((mouseWheel-1) * BLOCK_SIZE)
    angle = 2*math.pi/72
    for loop in range(72):
        _x = xMouse + (math.cos(angle*loop)*radius)
        _y = yMouse + (math.sin(angle*loop)*radius)
        
        __x = math.floor(_x/BLOCK_SIZE)
        __y = math.floor(_y/BLOCK_SIZE)
        drawSquare(__x*BLOCK_SIZE,__y*BLOCK_SIZE,BLOCK_SIZE, [1,1,1])

def grainAdding():
    global xMouse,yMouse,mouseWheel,BLOCK_SIZE

    for _wIter in reversed(range(0,mouseWheel)):
        radius = (_wIter * BLOCK_SIZE)
        angle = 2*math.pi/36
        for loop in range(36):
            _x = xPress + (math.cos(angle*loop)*radius)
            _y = yPress + (math.sin(angle*loop)*radius)
            
            __x = math.floor(_x/BLOCK_SIZE)
            __y = math.floor(_y/BLOCK_SIZE)

            if(GRAINMAP[__x][__y] != 0):
                pass
            else:
                _grain = [__x,__y,GRAIN_TYPE_SELECTED,False,0]

                GRAINMAP[__x][__y] = _grain
                GRAINLIST.append(_grain)

def get_grain_color(state):
    scolor = state.split('|')[1]
    cColor = scolor.split(',')
    modeColor = [float(cColor[0]),float(cColor[1]),float(cColor[2])]

    return modeColor

def update_grain_map():
    """ PROCESS GRAINMAP """
    global GRAINMAP,GRAINLIST

    MAXW = int(WIN_WIDTH/BLOCK_SIZE)

    GRAINMAP = [[0 for x in range(MAXW)] for y in range(MAXW)]

    for grain in GRAINLIST:
        try:
            GRAINMAP[grain[0]][grain[1]] = grain

        except:
            pass

def check_static(testList):
    """ CHANGES GRAINS TO STATIC OBJECTS """
    global GRAINLIST
    global static_GRAINLIST
    global GRAINMAP

    for grain in testList:
        try:
            x = grain[0]
            y = grain[1]

            found = False
            if (x-1 < 0 or y-1 < 0):
                continue

            if(GRAINMAP[x-1][y-1] == 0):
                found = True
            if(GRAINMAP[x][y-1] == 0):
                found = True
            if(GRAINMAP[x+1][y-1] == 0):
                found = True
            if(GRAINMAP[x-1][y] == 0):
                found = True
            if(GRAINMAP[x+1][y] == 0):
                found = True
            if(GRAINMAP[x-1][y+1] == 0):
                found = True
            if(GRAINMAP[x][y+1] == 0):
                found = True
            if(GRAINMAP[x+1][y+1] == 0):
                found = True

            #if not (found): # STATIC
            #    grain[3] = True
            #else:
            #    grain[3] = False

            if not (found):
                nGrain = grain.copy()
                nGrain[3] = True
                GRAINMAP[x][y] = nGrain

                static_GRAINLIST.append(nGrain)
                GRAINLIST.remove(grain)
                testList.remove(grain)

        except:
            pass

def move_grain(grain,newX,newY):
    """ GRAIN fMOVING """
    global GRAINMAP

    oldX = grain[0]
    oldY = grain[1]
    GRAINMAP[oldX][oldY] = 0

    grain[0] = newX
    grain[1] = newY

    return [[grain, grain[0], grain[1]]]

def sim():
    """ GRAIN SIM """
    global GRAINMAP, GRAINLIST

    MAXW = int(WIN_WIDTH/BLOCK_SIZE)

    staticTestList = []
    moveHistory = []
    for grain in GRAINLIST:
        x,y,STATE,STATIC,r = grain
        
        if not (STATIC):
            if(STATE == 1): #STATE SOLID
                try:
                    if(y > 0):
                        if(GRAINMAP[x][y-1] == 0): #SAND SIM
                            moveHistory += move_grain(grain, x, y-1)
                            grain[4] = 0
                        elif(GRAINMAP[x-1][y-1] == 0 and x > 0):
                            moveHistory += move_grain(grain, x-1,y-1)
                            grain[4] = 0
                        elif(GRAINMAP[x+1][y-1] == 0 and x < MAXW):
                            moveHistory += move_grain(grain, x+1,y-1)
                            grain[4] = 0
                        else:
                            grain[4] += 1
                            if(grain[4] >= 50):
                                staticTestList += [grain]
                except:
                    pass

            elif(STATE == 2): #STATE LIQUID
                try:
                    if(y > 0):
                        if(GRAINMAP[x][y-1] == 0): #SAND SIM
                            moveHistory += move_grain(grain, x, y-1)
                            grain[4] = 0
                        elif(GRAINMAP[x-1][y-1] == 0 and x > 0):
                            moveHistory += move_grain(grain, x-1,y-1)
                            grain[4] = 0
                        elif(GRAINMAP[x+1][y-1] == 0 and x < MAXW):
                            moveHistory += move_grain(grain, x+1,y-1)
                            grain[4] = 0
                        elif(GRAINMAP[x+1][y] == 0 and x < MAXW):
                            moveHistory += move_grain(grain, x+1,y)
                            grain[4] = 0
                        elif(GRAINMAP[x-1][y] == 0 and x > 0):
                            moveHistory += move_grain(grain, x-1,y)
                            grain[4] = 0
                        else:
                            grain[4] += 1
                            if(grain[4] >= 50):
                                staticTestList += [grain]
                    else:
                        if(GRAINMAP[x+1][y] == 0 and x < MAXW):
                            moveHistory += move_grain(grain, x+1,y)
                            grain[4] = 0
                        elif(GRAINMAP[x-1][y] == 0 and x > 0):
                            moveHistory += move_grain(grain, x-1,y)
                            grain[4] = 0
                        else:
                            grain[4] += 1
                            if(grain[4] >= 50):
                                staticTestList += [grain]
                except:
                    pass
            elif(STATE == 3):
                pass


    for i in moveHistory:
        GRAINMAP[i[1]][i[2]] = i[0]

    if(len(staticTestList) > 0):
        check_static(staticTestList)

    #update_grain_map()

    #check_static()


### mouse stuff
xPress = -1
yPress = -1

xMouse = -1
yMouse = -1

mouseWheel = 5 

### constants
WIN_WIDTH = 800
BLOCK_SIZE = 10
DRAW_MAP = False

###SIM USED STUFF
# 0 = eraser, 1 = solid, 2 = liquid
GRAIN_TYPE_SELECTED = 1

# list of all states
STATELIST = {1:"sand|0.8,0.8,0|", 
             2:"water|0,0,0.8|",
             3:"gas|0.1,0.8,0.1|"}

# list of grain
### GRAIN - POSX,POSY, STATE[SOLID - 1, LIQUID - 2], STATIC/AWAKE[NO - False,YES - True], staticLoop;
GRAINLIST = []

static_GRAINLIST = []

# map of grain - for physics and colisions ++ drawing
GRAINMAP = []

win = P.window.Window(WIN_WIDTH,WIN_WIDTH,caption="Grain sim")
win.set_mouse_visible(False)
fps_display = P.window.FPSDisplay(window=win)
glClearColor(0.25,0.25,0.25, 1)

@win.event
def on_draw():
    """ DRAW FUNCTION """
    win.clear()
    glColor3f(1,1,1)

    if(DRAW_MAP):
        checkerBoard(BLOCK_SIZE)

    global xPress,yPress,xMouse,yMouse
    if(xPress != -1): # ADD TO GRAINLIST
        grainAdding()
        xMouse = yMouse = -1

    elif(xMouse != -1): # CURSOR
        cursorDrawing()

    """
    for grain in GRAINLIST: # DRAWING GRAINLIST
        if(grain[3]):
            drawSquare(grain[0]*BLOCK_SIZE,grain[1]*BLOCK_SIZE,BLOCK_SIZE, [0.8,0,0])
        else:
            drawSquare(grain[0]*BLOCK_SIZE,grain[1]*BLOCK_SIZE,BLOCK_SIZE, [0,0.8,0])
    """

    sTime = time.time()

    #grainLDraw()
    #sgrainLDraw()

    """
    processes = []
    parts = 4
    pWidth = len(GRAINMAP)/parts
    
    x = -1
    processList = []
    for i in range(int(parts**2)):
        y = math.floor(i/parts)
        x += 1
        if(x == parts):
            x = 0

        processList += [[x,y,parts,GRAINMAP]]

    p = Pool(processes=1)
    data = p.map(testDrawScene, processList)
    p.close()
    #print(data)

    x = -1
    for i in range(int(parts**2)):
        y = math.floor(i/parts)
        x += 1
        if(x == parts):
            x = 0
        if(data[i]):
            for _y in range(int(pWidth*y), int(pWidth*y + pWidth)):
                for _x in range(int(pWidth*x),int(pWidth*x + pWidth)):
                    if(GRAINMAP[_x][_y] != 0):
                        color = get_grain_color(STATELIST[GRAINMAP[_x][_y][2]])
                        drawSquare(_x*BLOCK_SIZE,_y*BLOCK_SIZE,BLOCK_SIZE, color)

    """

    for y in range(len(GRAINMAP)):
        for x in range(len(GRAINMAP)):
            if(GRAINMAP[x][y] != 0):
                color = get_grain_color(STATELIST[GRAINMAP[x][y][2]])
                drawSquare(x*BLOCK_SIZE,y*BLOCK_SIZE,BLOCK_SIZE, color)

    print("looking through took {} seconds".format(time.time() - sTime))
    sim()

    drawText("Particles: {}/{}".format(len(GRAINLIST),len(static_GRAINLIST)),80,win.height-15,15)

    drawMode(win.width-200,win.height-80,50)
    
    fps_display.draw()

def grainLDraw():
    for grain in GRAINLIST:
        color = get_grain_color(STATELIST[grain[2]])
        drawSquare(grain[0]*BLOCK_SIZE,grain[1]*BLOCK_SIZE,BLOCK_SIZE, color)

def sgrainLDraw():
    for grain in static_GRAINLIST:
        color = get_grain_color(STATELIST[grain[2]])
        drawSquare(grain[0]*BLOCK_SIZE,grain[1]*BLOCK_SIZE,BLOCK_SIZE, color)

def testDrawScene(values):
    """ MULTIPROCESSING TEST """
    x = values[0]
    y = values[1]
    parts = values[2]
    GRAINMAP = values[3]

    pWidth = len(GRAINMAP)/parts

    for _y in range(int(pWidth*y), int(pWidth*y + pWidth)):
        for _x in range(int(pWidth*x),int(pWidth*x + pWidth)):
            if(GRAINMAP[_x][_y] != 0):
                #print("YES process end, working at xs: {}; ys: {}".format(pWidth*x,pWidth*y))
                #workArea[index] = [_x,_y,1]
                return True

    #print("NO process end, working at xs: {}; ys: {}".format(pWidth*x,pWidth*y))
    #workArea[index] = [_x,_y,0]
    return False

@win.event
def on_key_press(s,mod):
    """ KEYBOARD INPUTS """
    if(s == P.window.key.F1):
        global DRAW_MAP
        if(DRAW_MAP):
            DRAW_MAP = False
        else:
            DRAW_MAP = True
    if(s == P.window.key.N):
        global GRAINLIST, static_GRAINLIST
        GRAINLIST = []
        static_GRAINLIST = []
        update_grain_map()

    global GRAIN_TYPE_SELECTED
    if(s == P.window.key.NUM_0):
        GRAIN_TYPE_SELECTED = 0
    if(s == P.window.key.NUM_1):
        GRAIN_TYPE_SELECTED = 1
    if(s == P.window.key.NUM_2):
        GRAIN_TYPE_SELECTED = 2
    if(s == P.window.key.NUM_3):
        GRAIN_TYPE_SELECTED = 3

@win.event
def on_mouse_drag(x, y, dx, dy, c, d):
    """ MOUSE INPUT1 """
    global xPress, yPress 
    xPress = x
    yPress = y

@win.event
def on_mouse_press(x,y ,c,d):
    """ MOUSE INPUT2 """ 
    global xPress, yPress
    xPress = x
    yPress = y

@win.event
def on_mouse_motion(x,y ,c,d):
    """ MOUSE MOTION """ 
    global xMouse, yMouse
    xMouse = x
    yMouse = y

@win.event
def on_mouse_scroll(x,y,scroll_x,scroll_y):
    """ MOUSE WHEEL EVENT """ 
    global mouseWheel
    if(1 <= mouseWheel <= 10):
        mouseWheel += scroll_y

    if(mouseWheel == 0):
        mouseWheel = 1

    if(mouseWheel == 11):
        mouseWheel = 10

@win.event
def on_mouse_release(x, y, button, modifiers):
    """ MOUSE INPUT END """ 
    global xPress, yPress
    xPress = yPress = -1

@win.event
def tick(t):
    """ TICK """
    pass

if __name__ == "__main__":
    update_grain_map()

    P.clock.schedule_interval(tick, 1/120)
    P.app.run()
