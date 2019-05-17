#!/usr/bin/env python3

import turtle as t

class TGraph:

    def __init__(self,width=800,height=400,scaleX=10,scaleY=100,color="black"):
        self.width = width
        self.height = height
        t.setup(width,height)
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.color = color
        self.zeroPosX = None
        self.zeroPosY = None

        self.pointSpread = (self.width - 150) / scaleX

    def windowSize(self, width, height):
        if(width == None or height == None):
            pass
        else:
            self.width = width
            self.height = height
            t.screensize(width,height)
            t.update()

        return (self.width,self.height)

    def graphScale(self, scaleX, scaleY):
        if(scaleX == None or scaleY == None):
            pass
        else:
            self.scaleX = scaleX
            self.scaleY = scaleY
            self.pointSpread = (self.width - 150) / scaleX

        return (self.scaleX,self.scaleY)

    def startPrint(self):
        t.home()
        t.hideturtle()
        t.color(self.color)
        t.up()
        t.setx(self.width/2 - 50)
        t.sety(-self.height/2 + 50)
        t.down()
        #t.setx(-self.width/2 + 50)
        t.left(180)
        for i in range(self.scaleX):
            t.forward(self.pointSpread)
            t.dot(5)

        t.sety(self.height/2 - 50)

if __name__ == "__main__":
    tg = TGraph()
    tg.startPrint()
    input()
