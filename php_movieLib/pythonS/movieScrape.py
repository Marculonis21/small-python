#!/usr/bin/env python3

import urllib
import urllib.request as req
from bs4 import BeautifulSoup as BS

import sys


def webScrape(actName, maxList, on_page):
    A = []
    xxx = list(actName)
    for i in range(len(xxx)):
        if(xxx[i] == ' '):
            xxx[i] = '+'
        else:
            #FOR CZECH CHARACTERS!!!
            xxx[i] = urllib.parse.quote(xxx[i])

    _name = ''.join(xxx)

    #https://www.imdb.com/find?q={}&s=tt&ttype=ft

    '''
    PARSING CZECH TO URL
    #TEST

    unurl = "http://example.com/unicode?q=áač"
    print(unurl)

    parts = urllib.parse.urlsplit(unurl)
    lparts = list(parts)

    lparts[3] = urllib.parse.quote(lparts[3])
    unurl = urllib.parse.urlunsplit(lparts)
    print(unurl)
    
    quit()
    '''

    #1PAGE
    page = req.urlopen("https://www.imdb.com/find?q={}&s=tt&ttype=ft".format(_name))
    soup = BS(page, 'html.parser')

    foundAll = soup.find_all('tr')

    _range = len(foundAll)
    for item in reversed(range(_range)):
        testIMG = foundAll[item].find("img")["src"]
        #print(testIMG)
        if("nopicture" in testIMG):
            foundAll.remove(foundAll[item])

            #print("Found")


    #print(len(foundAll))
    if(len(foundAll) < maxList*on_page):
        end = len(foundAll)
    else:
        end = maxList * on_page

    startingP = maxList * (on_page-1)

    scrapeLog = ""
    scrapeLog += ";{};{};|".format(len(foundAll), (len(foundAll) >= maxList*on_page))
    for single in range(startingP, end):
        main = foundAll[single]
        
        n = main.find(class_='result_text')
        name = n.find('a').contents[0]
        aka = n.find('i')
        try:
            aka = aka.contents[0][1:-1]
        except:
            aka = ""
            pass

        #findResults
        final = main.find("a")["href"]
        
        page = req.urlopen("https://www.imdb.com/{}".format(final))
        soup = BS(page, 'html.parser')

        score = "None"
        try:
            _score = soup.find(class_='ratingValue')
            score = _score.find("span").contents[0]
        except:
            pass

        info = "None"
        try:
            _info = soup.find(class_='summary_text')

            if(len(_info) > 1):
                info = "{} {} {}".format(_info.contents[0].strip(), _info.find('a').contents[0], _info.contents[2].strip())
            else:
                info = _info.contents[0].strip()

            if("Add a Plot" in info):
                info = "No info"
        except: 
            pass

        img = ""
        try:
            poster = soup.find(class_='poster')
            img_p = poster.find("a")["href"]
            page = req.urlopen("https://www.imdb.com{}".format(img_p))
            soup = BS(page, 'html.parser')
            img = soup.find('meta',itemprop="image")['content']
        except:
            pass

        scrapeLog += ("{};{};{};{};{};|".format(name,aka,img,info,score))

    return scrapeLog

arg = sys.argv

if(arg[1] == '-M'):
    movie = arg[4]
    sL = webScrape(movie, int(arg[2]), int(arg[3]))
    #print("ěščřžýáíé".encode('utf-8'))
    print(sL.encode('utf-8'))

#print("TESTTESTTEST")
