#!/usr/bin/env python3

import threading
import time
import queue

def thread_function(num,xxx,q):
    while True:
        num = num + 5
        q.put(num)

        xxx = xxx + 5
        q.put(xxx)
        

q = queue.Queue()
num = 0
xxx = -100
x = threading.Thread(target=thread_function, args=(num,xxx,q))
print("#####################################xstart")
print(str(x.is_alive()))
x.start()
print(str(x.is_alive()))
quit()

while True:
    num = q.get()
    xxx = q.get()
    print(num)
    print(xxx)
