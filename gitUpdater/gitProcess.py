#!/usr/bin/env python3

import os
allPath = os.popen("ls").read().split("\n")

dirs = [x for x in allPath if os.path.isdir(x)]

for i in dirs:
    #os.system("git -C {}/ status".format(i))

    if(".git" in os.popen("ls {}/ -a".format(i)).read().split("\n")):
        print("Directory {}".format(i))
        print(30*"-")
        os.system("git -C {}/ status".format(i))
        print()
        os.system("git -C {}/ pull".format(i))
        print()
