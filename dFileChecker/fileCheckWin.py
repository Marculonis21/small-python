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
                b = bytes(x.encode("iso8859-2"))
                print(b)
                files.append(x)

    for x in files:
        if(os.path.isdir("{}\{}".format(dir, x))):
            dirs.append("{}\{}".format(dir, x))
        else:
            fileMem.append("{}\{}".format(dir, x))

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)if unicodedata.category(c) != 'Mn')

logging.basicConfig(filename=("duplicatesLog.txt"), level=logging.DEBUG, format="Found duplicate: %(message)s")

fileMem = []

allP = os.popen("dir").read().split("\n")
allPath = []
for i in allP:
    xxx = i.split(" ")
    if(xxx[0] != ""):
        x = i.split(" ").pop()
        if(x != "." and x != ".."):
            allPath.append(x)
    
dirs = [x for x in allPath if os.path.isdir(x)]

for item in dirs:
    fSMethod(item)
quit()
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
