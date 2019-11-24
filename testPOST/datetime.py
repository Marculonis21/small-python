#!/usr/bin/env python3

import time
import calendar

local = time.localtime()
print("Dnes je {}. {}. {}.".format(local[2], local[1], local[0]))

print(time.asctime(local))
print("Datum a čas: {} ".format(time.asctime(local))) 

print("start")
time.sleep(3)
print("konec")
