#!/usr/bin/env python3

import curses as C
import random as R
import time
import _thread


def anim():
    win = C.initscr()
    
    C.noecho()
    C.cbreak()
    C.curs_set(0)

    win.clear()
    win.refresh()
   
    while True:
        win.clear()

        win.addstr(10,R.randint(10,20), "a")
        key = win.getch()
        win.addstr(5,R.randint(5,10), str(key))

        startT = time.time()
        while time.time() - startT <= 1/60:
            pass

        win.refresh()

anim()
