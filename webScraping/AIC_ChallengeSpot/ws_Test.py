#!/usr/bin/env python3

import urllib.request as req
from bs4 import BeautifulSoup as BS
import os
from tqdm import tqdm

import pyglet
from pyglet.gl import *

path = os.getcwd()

wantedWidth = 250 
imagePaths = []
challengeAttribs = []

imagePick = 0

def webScrapeImages():
    global imagePaths, challengeAttribs, winIcon

    page = req.urlopen("https://www.aicrowd.com/challenges")
    soup = BS(page, 'html.parser')
    challengeList = soup.find_all(class_='card card-challenge')

    os.system("rm "+path+"/data/*")

    for i in tqdm(range(len(challengeList))):
        imgClass = challengeList[i].find(class_='card-img')
        pathX = imgClass['src']
        
        attribs = {} 

        altPath = challengeList[i].find(class_='badge badge-primary')
        if(altPath == None):
            tqdm.write("continue")
            continue

        timeAttrib = altPath.text
        attribs['time'] = timeAttrib.strip()

        bodyPath = challengeList[i].find(class_='card-body')
        nameAttrib = bodyPath.find(class_="card-title").text
        attribs['name'] = nameAttrib.strip()

        mainText = bodyPath.find(class_="card-text").text
        attribs['text'] = mainText.strip()

        prizes = bodyPath.find(class_='prizes-breakdown')
        items = prizes.find_all('div')
        prizeList = []
        for single in items:
            prizeList.append(single.text.strip())

        attribs['prizes'] = prizeList

        endBody = challengeList[i].find(class_="card-footer")
        alt = endBody.find_all('a')
        orgName = alt[1].text.strip()
        attribs['org'] = orgName

        tqdm.write(pathX)
        req.urlretrieve(pathX, path + "/data/" + str(pathX.split("/").pop()))

        imagePaths.append("data/"+str(pathX.split("/").pop()))
        challengeAttribs.append(attribs)

###

webScrapeImages()
window = pyglet.window.Window(400,600, "Challenges", resizable = False)

winIcon = "data/icon/icon.png"
ico1 = pyglet.image.load("data/icon/32x32.png")
ico2 = pyglet.image.load("data/icon/16x16.png")
window.set_icon(ico1,ico2)

#glEnable(GL_TEXTURE_2D)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


imageList = []
def loadImages():
    global imageList

    for item in imagePaths:
        img = pyglet.image.load(item)
        tex = img.get_texture()
        actW = tex.width 
        actH = tex.height
        rat = actW/actH

        tex.width = wantedWidth
        tex.height = wantedWidth*rat

        imageList.append(tex)

def drawText(text, x, y, anX='center',anY='center', r=1,g=1,b=1,a=1, size=15, lWidth=300, hAlign="left"):

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

    label.draw()

def drawImage(image, x, y, opacity=1):
    xx = x - image.width/2
    yy = y - image.height/2
    image.blit(xx,yy)
    pass

def drawLine(startX, startY, endX, endY, r=1,g=1,b=1):
    glBegin(GL_LINES)
    glColor3f(r,g,b)
    glVertex2f(int(startX), int(startY))
    glVertex2f(int(endX), int(endY))
    glEnd()

def drawRect(x,y,sizeX,sizeY, r=1,g=1,b=1):
    
    x -= sizeX/2
    y -= sizeY/2

    glBegin(GL_QUADS)
    glColor3f(r,g,b)
    glVertex2f(int(x), int(y))
    glVertex2f(int(x+sizeX), int(y))
    glVertex2f(int(x+sizeX), int(y+sizeY))
    glVertex2f(int(x), int(y+sizeY))
    glEnd()
    glColor3f(1,1,1)

def allTextDraw(imagePick = -1):
    drawText(challengeAttribs[imagePick]['name'],
            x = window.width/2,
            y = window.height/2-5,
            anX = 'center',
            anY = 'center',
            size = 15,
            r=1,g=1,b=1,
            lWidth = 350,
            hAlign = "center")

    drawText(challengeAttribs[imagePick]['time'],
            x = 20,
            y = window.height/2-30,
            anX = 'left',
            anY = 'top',
            size = 12,
            r=0.8,g=0.8,b=0.8,
            lWidth = 360,
            hAlign = "left")

    drawText(challengeAttribs[imagePick]['text'],
            x = 20,
            y = window.height/2-60,
            anX = 'left',
            anY = 'top',
            size = 12,
            r=0.8,g=0.8,b=0.8,
            lWidth = 360,
            hAlign = "left")

    prizeLoop = 0
    for item in challengeAttribs[imagePick]['prizes']:
        drawText(item,
                x = 20,
                y = 175-(15*prizeLoop),
                anX = 'left',
                anY = 'top',
                size = 12,
                r=0.8,g=0.8,b=0.8,
                lWidth = 360,
                hAlign = "left")
        prizeLoop+=1

    drawText("By " + challengeAttribs[imagePick]['org'],
            x = 20,
            y = 80,
            anX = 'left',
            anY = 'top',
            size = 12,
            r=0.8,g=0.8,b=0.8,
            lWidth = 360,
            hAlign = "left")

def tick(t):

    pass

@window.event
def on_draw():
    glClearColor(0.3,0.3,0.3,1)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    drawImage(imageList[imagePick], window.width/2,(3/4)*window.height)

    #TEXT
    allTextDraw(imagePick)

    #SELECT
    chNum = len(imageList)
    pad = 25
    for i in range(chNum):

        x = window.width/2 - (pad*(chNum/2)) + (pad*i)
        c = 0.2
        s = 10

        if(i == imagePick):
            c = 0.5
            s = 15

        drawRect(x,15,s,s,c,c,c)
    
@window.event
def on_key_press(symbol,mod):
    global imageList,imagePick
    
    if(symbol == pyglet.window.key.LEFT):
        if(imagePick == 0):
            imagePick = len(imageList)-1
        else:
            imagePick -= 1
    
    if(symbol == pyglet.window.key.RIGHT):
        if(imagePick == len(imageList)-1):
            imagePick = 0
        else:
            imagePick += 1



loadImages()

pyglet.clock.schedule_interval(tick, 1/60)
pyglet.app.run()
