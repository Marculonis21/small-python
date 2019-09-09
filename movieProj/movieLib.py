#!/usr/bin/env python3

import os 
import sys
import tqdm

import urllib.request as req
from bs4 import BeautifulSoup as BS

import pyglet
from pyglet.gl import *

window = pyglet.window.Window(800,800, "Movies", resizable = True)

#path = os.curdir
path = "/media/marculonis/""My Passport""/""Filmy"""
if(len(sys.argv) > 1):
    path = sys.argv[1]

dataFiles = os.listdir("data/")
fileNames = [x.rsplit('_',1)[0] for x in dataFiles]

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

imageList = {}
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

    #ALPHABET SORT
    imageList = dict(sorted(imageList.keys()))

    #SCORE SORT
    #imageList = dict(sorted(imageList.items(), key = lambda x: x[0].split('_')[1]))

def webScrape(_name):
    #tqdm.tqdm.write(_name)
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
for i in imageList:
    print(i)

quit()

pyglet.app.run()
