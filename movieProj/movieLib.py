#!/usr/bin/env python3

import os 
import sys
import tqdm

import urllib.request as req
from bs4 import BeautifulSoup as BS

import pyglet
from pyglet.gl import *

window = pyglet.window.Window(800,800, "Movies", resizable = True)

path = os.curdir
if(len(sys.argv) > 1):
    path = sys.argv[1]

dataFiles = os.listdir("data/")

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

imageList = []
def loadImages():
    global imageList

    imagePaths = os.listdir("data/")

    for item in imagePaths:
        img = pyglet.image.load("data/"+item)
        tex = img.get_texture()
        actW = tex.width 
        actH = tex.height
        rat = actW/actH

        imageList.append(tex)

def webScrape(_name):
    tqdm.tqdm.write(_name)
    name = _name.split(';')
    name.pop()
    sName = name[0]

    fff = list(sName)
    for i in range(5): fff.pop()
    sName = ''.join(fff)

    if('pic_'+sName in dataFiles):
       return

    xxx = list(sName)
    for i in range(len(xxx)):
        if(xxx[i] == ' '):
            xxx[i] = '+'

    _name = ''.join(xxx)

    #1PAGE
    page = req.urlopen("https://www.imdb.com/find?q={}".format(_name))
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
    r1 = fFind.find_all("a")
    result1 = r1[1]
    print(result1)
    quit()

    result2 = None
    try:
        fFind = fSection[sel].find(class_='findResult even')
        result2 = fFind.find("a")["href"]
    except:
        pass

    final = ""
    if(result2 == None):
        final = result1
    else:
        x1 = list(result1)
        x2 = list(result2)

        f = list(sName)

        reward1 = 0
        for i in range(len(x1)):
            try:
                if(x1[i] == f[i]):
                    reward1 += 1
            except:
                pass

        reward2 = 0
        for i in range(len(x2)):
            try:
                if(x2[i] == f[i]):
                    reward2 += 1
            except:
                pass

        print(x1,x2)
        print(f)
        print(reward1,reward2)

    if(reward1 >= reward1):
        final = result1
    else:
        final = result2

    
    page = req.urlopen("https://www.imdb.com/{}".format(final))
    soup = BS(page, 'html.parser')

    poster = soup.find(class_='poster')
    img = poster.find("img")["src"]

    ###SCORE
    _score = soup.find(class_='ratingValue')
    score = _score.find("span")["itemprop"].text
    print(_score)
    print(score)
    quit()

    req.urlretrieve(img, "data/pic_"+sName+"_"+str(score))

def drawImage(image, x, y, opacity=1):
    xx = x - image.width/2
    yy = y - image.height/2
    image.blit(xx,yy)
    pass

def drawText(text, x, y, anX='center',anY='center', r=1,g=1,b=1,a=1, size=15, shadow=False, shadowS=2, lWidth=300, hAlign="left"):
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

def tick(t):

    pass

@window.event
def on_draw():
    glClearColor(0.3,0.3,0.3,1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    drawText("Movies", 20, window.height-20, anX='left',anY='top', size=30, shadow=True)

    drawImage(imageList[0], window.width/2,window.height/2)



_files = findFiles(path, ["mkv","avi","mp4"], False)
files = _files.split('\n')
files.sort()
nFiles = [x.split('/').pop() for x in files]
nFiles.remove(nFiles[0])


for i in tqdm.tqdm(range(len(nFiles))):
    name = nFiles[i]

    webScrape(nFiles[i])
#https://www.imdb.com/find?q=a+a

loadImages()

pyglet.app.run()
