#!/usr/bin/env python3

import curses as C
import random as R

def anim():
    win = C.initscr()
    
    C.noecho()
    C.cbreak()
    
    while True:
        win.clear()

        key = win.getch()

        win.addstr(10,R.randint(10,20), str(key))

        win.refresh()


anim()
