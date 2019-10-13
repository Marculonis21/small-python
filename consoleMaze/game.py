#!/usr/bin/env python3

#Project for competition by ITnetwork.cz. 
#Done by Marek Šrůma in about 2 months working on and off the project.
#Feel free to dig in as you wish, hopefully my code is readable for others.
#I'll be surely happy to share a word with people,
#who are willing to talk about the game and the code (ideas, etc.).
#Contact address: marek.sruma@gmail.com
#
#Needless to say I'm not a professional programmer, but this project was a lot of fun for me!
#
#PS.: Additional content I was thinking about: more maps, in game map creator, enhanced 3D feel

import math
import random as R
import time
import sys
import termios
import tty
import os
import curses as C 

while True:
    try:
        import pyglet
        from pyglet.gl import *
        break
    except ModuleNotFoundError:
        os.system("pip3 install pyglet")

while True:
    try:
        import webbrowser
        break
    except ModuleNotFoundError:
        os.system("pip3 install webbrowser")

sys.path.append('./data')
import mapData
import menuData


#import list of levels from data/mapData.py
mapData.makeLvls()
lvls = mapData.levels

test_playMap = ["WWWWWWWWWWWWWW",
                "W            W",
                "W            W",
                "W  .    W    W",
                "W       RG   W",
                "W            W",
                "WWWWWWWWWWWWWW"]

#mapdata variables
playMap = []
mapPorts = []
lvlStage = 0
gameEnd = False
lvlEnd = False

#input
inputKeys =  {'w':'forward', 
              's':'backward',
              'a':'left',
              'd':'right',
              'P':'exit'}

#world settings 
pieceSize = 50
cornerSize = 8

#player variables
playerPos = {}
playerDir = 270

#WALLS+COLORS
WC = {'R':1,'G':3,'W':5,'B':7,'M':9,'Y':11}
WALL = "".join(i for i in WC.keys())

#MORE OPTIONS
#moveSpeed
PMS = 12
#rotationSpeed
PRS = 6
#viewDistance
PVD = 400
#fieldOfView
FOV = 80
#rayCastFidelity
RCF = 50
#portrotationbias
PRB = 90


def displaying(_pos,_dir):
    rayOutput = []

    #for every FOV point send out a ray
    #+1 - fine number of rays (symetry)
    for loop in range(FOV+1):
        testDir = _dir + int(FOV/2) - loop

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

            N = int(_PVD/math.cos(math.radians(testDir-_dir)))

            rayX = int(N*math.sin(math.radians(testDir)))
            rayY = int(N*math.cos(math.radians(testDir)))

            collision, corner = rayCast(rayX,rayY,_pos)

            if(collision != ' '):
                collided = True
                rayOutput.append([collision, _PVD, corner])
                break

        if not (collided):
            rayOutput.append([' ', PVD, corner])
            
    return rayOutput

def rayCast(_rayX,_rayY,_pos):
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
            if(upperBoundX >= itemX >= upperBoundX-cornerSize):
                if(upperBoundY >= itemY >= upperBoundY-cornerSize):
                    corner = True

    return collision, corner

def getPlayerStartPos():
    global playerPos, playerDir
    playerDir = 270

    for y in range(len(playMap)):
        _y = list(playMap[y])

        for x in range(len(_y)):
            if(_y[x] == '.'):
                playerPos['y'] = (pieceSize*y)
                playerPos['x'] = (pieceSize*x)

def borderDraw(win,winX,winY):
    for x in range(0,winX-2):
        win.addstr(0,x,"#")
        win.addstr(winY-2,x,"#")
    for y in range(0,winY-2):
        win.addstr(y,0,"#")
        win.addstr(y,winX-2,"#")

def viewPrinting(win,winX,winY,view):
    global cNumf

    screenWidth = int(winX+1)
    midX = int(screenWidth/2)
    midY = int(winY/2)

    #linePerRay
    LPR = screenWidth / FOV

    lastValue = 0
    #going through rays and spreading them through all columns on the screen
    for rayIndex in range(FOV):
        actualValue = int(LPR*rayIndex)

        for i in range(actualValue-lastValue):
            height_HALF = int(midY - view[rayIndex][1]/15)

            xPos = lastValue + i

            for z in range(int(midY - view[rayIndex][1]/15)):
                if(z >= midY):
                    break
                
                #WALL PRINTING
                if(view[rayIndex][0] in WALL):
                    if(view[rayIndex][1] < 100):
                        win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_BOLD)
                        win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_BOLD)

                        if(view[rayIndex][2]):
                            win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_BOLD)
                            win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_BOLD)

                    elif(view[rayIndex][1] < 200):
                        win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]))
                        win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]))

                        if(view[rayIndex][2]):
                            win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1))
                            win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1))

                    elif(view[rayIndex][1] < PVD):
                        win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_DIM)
                        win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]) + C.A_DIM)

                        if(view[rayIndex][2]):
                            win.addstr(midY + z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_DIM)
                            win.addstr(midY - z, xPos+1, '#', C.color_pair(WC[view[rayIndex][0]]+1) + C.A_DIM)

                else:
                    win.addstr(int(midY) + z, xPos+1, ' ')
                    win.addstr(int(midY) - z, xPos+1, ' ')

            #FLOOR distance from player
            DFP = midY - height_HALF
            
            #FLOORSHADOW
            for i in range(DFP - 2):
                #Center point distance (for floor shading)
                CPD = math.sqrt(abs(midX-3 - xPos+1)**2 + abs(winY - winY-i-250)**2) 

                if(CPD < 255):
                    win.addstr(winY-3-i, xPos+1, 'O')
                elif(CPD < 265):
                    win.addstr(winY-3-i, xPos+1, '-')
                elif(CPD < 270):
                    win.addstr(winY-3-i, xPos+1, '-', C.A_DIM)

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
    global playMap,lvlStage,mapPorts
    global gameEnd
    gameEnd = False

    #get mapdata
    _map = lvls[lvlIndex][mapIndex].copy()

    #format map
    _map.remove(_map[0])
    _map.remove(_map[len(_map)-2])

    _trans = _map.pop()
    _trans = _trans.translate({ord(i): None for i in '()'})
    opts = _trans.split('|')
    opts.pop()

    #update map settings 
    playMap = _map
    lvlStage = lvlIndex

    #get ports on map
    _ports = []
    for item in opts:
        s1 = item.split('_')
        s2 = s1[2].translate({ord(i): None for i in '[]'}).split(',')

        if('*' in s1[0]):
            xs1 = s1[0].split('*')
            p = [int(xs1[0]), int(xs1[1])-1, int(s1[1]), [int(s2[0]),int(s2[1])]]
        else:
            p = [ int(s1[0]),    lvlStage, int(s1[1]), [int(s2[0]),int(s2[1])]]

        _ports.append(p)

    #update ports settings
    mapPorts = _ports

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

            playerDir += PRS
            if(playerDir < 0):
                playerDir = 360 + playerDir 

            if(playerDir >= 360):
                playerDir = playerDir - 360

        if(inputKeys[key] == 'right'):
            
            playerDir -= PRS
            if(playerDir < 0):
                playerDir = 360 + playerDir 

            if(playerDir >= 360):
                playerDir = playerDir - 360


        _tp_lvlStage = -2
        _tp_lvl = -1
        _tp_distx = -1
        _tp_disty = -1
        for y in range(len(playMap)):

            #If there is a need for port (end of the for loop)
            if(_tp_lvlStage != -2):
                getMap(_tp_lvlStage, _tp_lvl)

                playerPos['x'] += _tp_distx*pieceSize
                playerPos['y'] += _tp_disty*pieceSize
                break

            for x in range(len(playMap[y])):

                #Player wall collision
                if(playMap[y][x] in WALL):
                    if(getCollision(x, y, playerPos['x'], playerPos['y'])[0]):
                        playerPos = oldPos

                #Map teleports
                if(playMap[y][x] in "012345678"):
                    if(getCollision(x, y, playerPos['x'], playerPos['y'])[0]):
                        for item in mapPorts:
                            if(item[0] == int(playMap[y][x])):
                                lowBound = item[2] - PRB/2
                                upBound = item[2] + PRB/2

                                if(lowBound < 0):
                                    lowBound = 360 + lowBound 

                                if(upBound >= 360):
                                    upBound = upBound - 360

                                if(item[2] == 0):
                                    if(lowBound <= playerDir <= 360
                                           or 0 <= playerDir <= upBound):
                                        _tp_lvlStage = item[1]
                                        _tp_lvl = item[0]
                                        _tp_distx = item[3][0]
                                        _tp_disty = item[3][1]
                                        break

                                else:
                                    if(lowBound <= playerDir <= upBound):
                                        _tp_lvlStage = item[1]
                                        _tp_lvl = item[0]
                                        _tp_distx = item[3][0]
                                        _tp_disty = item[3][1]
                                        break

                if(playMap[y][x] in "9"):
                    if(getCollision(x, y, playerPos['x'], playerPos['y'])[0]):
                        if(lvlStage == 0):
                            global lvlEnd
                            lvlEnd = True

                        else:
                            global gameEnd
                            gameEnd = True

                        
def menuDrawCenter(win, x,y,text, BOLD = False, SELECTED = False):
    label = text
    centXText = int(len(label[0])/2)
    loop = 0
    for row in label:
        if(BOLD or SELECTED):
            win.addstr(y+loop, x-centXText, row, C.A_BOLD)

            if(SELECTED):
                win.addstr(y+loop, x-(centXText+15), menuData.arrow[loop], C.A_BOLD)

        else:
            win.addstr(y+loop, x-centXText, row)

        loop += 1

def cursesBox(win, x, y, xScale, yScale):
    for _x in range(xScale):
        win.addstr(y, x+_x, '-')
        win.addstr(y+yScale, x+_x, '-')
    for _y in range(yScale):
        win.addstr(y+_y, x, '|')
        win.addstr(y+_y, x+xScale, '|')

    win.addstr(y,x,'#')
    win.addstr(y+yScale,x,'#')
    win.addstr(y,x+xScale,'#')
    win.addstr(y+yScale,x+xScale,'#')

def menuPhase(win):
    menuSelect = 0
    PRESSED = -1
    PHASE = 0
    while True:
        if(PHASE == 0):
            midX = int((win.getmaxyx()[1]+1)/2)

            win.clear()
            
            try:
                if(PRESSED == -1): #NOTHING SELECTED
                    menuDrawCenter(win, midX, 2, menuData.topName, True)

                    for i in range(4):
                        menuDrawCenter(win, midX, 15+(8*i), menuData.signs[i], False, (menuSelect == i))
                        if(i == 3):
                            win.addstr(win.getmaxyx()[0]-3, win.getmaxyx()[1] - 54,
                                    "GAME DEVELOPED FOR 2019 ITNETWORK.CZ SUMMER CONTEST")
                            cursesBox(win, win.getmaxyx()[1]-56,win.getmaxyx()[0] - 4, 54, 2)

                            win.addstr(win.getmaxyx()[0]-5, 3,
                                    " UP - W || DOWN - S")
                            win.addstr(win.getmaxyx()[0]-3, 3,
                                    "     SELECT - D    ")
                            cursesBox(win, 1, win.getmaxyx()[0]-6, 23, 4)

                elif(PRESSED == 0): #START
                    return "game"

                elif(PRESSED == 1): #HELP 
                    win.addstr(10, int(win.getmaxyx()[1]/2)-11 , "TO MOVE AROUND IN GAME:")
                    win.addstr(11, int(win.getmaxyx()[1]/2)-11, "-----------------------")

                    win.addstr(13, int(win.getmaxyx()[1]/2)-11, "      W - Forward      ")
                    win.addstr(14, int(win.getmaxyx()[1]/2)-11, "      S - Backward     ")
                    win.addstr(15, int(win.getmaxyx()[1]/2)-11, "      A - Rotate Left  ")
                    win.addstr(16, int(win.getmaxyx()[1]/2)-11, "      D - Rotate Right ")
                    win.addstr(17, int(win.getmaxyx()[1]/2)-11, "      P - Exit to menu ")


                    win.addstr(21, int(win.getmaxyx()[1]/2)-4,  "IN MENU:")
                    win.addstr(22, int(win.getmaxyx()[1]/2)-4,  "--------")

                    win.addstr(24, int(win.getmaxyx()[1]/2)-4,  " W - Up ")
                    win.addstr(25, int(win.getmaxyx()[1]/2)-4,  " S - Down")
                    win.addstr(26, int(win.getmaxyx()[1]/2)-4,  " D - Select")

                    cursesBox(win, int(win.getmaxyx()[1]/2) - 14, 8, 28, 20)

                    win.addstr(31, int(win.getmaxyx()[1]/2)-3, "About:")
                    win.addstr(32, int(win.getmaxyx()[1]/2)-3, "------")

                    win.addstr(34, int(win.getmaxyx()[1]/2)-24, "The game was made as a part of 2019 summer contest")

                    win.addstr(36, int(win.getmaxyx()[1]/2)-12, "AUTHOR: MAREK SRUMA  (CZE)")
                    win.addstr(37, int(win.getmaxyx()[1]/2)-14, "CONTACT: marek.sruma@gmail.com")

                    win.addstr(38, int(win.getmaxyx()[1]/2)-31, "https://github.com/Marculonis21/main-python/tree/master/consoleMaze")

                    menuDrawCenter(win, midX, win.getmaxyx()[0] - 10, menuData.back, False, True)
                    pass

                elif(PRESSED == 3): #EXIT
                    C.endwin()
                    C.echo()
                    C.curs_set(0)
                    return "exit"

            except:
                pass

            win.box()
    
            PHASE = 1

            win.refresh()
        
        elif(PHASE == 1):
            key = getch()

            if(PRESSED == -1): #IN MENU
                if(key == "w" or key == 'W'):
                    menuSelect -= 1
                    if(menuSelect < 0):
                        menuSelect = 3
                elif(key == "s" or key == 'S'):
                    menuSelect += 1
                    if(menuSelect > 3):
                        menuSelect = 0
                
                if(key == 'd' or key == 'D'):
                    if(menuSelect == 2):
                        webbrowser.open_new_tab("https://www.itnetwork.cz/programovani/programatorske-souteze/itnetwork-summer-2019")

                    else:
                        PRESSED = menuSelect

            elif(PRESSED == 1): #IN HELP
                if(key == 'd' or key == 'D'):
                    PRESSED = -1

            if(key == 'P' or key == 'p'):
                break

            PHASE = 0

def gamePhase(win):
    getMap(0,0)

    getPlayerStartPos()

    # DRAWPHASE 0
    # INPUTPHASE 1
    PHASE = 0
    GAMERUNNING = True

    INFOTIME = True
    INFOPRESS = {'W':False,'S':False,'A':False,'D':False,'P':False}

    while GAMERUNNING:
        if(PHASE == 0):
            drawTimeStart = time.time()

            ### DRAW LOOP
            win.clear()
            
            winX = int(win.getmaxyx()[1])
            winY = int(win.getmaxyx()[0])

            #get view output from displaying(raycasting)
            view = displaying(playerPos,playerDir)

            #display all from rayCast (walls and stuff)
            viewPrinting(win,winX,winY,view)            

            #displayBorder 
            #borderDraw(win,winX,winY)
            win.box()

            #TUTORIAL at the start
            if(INFOTIME):
                INFOTIME = infoPhase(win, INFOTIME, INFOPRESS)
                
                if not(INFOTIME):
                    win.refresh()
                    continue

            #FOR DEBUGING
            #-----------------
            try:
            #    #POS + DIR
                win.addstr(3,3,"POS: X:{} Y:{}".format(playerPos['x'],playerPos['y']))
                win.addstr(4,3,"DIR: {}".format(playerDir))

            #    #MINIMAP
                rootP = 15
                mmmMap = getMinMap(playerPos)
                for y in range(len(playMap)):
                    for x in range(len(playMap[y])):
                        win.addstr(rootP - y, rootP+x, mmmMap[len(playMap)-1-y][x])

                win.addstr(rootP + 3, rootP, str(mapPorts))
            except:
                pass
            #-----------------

            #CHANGE TO INPUT PHASE
            PHASE = 1

            #DRAWTIME
            while time.time() - drawTimeStart <= 1/10:
                pass

            win.refresh()
            ### DRAW LOOP

        elif(PHASE == 1):
            ### INPUT LOOP
            key = getch()
            if(INFOTIME):
                if(key in inputKeys or key.upper() in inputKeys):
                    s = key.upper()
                    INFOPRESS[s] = True
                

            inputHandling(key)

            if (gameEnd):
                gameEndFunc(win)
                break
            
            global lvlEnd
            if (lvlEnd):
                lvlEnd = False
                gameEndFunc(win, True)
                getMap(1,0)
                getPlayerStartPos()

            if not(INFOTIME):
                if(key == 'P' or key == 'p'):
                    GAMERUNNING = False

            PHASE = 0

def gameEndFunc(win, lvl = False):
    for i in range(10):
        win.addstr(int(win.getmaxyx()[0]/2)-8+i, int(win.getmaxyx()[1]/2)-10, ' '*19)

    cursesBox(win,int(win.getmaxyx()[1]/2)-10, int(win.getmaxyx()[0]/2)-8, 19,10)

    if not (lvl):
        win.addstr(int(win.getmaxyx()[0]/2)-3, int(win.getmaxyx()[1]/2)-8, "YOU WON THE GAME")
        win.addstr(int(win.getmaxyx()[0]/2)-2, int(win.getmaxyx()[1]/2)-8, "----------------")

    else:
        win.addstr(int(win.getmaxyx()[0]/2)-3, int(win.getmaxyx()[1]/2)-8, "  SECOND LEVEL  ")
        win.addstr(int(win.getmaxyx()[0]/2)-2, int(win.getmaxyx()[1]/2)-8, "----------------")

    win.refresh()


    time.sleep(3)
    getch()

def infoPhase(win, INFOTIME, PRESSED):
    if not (INFOTIME):
        return False
    
    else:
        for i in range(16):
            win.addstr(int(win.getmaxyx()[0]/2)-8+i, int(win.getmaxyx()[1]/2)-14,' '*30)
            cursesBox(win,int(win.getmaxyx()[1]/2)-14, int(win.getmaxyx()[0]/2)-8, 29,16)

        #Writing the start tutorial
        win.addstr(int(win.getmaxyx()[0]/2)-6, int(win.getmaxyx()[1]/2)-7,    "Small Tutorial:")
        win.addstr(int(win.getmaxyx()[0]/2)-5, int(win.getmaxyx()[1]/2)-7,    "---------------")

        done = True

        if(PRESSED['W']):
            win.addstr(int(win.getmaxyx()[0]/2) - 3, int(win.getmaxyx()[1]/2)-7, "  W - Forward  ")
        else:
            win.addstr(int(win.getmaxyx()[0]/2) - 3, int(win.getmaxyx()[1]/2)-7, "  W - Forward  ", C.A_DIM)
            done = False

        if(PRESSED['S']):
            win.addstr(int(win.getmaxyx()[0]/2) - 1, int(win.getmaxyx()[1]/2)-7, "  S - Backward ")
        else:
            win.addstr(int(win.getmaxyx()[0]/2) - 1, int(win.getmaxyx()[1]/2)-7, "  S - Backward ", C.A_DIM)
            done = False

        if(PRESSED['A']):
            win.addstr(int(win.getmaxyx()[0]/2) + 1, int(win.getmaxyx()[1]/2)-7, "  A - Rotate Left")
        else:
            win.addstr(int(win.getmaxyx()[0]/2) + 1, int(win.getmaxyx()[1]/2)-7, "  A - Rotate Left", C.A_DIM)
            done = False

        if(PRESSED['D']):
            win.addstr(int(win.getmaxyx()[0]/2) + 3, int(win.getmaxyx()[1]/2)-7, "  D - Rotate Right")
        else:
            win.addstr(int(win.getmaxyx()[0]/2) + 3, int(win.getmaxyx()[1]/2)-7, "  D - Rotate Right", C.A_DIM)
            done = False

        if(PRESSED['P']):
            win.addstr(int(win.getmaxyx()[0]/2) + 5, int(win.getmaxyx()[1]/2)-7, "  P - Exit to Menu")
        else:
            win.addstr(int(win.getmaxyx()[0]/2) + 5, int(win.getmaxyx()[1]/2)-7, "  P - Exit to Menu", C.A_DIM)
            done = False

        if(done):
            return False
        else:
            return True

def mainProgram():
    win = C.initscr()

    # 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    #color pairs (curses use of color)
    C.start_color()
    C.use_default_colors()
    C.init_pair(WC['W'], C.COLOR_WHITE, -1)
    C.init_pair(WC['W']+1, C.COLOR_WHITE, C.COLOR_WHITE)

    C.init_pair(WC['R'], C.COLOR_RED, -1)
    C.init_pair(WC['R']+1, C.COLOR_RED, C.COLOR_RED)

    C.init_pair(WC['G'], C.COLOR_GREEN, -1)
    C.init_pair(WC['G']+1, C.COLOR_GREEN, C.COLOR_GREEN)

    C.init_pair(WC['B'], C.COLOR_BLUE, -1)
    C.init_pair(WC['B']+1, C.COLOR_BLUE, C.COLOR_BLUE)

    C.init_pair(WC['M'], C.COLOR_MAGENTA, -1)
    C.init_pair(WC['M']+1, C.COLOR_MAGENTA, C.COLOR_MAGENTA)

    C.init_pair(WC['Y'], C.COLOR_YELLOW, -1)
    C.init_pair(WC['Y']+1, C.COLOR_YELLOW, C.COLOR_YELLOW)

    # curses options
    C.noecho()
    C.cbreak()
    C.curs_set(0)

    win.clear()
    win.refresh()

    #APP LOOP
    while True:
        out = menuPhase(win)
        
        if(out == "game"):
            gamePhase(win)
        elif(out == "exit"):
            break


#PYGLET used for splashscreen
pWindow = pyglet.window.Window(1280,720, "SUMMER 2019", resizable = False)

#splashscreen tick
def tick(t):

    pass

#SPLASHSCREEN
c = 0.0
gradUp=True
keyEnd = False
@pWindow.event
def on_draw():
    global c
    global gradUp

    #pWindow.set_location(0,0)
    img = pyglet.image.load("data/summer2019_en.jpg")
    tex = img.get_texture()

    if(gradUp and c <= 1.0):
        c+=0.01
        if(keyEnd):
            c+=0.05
        if(c >= 1):
            gradUp = False
    elif(gradUp == False and c > 0):
        c-=0.05
        if(keyEnd):
            c-=0.05
    elif(gradUp == False and c <= 0):
        pyglet.app.exit()

    glColor3f(c,c,c)
    tex.blit(0,0)

#SKIP option
@pWindow.event
def on_key_press(key, mod):
    global keyEnd
    if(key == pyglet.window.key.ESCAPE):
        keyEnd = True
        return pyglet.event.EVENT_HANDLED

    keyEnd = True

#pyglet
pyglet.clock.schedule_interval(tick, 1/30)
pyglet.app.run()
pWindow.close()

#main
mainProgram()
