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
    xxx = list(x)
    b = [i.encode("cp1250") for i in xxx]
    
    for i in range(len(b)):
        if(b"\xd8" == b[i]):
            xxx[i] = "ě"
        if(b"\xe7" == b[i]):
            xxx[i] = "š"
        if(b"\x9f" == b[i]):
            xxx[i] = "č"
        if(b"\xfd" == b[i]):
            xxx[i] = "ř"
        if(b"\xa7" == b[i]):
            xxx[i] = "ž"
        if(b"\xec" == b[i]):
            xxx[i] = "ý"
        if(b"\xa0" == b[i]):
            xxx[i] = "á"
        if(b"\xa1" == b[i]):
            xxx[i] = "í"
        if(b"\x82" == b[i]):
            xxx[i] = "é"
                
    s = "".join(x for x in xxx)
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
