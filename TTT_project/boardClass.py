class BoardClass:

    lines = ""

    def fileReady():
        file = open("TTT_games.txt")
        BoardClass.lines = file.readlines()
        file.close()

    def initBoard():
        return [0.5 for i in range(9)]

    def printBoard(board, real=[]):
        minus = 0

        for y in range(3):
            print("-------")
            print("|", end="")

            for x in range(3):
                if(real != []):

                    if(real[x+(y*3)] != 0.5):
                        print("    X|", end="")
                        minus += 1
                    else:
                        print("{:5.0f}|".format(board[x+(y*3)-minus]), end="")
                else:
                    if(board[x+(y*3)] == 0):
                        print("O|", end="")
                    elif(board[x+(y*3)] == 1):
                        print("X|", end="")
                    else:
                        print(" |", end="")

            print("")
        print("")

    def isComplete(board=[]):
        if(board.count(0.5) == 0):
            return True
        else:
            if(board[0] == board[1] == board[2] != 0.5):
                return True
            elif(board[3] == board[4] == board[5] != 0.5):
                return True
            elif(board[6] == board[7] == board[8] != 0.5):
                return True
            elif(board[0] == board[3] == board[6] != 0.5):
                return True
            elif(board[1] == board[4] == board[7] != 0.5):
                return True
            elif(board[2] == board[5] == board[8] != 0.5):
                return True
            elif(board[0] == board[4] == board[8] != 0.5):
                return True
            elif(board[2] == board[4] == board[6] != 0.5):
                return True
            else:
                return False

    def pWon(board=[]):
        if(board[0] == board[1] == board[2] != 0.5):
            return board[0]
        elif(board[3] == board[4] == board[5] != 0.5):
            return board[3]
        elif(board[6] == board[7] == board[8] != 0.5):
            return board[6]
        elif(board[0] == board[3] == board[6] != 0.5):
            return board[0]
        elif(board[1] == board[4] == board[7] != 0.5):
            return board[1]
        elif(board[2] == board[5] == board[8] != 0.5):
            return board[2]
        elif(board[0] == board[4] == board[8] != 0.5):
            return board[0]
        elif(board[2] == board[4] == board[6] != 0.5):
            return board[2]
        else:
            return -1

    def getMoveOptions(board, player):
        moveMatrix = []

        for i in range(9):
            if(board[i] == 0.5):
                change = board.copy()
                change[i] = player

                moveMatrix.append(change)

        return moveMatrix

    def minMax(board=[], player=-1):
        value = 0

        testStr = ""
        for i in range(9):
            if(board[i] == 0):
                testStr += "O"
            elif(board[i] == 1):
                testStr += "X"
            else:
                testStr += "."

        lines = BoardClass.lines

        found = False
        loop = -1

        for line in lines:
            loop += 1
            # if(loop%5000 == 0):
            #     print(loop)

            if(testStr in line):
                found = True
                if("Noughts" in lines[loop-1]):
                    if(player == 0):
                        value += 1

                        if(line.split('|').index(testStr) ==
                            len(line.split('|'))-2):

                            value += 150

                    else:
                        value -= 1

                        if(line.split('|').index(testStr) ==
                            len(line.split('|'))-3):
                            value -= 100

                elif("Crosses" in lines[loop-1]):
                    if(player == 0):
                        value -= 1

                        if(line.split('|').index(testStr) ==
                            len(line.split('|'))-3):
                            value -= 100

                    else:
                        value += 1

                        if(line.split('|').index(testStr) ==
                            len(line.split('|'))-2):
                            value += 150

                else:
                    value += 0

            elif(found and loop % 2 == 1):
                # print(line)
                # print(loop)
                break

        return value
