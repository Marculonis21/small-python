#!/usr/bin/env python3

import os
import logging

def fSMethod(dir):
    global fileMem
    global dirs

    files = os.popen("ls {}/".format(dir)).read().split("\n")
    files.pop()

    for x in files:
        if(os.path.isdir("{}/{}".format(dir, x))):
            dirs.append("{}/{}".format(dir, x))
        else:
            fileMem.append("{}/{}".format(dir, x))

log_dir = ""
logging.basicConfig(filename=(log_dir+"duplicatesLog.txt"), level=logging.DEBUG, format="Found duplicate: %(message)s")

fileMem = []

allPath = os.popen("ls").read().split("\n")

dirs = [x for x in allPath if os.path.isdir(x)]

for item in dirs:
    fSMethod(item)

fDir = {}
for f in fileMem:
    x = f.split("/").pop()

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
