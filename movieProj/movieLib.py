#!/usr/bin/env python3

import os 
import sys
import tqdm

import urllib.request as req
from bs4 import BeautifulSoup as BS

path = os.curdir
if(len(sys.argv) > 1):
    path = sys.argv[1]

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

def webScrape(_name):
    name = _name.split(';')
    name.pop()

    xxx = list(name[0])
    for i in range(len(xxx)):
        if(xxx[i] == ' '):
            xxx[i] = '+'

    _name = ''.join(xxx)

    page = req.urlopen("https://www.imdb.com/find?q={}".format(_name))
    soup = BS(page, 'html.parser')

    fFind = soup.find(class_='findResult odd')
    fSite = fFind.find("a")["href"]

    page = req.urlopen("https://www.imdb.com/{}".format(fSite))
    soup = BS(page, 'html.parser')

    poster = soup.find(class_='poster')
    img = poster.find("img")["src"]

    req.urlretrieve(img, "data/pic_"+name[0])

_files = findFiles(path, ["mkv","avi","mp4"], False)
files = _files.split('\n')
files.sort()
nFiles =[x.split('/').pop() for x in files]
nFiles.remove(nFiles[0])

#for i in nFiles:
#    print(i)

for i in tqdm.tqdm(range(len(nFiles))):
    webScrape(nFiles[i])
#https://www.imdb.com/find?q=a+a

