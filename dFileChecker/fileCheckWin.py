#!/usr/bin/env python3

#''.join(c for c in unicodedata.normalize('NFD', "notykrávo")if unicodedata.category(c) != 'Mn')
import os
import logging
import unicodedata

def fSMethod(dir):
    global fileMem
    global dirs

    _files = os.popen("dir {}".format(dir)).read().split("\n")
    files = []
    for i in _files:
        xxx = i.split(" ")
        if(xxx[0] != ""):
            x = i.split(" ").pop()
            if(x != "." and x != ".."):
                s = czWin_Trans(x)
                files.append(s)

    for x in files:
        if(os.path.isdir("{}\{}".format(dir, x))):
            dirs.append("{}\{}".format(dir, x))
        else:
            fileMem.append("{}\{}".format(dir, x))

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)if unicodedata.category(c) != 'Mn')

def czWin_Trans(x):
    b = list(bytes(x.encode("cp1250")))
    for i in range(len(b)):
        if("\\xd8" in b[i]):
            b[i] = "ě"
        if("\\xe7" in b[i]):
            b[i] = "š"
        if("\\x9f" in b[i]):
            b[i] = "č"
        if("\\xfd" in b[i]):
            b[i] = "ř"
        if("\\xa7" in b[i]):
            b[i] = "ž"
        if("\\xec" in b[i]):
            b[i] = "ý"
        if("\\xa0" in b[i]):
            b[i] = "á"
        if("\\xal" in b[i]):
            b[i] = "í"
        if("\\x82" in b[i]):
            b[i] = "é"

    s = "".join(x for x in b)
    return s
    

logging.basicConfig(filename=("duplicatesLog.txt"), level=logging.DEBUG, format="Found duplicate: %(message)s")

fileMem = []

allP = os.popen("dir").read().split("\n")
allPath = []
for i in allP:
    xxx = i.split(" ")
    if(xxx[0] != ""):
        x = i.split(" ").pop()
        if(x != "." and x != ".."):
            s = czWin_Trans(x)
            allPath.append(s)
    
dirs = [x for x in allPath if os.path.isdir(x)]

for item in dirs:
    fSMethod(item)

fDir = {}
loop = 0
for f in fileMem:
    loop += 1;
    x = f.split("\\").pop()
    
    if not (x in fDir):
        fDir[x] = []

    fDir[x].append(f)

for item in fDir:
    log = ""
    if(len(fDir[item]) > 1):
        print("Found duplicates:")
        for x in fDir[item]:
            log += "{}; ".format(x)
            print(x, end = "; ")

        print()

        logging.info(log)
