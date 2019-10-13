#!/usr/bin/env python3

import os 
import sys
import tqdm

import urllib.request as req
from bs4 import BeautifulSoup as BS

import pyglet
from pyglet.gl import *

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window(800,800, "Movies", resizable = True)
scrollY = 0

mouseX = -1
mouseY = -1

path = "/media/marculonis/""My Passport""/""Filmy"""
#path = "./testData"
if(len(sys.argv) > 1):
    path = sys.argv[1]

dataFiles = os.listdir("data/")
fileNames = [x.rsplit('_',1)[0] for x in dataFiles]
imageList = {}

def webScrape(_name):
    #tqdm.tqdm.write(_name)
    print(_name)
    name = _name.split(';')
    name.pop()
    sName = name[0]

    #fff = list(sName)
    #for i in range(5): fff.pop()
    #sName = ''.join(fff)

    if('pic_'+sName in fileNames):
       return

    s = sName[:len(sName)-4] + "(" + sName[len(sName)-4:] + ")"

    xxx = list(s)
    for i in range(len(xxx)):
        if(xxx[i] == ' '):
            xxx[i] = '+'

    _name = ''.join(xxx)

    #https://www.imdb.com/find?q={}&s=tt&ttype=ft

    #1PAGE
    page = req.urlopen("https://www.imdb.com/find?q={}&s=tt&ttype=ft".format(_name))
    soup = BS(page, 'html.parser')

    #Find right section ("title"/"actor")
    fSection = soup.find_all(class_='findSection')
    sel = 0
    for section in range(len(fSection)):
        checkFind = fSection[section].find(class_='findSectionHeader')
        if(checkFind.find('a')["name"] == "tt"):
            sel = section
            break
        else:
            pass

    #findResults
    fFind = fSection[sel].find(class_='findResult odd')
    final = fFind.find("a")["href"]
    
    page = req.urlopen("https://www.imdb.com/{}".format(final))
    soup = BS(page, 'html.parser')

    poster = soup.find(class_='poster')
    img = poster.find("img")["src"]

    ###SCORE
    _score = soup.find(class_='ratingValue')
    score = _score.find("span").contents[0]

    req.urlretrieve(img, "data/pic_"+sName+"_"+score)


def findFiles(_dir, _ext, expand = True):
    found = ""

    for f in os.listdir(_dir):
        workPath = _dir+"/"+f

        if(expand):
            if(os.path.isdir(workPath)):
                found += findFiles(workPath, _ext)

        if(f.split('.').pop() in _ext):
            found += os.path.abspath(workPath) + "\n"

    return found

def loadImages():
    global imageList

    imagePaths = os.listdir("data/")

    for item in imagePaths:
        img = pyglet.image.load("data/"+item)
        tex = img.get_texture()
        actW = tex.width 
        actH = tex.height
        rat = actW/actH

        imageList[item.split('_', 1)[1]] = tex

    sortImages()

def sortImages(ABCSort = True):
    global imageList

    if(ABCSort):
        #ALPHABET SORT
        imageList = dict(sorted(imageList.items()))
    else:
        #SCORE SORT
        imageList = dict(sorted(imageList.items(), key = lambda x: x[0].split('_')[1]))


def drawImage(image, x, y, c):
    xx = x - image.width/2
    yy = y - image.height/2
    glColor3f(c,c,c)
    image.blit(xx,yy)
    pass

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

def drawText(text, x, y, anX='center',anY='center', r=1,g=1,b=1,a=1, size=15, shadow=False, shadowS=4, lWidth=300, hAlign="left"):
    label = pyglet.text.Label(str(text),
                              font_size=size,
                              anchor_x=anX,
                              anchor_y=anY,
                              align = hAlign,
                              multiline=True,
                              width = lWidth)

    label.x = x
    label.y = y

    label.color = (int(r*255),int(g*255),int(b*255), int(a*255))

    if(shadow):
        _label = pyglet.text.Label(str(text),
                                   font_size=size,
                                   anchor_x=anX,
                                   anchor_y=anY,
                                   align = hAlign,
                                   multiline=True,
                                   width = lWidth)

        _label.x = x+shadowS
        _label.y = y-shadowS

        _label.color = (0,0,0, int(a*255))

        _label.draw()

    label.draw()

def winButton(img, text, x, y, sizeX=0, sizeY=0, hover=False, clicked=False):
    if(sizeX != 0):
        img.width = sizeX
        sizeY = sizeX*1.47
        img.height = sizeY
    elif(sizeY != 0):
        img.height = sizeY
        sizeX = sizeY/1.47
        img.width = sizeX
    else:
        sizeX = img.width
        sizeY = img.height
        print(sizeX)
        print(sizeY)

    if(hover):
        drawImage(img, x, y, 0.5)
    else:
        drawImage(img, x, y, 0.9)

    if(clicked):
        print(img)


    if(text != ""):
        if(hover):
            drawText(text, x+sizeX/2, y-sizeY/2, r=0.8,g=0.8,b=0.8)
        else:
            drawText(text, x+sizeX/2, y-sizeY/2, r=1,g=1,b=1)


def tick(t):

    pass

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouseX, mouseY
    mouseX = x
    mouseY = y
    #print(x,y)

@window.event
def on_draw():
    global scrollY
    glClearColor(0.3,0.3,0.3,1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    drawRect(0, scrollY+window.height, window.width, -75, 0.25,0.25,0.25)
    drawRect(0, scrollY+window.height-75, window.width, -4, 0.1,0.1,0.1)

    drawText("Movies", 20, scrollY + window.height-35, anX='left',anY='center', r=0.9,g=0.9,b=0.9, size=45, shadow=True)

    #drawLine(window.width/5*1,0,window.width/5*1,window.height, 1,0,0)
    #drawLine(window.width/5*2,0,window.width/5*2,window.height, 1,0,0)
    #drawLine(window.width/5*3,0,window.width/5*3,window.height, 1,0,0)
    #drawLine(window.width/5*4,0,window.width/5*4,window.height, 1,0,0)
    #drawLine(window.width/5*5,0,window.width/5*5,window.height, 1,0,0)

    #drawLine(0,window.height/4,window.width,window.height/4, 1,0,0)
    #drawLine(0,window.height/7,window.width,window.height/7, 1,0,0)
    #drawLine(0,window.height/4*3,window.width,window.height/4*3, 1,0,0)
    #drawLine(0,window.height/7*6,window.width,window.height/7*6, 1,0,0)

    if(mouseY<window.height/7):
        scrollY+=7
    elif(mouseY<window.height/4):
        scrollY+=3

    if(mouseY>window.height/7*6):
        if(scrollY >= 7):
            scrollY-= 7
    elif(mouseY>window.height/4*3):
        if(scrollY >= 3):
            scrollY-=3
    print(scrollY)

    #sizeY = sizeX*1.47
    xLoop = 0
    yLoop = 0
    for item in imageList.keys():
        winButton(imageList[item], "", window.width/5*(xLoop+1), scrollY+window.height-200 - (230*yLoop), sizeX=window.width/6)
        xLoop += 1
        if(xLoop > 3):
            xLoop = 0
            yLoop += 1

    #drawImage(imageList[0], window.width/2,window.height/2)

_files = findFiles(path, ["mkv","avi","mp4"], False)

files = _files.split('\n')
files.sort()
nFiles = [x.split('/').pop() for x in files]
nFiles.remove(nFiles[0])

for item in tqdm.tqdm(range(len(nFiles))):
    webScrape(nFiles[item])

loadImages()

pyglet.clock.schedule_interval(tick, 1/60)
pyglet.app.run()
