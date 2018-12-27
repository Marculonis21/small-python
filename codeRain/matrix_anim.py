import curses as C
import random as R
import string
import time

# class for columns instances
class lString:
    def __init__(self, window, strLen, hltime, lifetime):
        self.strLen = strLen
        self.lifetime = lifetime
        self.LTtick = -1
        self.hltime = hltime

        self.sPosX = R.randint(0, window.getmaxyx()[1])
        self.sPosY = R.randint(0,window.getmaxyx()[0] - strLen)

        self.LIFESPAN = 0

        self.group = [R.choice(lPool) for i in range(strLen)]
        self.stage = "0"
        # 0,1,2,3
        # 0 - start
        # 1 - classic stay
        # 2 - higlight over
        self.lastHLtick = -1
        # 3 - end
        # 4 - dead

        self.lState =  [-1 for i in range(strLen)]
        # -1,0,1,2,3
        # -1 - invisible
        # 0 - dimmed
        # 1 - lowered
        # 2 - normal plus
        # 3+2 - higligted - bold
        # 3+1 - higligted - blink

    def tick(self):
        self.LIFESPAN += 1

        for l in range(len(self.group)):
            if(R.random() < 0.2):
                self.group[l] = R.choice(lPool)

        #STARTING PHASE
        if("0" in self.stage):
            if(self.lState.count(-1) > 0):
                for i in range(len(self.lState)):
                    if(self.lState[i] == -1):
                        self.lState[i] = 32

                        if(i > 0):
                            self.lState[i-1] = 31
                        if(i > 1):
                            self.lState[i-2] = R.choice([1,2])

                        break

            elif(self.lState[len(self.lState)-1] == 32):
                self.lState[len(self.lState)-1] = 31
                self.lState[len(self.lState)-2] = R.choice([1,2])

            elif(self.lState[len(self.lState)-1] == 31):
                self.lState[len(self.lState)-1] = R.choice([1,2])
                self.stage = "1"

        #NORMAL RUNNING PHASE
        if("1" in self.stage):
            if(self.LIFESPAN > self.hltime and not "3" in self.stage):
                self.stage += "2"

            if(self.LIFESPAN > self.lifetime):
                self.stage += "3"

        #HIGHLIGHT OVER PHASE
        if("2" in self.stage):
            self.lastHLtick += 1

            if(self.lastHLtick < len(self.lState)):
                self.lState[self.lastHLtick] = 32

                if(self.lastHLtick > 0):
                    self.lState[self.lastHLtick - 1] = 31
                if(self.lastHLtick > 1):
                    self.lState[self.lastHLtick - 2] = R.choice([1,2])

            else:
                if(self.lState[len(self.lState)-1] == 32):
                    self.lState[len(self.lState)-1] = 31
                    self.lState[len(self.lState)-2] = R.choice([1,2])

                elif(self.lState[len(self.lState)-1] == 31):
                    self.lState[len(self.lState)-1] = R.choice([1,2])

                    self.stage = "1"
                    self.hltime *= 2
                    self.lastHLtick = -1

        #END PHASE
        if("3" in self.stage):
            self.LTtick += 1

            if(self.LTtick < len(self.lState)):
                self.lState[self.LTtick] = 0

                if(self.LTtick > 0):
                    self.lState[self.LTtick-1] = -1

            else:
                if(self.lState[len(self.lState)-1] == 0):
                    self.lState[len(self.lState)-1] = -1
                    self.stage = "4"


#string.printable
lPool = list(string.printable[:94])

def animation_play():
    # new window
    win = C.initscr()

    C.start_color()
    C.use_default_colors()

    # color pairs
    C.init_pair(1, C.COLOR_GREEN, -1)
    C.init_pair(2, C.COLOR_WHITE, -1)

    # hiding typing and cursor
    C.noecho()
    C.curs_set(0)

    win.clear()
    win.refresh()

    ### class(self, window, strlen, highlightTime, lifetime)
    #s1 = lString(win, R.randint(15,25), R.randint(5,10))
    #sCol = [lString(win, R.randint(5,30), R.randint(35,80), R.randint(30, 150)) for i in range(40)]

    # list of char columns instances
    sCol = []

    spawnTime = 0
    spawnCD = 1
    try:
        # animation loop
        while True:
            spawnTime += 1

            win.clear()

            #win.addstr(0,0,str(spawnTime))
            #win.addstr(1,0,str(spawnCD))

            # spawn rate counter
            if(spawnTime > spawnCD):
                spawnCD += R.randint(5,10)
                for i in range(R.randint(1,5)):
                    # instance spawning
                    sCol.append(lString(win, R.randint(5,win.getmaxyx()[0]-(win.getmaxyx()[0]/3)), R.randint(35,80), R.randint(30, 150)))

            # all tick loop
            for item in sCol:
                item.tick()

                # win.addstr(sCol.index(item)+1,0,str(item.lifetime) + ", " + str(item.hltime) + ", " + str(item.LIFESPAN) + ", " + str(item.stage))

                # setting up cursor
                y = item.sPosY
                x = item.sPosX

                # writing loop + all the different states
                # THE POWER OF THE DUCK
                pos = -1
                for l in item.lState:
                    pos += 1
                    try:
                        if(l == 2):
                            win.addstr(y+pos, x, item.group[pos], C.color_pair(1) + C.A_BOLD)
                        elif(l == 1):
                            win.addstr(y+pos, x, item.group[pos], C.color_pair(1))
                        elif(l == 32):
                            win.addstr(y+pos, x, item.group[pos], C.color_pair(2) + C.A_BOLD)
                        elif(l == 31):
                            win.addstr(y+pos, x, item.group[pos], C.color_pair(2))
                        elif(l == 0):
                            win.addstr(y+pos, x, item.group[pos], C.color_pair(1) + C.A_DIM)
                    except:
                        pass

            #win.addstr(y+1,x,"".join(xxx), C.color_pair(1) + C.A_BOLD)
            #win.addstr(y+3,x,"".join(xxx), C.color_pair(1) + C.A_DIM)

            # loop for dead instance removal
            for item in sCol:
                if(item.stage == "4"):
                    sCol.remove(item)

            # delta time / animation speed
            sTime = time.time()
            while(time.time() - sTime < 0.075):
                pass

            win.refresh()

    # escape sequence
    except KeyboardInterrupt:
        pass
    C.endwin()

# ---------------------------------------------
animation_play()
