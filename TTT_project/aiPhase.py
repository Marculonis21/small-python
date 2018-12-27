#!/usr/bin/env python3

import numpy as np
import random as r
import time


def nonlin(x, deriv=False):
    if(deriv):
        return(x*(1-x))

    return 1/(1+np.exp(-x))


def netTraining(inp=[], playSide=-1, LR=0.5):
    global w1
    global w2
    global WINNABLE

    # Změna board pro síť
    if(playSide == 0):
        _input = inp.copy()
    else:
        lam = lambda x: 0.5 if x == 0.5 else (1 if x == 0 else 0)
        _input = list(map(lam, inp))

    # NET - WORK
    l1 = np.array([_input])
    l2 = nonlin(np.dot(l1, w1))
    l3 = nonlin(np.dot(l2, w2))

    # Kde už je pole obsazené síť nemůže nic vložit
    for i in range(9):
        if not (_input[i] == 0.5):
            l3[0][i] = 0

    # Změna na string pro kontrolu s FILE
    if(playSide == 0):
        test = ""
        for i in range(len(_input)):
            if(_input[i] == 0.5):
                test += "."
            elif(_input[i] == 1):
                test += "X"
            else:
                test += "O"
    else:
        test = ""
        for i in range(len(_input)):
            if(_input[i] == 0.5):
                test += "."
            elif(_input[i] == 1):
                test += "O"
            else:
                test += "X"

    wantedOut = [0 for i in range(9)]


    if(test == "........."):
        wantedOut[5] = 1
    else:
        # Kontrola s FILE ##### Změna #### Nechat najít FILE se stejným
        # stringem, a zjistit, která cesta je nekratší k WIN
        # -> pak hrát podle ní

        start = time.time()

        if(WINNABLE):
            recordLength = 10
            recordList = []
            for line in lines:
                if not (line.find(test) == -1):
                    if (playSide == 0):
                        if not (lines[lines.index(line) - 1].find("Crosses") == -1):
                            s = line.split("|")
                            s.pop()
                            if (len(s) < recordLength):
                                recordLength = len(s)
                                recordList = s.copy()

                                if (len(s) == 6):
                                    break

                    else:
                        if not (lines[lines.index(line) - 1].find("Noughts") == -1):
                            s = line.split("|")
                            s.pop()
                            if (len(s) < recordLength):
                                recordLength = len(s)
                                recordList = s.copy()

                                if (len(s) == 5):
                                    break

            if (recordList == []):

                for line in lines:
                    if not (line.find(test) == -1):
                        if (playSide == 0):
                            if not (lines[lines.index(line) - 1].find("Draw") == -1):
                                s = line.split("|")
                                s.pop()
                                recordLength = len(s)
                                recordList = s.copy()

                        else:
                            if not (lines[lines.index(line) - 1].find("Draw") == -1):
                                s = line.split("|")
                                s.pop()
                                recordLength = len(s)
                                recordList = s.copy()

            #print(recordList)

            try:
                rL = recordList[recordList.index(test)+1]
                tL = list(test)
                for i in range(len(tL)):
                    if not (tL[i] == rL[i]):
                        wantedOut[i] = 1
            except ValueError:
                WINNABLE = False

        if not (WINNABLE):
            print("CANNOT WIN")

        end = time.time()

        print("Was working for {:.3f} seconds".format(end - start))

    if(WINNABLE):
        for i in range(100):
            l3_error = wantedOut - l3
            l3_delta = l3_error*nonlin(l3, deriv=True)
            l2_error = l3_delta.dot(w2.T)
            l2_delta = l2_error*nonlin(l2, deriv=True)
            l1_error = l2_delta.dot(w1.T)

            w2 += l2.T.dot(l3_delta) * LR
            w1 += l1.T.dot(l2_delta) * LR

        global gameBoard

        if (playSide == 0):
            gameBoard[wantedOut.index(1)] = 1
        else:
            gameBoard[wantedOut.index(1)] = 0

    else:
        randomPlay(inp, playSide)

def printBoard(gm=[]):
    for y in range(3):
        print("\n--------")
        for x in range(3):
            if(gm[x+(y*3)] == 0.5):
                print("| ", end="")
            elif(gm[x+(y*3)] == 1):
                print("|X", end="")
            elif(gm[x+(y*3)] == 0):
                print("|O", end="")

        print("|", end="")
    print("\n--------")


def checkBoard(gm=[], pOutput=False):
    playable = True
    if(gm.count(0.5) == 0):
        playable = False

        if(pOutput):
            print("DRAW")
    else:
        for i in range(3):
            if(gm[i] == gm[i+3] == gm[i+6]) and (gm[i] != 0.5):
                playable = False

        for w in range(3):
            testY = 0
            testY += 3*w
            if(gm[testY] == gm[testY+1] == gm[testY+2]) and (gm[testY] != 0.5):
                playable = False

        if(gm[0] == gm[4] == gm[8]) and (gm[0] != 0.5):
            playable = False
        if(gm[2] == gm[4] == gm[6]) and (gm[2] != 0.5):
            playable = False

    if(pOutput):
        if not (playable):
            global TURN

            if(TURN):
                print("PC WON")

            else:
                print("PLAYER WON")

    return playable


def randomPlay(gm=[], STARTING=-1):
    global gameBoard
    global TURN

    while True:
        pos = r.randint(0, 8)

        if(gm[pos] != 0.5):
            pass
        else:
            if(STARTING == 0):
                gm[pos] = 0
            else:
                gm[pos] = 1
            break

    gameBoard = gm


def netPlay(gm=[], playSide=-1):
    global w1
    global w2

    start = time.time()

    # Změna board pro síť
    if(playSide == 0):
        _input = gm.copy()
    else:
        lam = lambda x: 0.5 if x == 0.5 else (1 if x == 0 else 0)
        _input = list(map(lam, gm))

    # NET - WORK
    l1 = np.array([_input])
    l2 = nonlin(np.dot(l1, w1))
    l3 = nonlin(np.dot(l2, w2))

    # Kde už je pole obsazené síť nemůže nic vložit
    for i in range(9):
        if not (_input[i] == 0.5):
            l3[0][i] = 0

    end = time.time()
    print("Was working for {:3f}".format(start-end))

    global gameBoard

    if(playSide == 0):
        gameBoard[np.argmax(l3)] = 1
    else:
        gameBoard[np.argmax(l3)] = 0


def playerPlay(gm=[], playSide=-1):
    while True:
        try:
            _input = int(input("Zadejte polohu 1-9: "))

            if not (_input > 9 and _input < 1):
                if(gm[_input-1] == 0.5):
                    break
                else:
                    print("INVALID INPUT!")
            else:
                print("INVALID INPUT!")

        except ValueError:
            print("INVALID INPUT!")

    pos = _input - 1

    global gameBoard

    if(playSide == 0):
        gameBoard[pos] = 0
    else:
        gameBoard[pos] = 1


#file = open("TTT_games.txt","r")
file = open("//home//marculonis//Desktop//TTT_games.txt")
lines = file.readlines()
file.close()

try:
    w1 = np.load("w1File.npy")
    w2 = np.load("w2File.npy")

    print("Save files found - Weights loaded from files")
except FileNotFoundError:
    w1 = 2*np.random.random([9, 36]) - 1
    w2 = 2*np.random.random([36, 9]) - 1

    print("No save files found - Weights initialized")


# Work cycle
while True:
    while True:
        try:
            dec = int(input("\nTrain network ---> 1\nPlay TTT --------> 2\n"))
            break
        except ValueError:
            print("INVALID INPUT!")

    #
    #   AI VS RANDOM TIME
    #
    if(dec == 1):
        endTime = int(input("Wanted training time (s): "))

        STARTING = 0  # Starting = 0 = Human/Random first ### Starting = 1 = AI first

        iteration = 0
        startTime = time.time()

        # Training time
        while time.time() - startTime <= endTime:
            iteration += 1
            print("Loop {}------------------------------".format(str(iteration)))

            # New game board
            gameBoard = [0.5 for i in range(9)]
            WINNABLE = True

            # Pokud je STARTING 0 začíná random/player /// else začíná AI
            if(STARTING == 0):
                TURN = True
            else:
                TURN = False

            # GAME LOOP
            while True:
                printBoard(gameBoard)

                # check board playability
                if not (checkBoard(gameBoard)):
                    break

                print("##Playing: {}".format(TURN))


                if(TURN):
                    randomPlay(gameBoard, STARTING)
                    TURN = False

                else:  # learning
                    netTraining(gameBoard, STARTING, 1)
                    TURN = True
                    pass


            # Hra skončí -> změní se pořadí hry
            if(STARTING == 0):
                STARTING = 1
            else:
                STARTING = 0


            # Ukládání weight files
            np.save("w1File", w1)
            np.save("w2File", w2)

        print("-------- END OF TRAINING --------\nWas training for {:.3f} seconds.".format(time.time() - startTime))


    #
    #   AI VS PLAYER TIME
    #
    elif(dec == 2):
        STARTING = 1  # Starting = 0 = Human/Random first ### Starting = 1 = AI first

        iteration = 0

        # New game board
        gameBoard = [0.5 for i in range(9)]

        # Pokud je STARTING 0 začíná random/player /// else začíná AI
        if(STARTING == 0):
            TURN = True
        else:
            TURN = False

        # GAME LOOP
        while True:
            printBoard(gameBoard)

            # check board playability
            if not (checkBoard(gameBoard, True)):
                break

            # Info print
            if(TURN):
                print("##Playing: PLAYER")
            else:
                print("##Playing: AI")

            # Playing phase
            if(TURN):
                playerPlay(gameBoard, STARTING)
                TURN = False

            else:
                netPlay(gameBoard, STARTING)
                TURN = True
                pass

        # Hra skončí -> změní se pořadí hry
        if(STARTING == 0):
            STARTING = 1
        else:
            STARTING = 0
