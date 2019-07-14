import random

class BoardClass:
    def fileReady(self):
        file = open("TTT_gamesDir/TTT_games.txt")
        ff = open("TTT_gamesDir/TTT_trimGames.txt")
        self.lines = file.readlines()
        self.trimlines = ff.readlines()
        file.close()
        ff.close()

        self.allInOne = []

        for line in self.trimlines:
            x = list(line)
            x.pop()
            self.allInOne.append(x)

        self.playCount = len(self.allInOne)

    def initBoard(self):
        return [0.5 for i in range(9)]

    def conv2Board(self, sboard):
        x = list(sboard)
        _board = []
        for i in x:
            if(i == "O"):
                _board.append(0)
            elif(i == "X"):
                _board.append(1)
            else:
                _board.append(0.5)

        return(_board)

    def printBoard(self, board, real=[]):
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

    def isComplete(self, board=[]):
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

    def pWon(self, board=[]):
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

    def getMoveOptions(self, board, player):
        moveMatrix = []

        for i in range(9):
            if(board[i] == 0.5):
                change = board.copy()
                change[i] = player

                moveMatrix.append(change)

        return moveMatrix

    def getOpponent(self, player):
        if(player == 0):
            return 1
        else:
            return 0


    def mmFunc(self, board, player):
        if(self.pWon(board) == self.getOpponent(player)):
            #opponent won
            return -50


        freePos = self.getMoveOptions(board, player)

        if(len(freePos) == 0):
            #draw
            return 0
        else:
            score = -2

            for opt in freePos:
                singleMoveScore = -self.mmFunc(opt, self.getOpponent(player))

                if(score < singleMoveScore):
                    score = singleMoveScore

            return score



    def minMax(self, board=[], player=-1):
        value = 0

        testStr = ""
        for i in range(9):
            if(board[i] == 0):
                testStr += "O"
            elif(board[i] == 1):
                testStr += "X"
            else:
                testStr += "."

        found = False
        loop = -1

        for line in self.lines:
            loop += 1

            if(testStr in line):
                found = True
                if("Noughts" in self.lines[loop-1]):
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

                elif("Crosses" in self.lines[loop-1]):
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
                break

        return value

    def getMoveValues(self, board, playerTurn):
        values = []

        nextOpts = self.getMoveOptions(board, playerTurn)
        fvalues = [-self.mmFunc(x, self.getOpponent(playerTurn)) for x in nextOpts]

        if(fvalues.count(50) == 0 and fvalues.count(0) > 1):
            drawOpts = []
            for i in range(len(nextOpts)):
                if(fvalues[i] == 0):
                    drawOpts.append(nextOpts[i])

            svalues = [self.minMax(x, playerTurn) for x in drawOpts]

            parsedOut = []
            loop = 0
            for i in range(len(fvalues)):
                if(fvalues[i] == 0):
                    parsedOut.append(svalues[loop])
                    loop+=1
                else:
                    parsedOut.append(fvalues[i])

            values = parsedOut
        else:
            values = fvalues

        return values

    def getPlayBoard(self, idx=random.randint(0,4519)):
        if(idx >= 0 and idx < len(self.allInOne)):
            return(self.allInOne[idx])
        else:
            return("INVALID INPUT")

if __name__ == "__main__":
    bc = BoardClass()
    bc.fileReady()

    # --- TO JE SAKRA DOBREJ SYSTÉM---

    #zkušební hry
    board2 = [  0,0.5,0.5,
              0.5,0.5,0.5,
              0.5,0.5,0.5]

    board = [  0,0.5,0.5,
             0.5,  1,0.5,
             0.5,0.5,0.5]

    board3 = [0.5,  1,0.5,
              0.5,0.5,0.5,
              0.5,0.5,0.5]

    #vytvořit list dalších možných her pro akt. hráče
    opts = bc.getMoveOptions(board,1)
    #spočítat hodnotu každého pohybu (-minmax)
    #!začít protihráčem akt. hráče
    vals = [-bc.mmFunc(x,0) for x in opts]

    opts2 = bc.getMoveOptions(board2,1)
    vals2 = [-bc.mmFunc(x,0) for x in opts2]

    bc.printBoard(vals,board)
    bc.printBoard(vals2,board2)

    outVals = vals2

    #když minimax vyhodnotí všechny ideální konce jako draw bude víc nul
    #a žádný dominantí tah
    if(vals2.count(50) == 0 and vals2.count(0) > 1):

        #zjistit, jaké tahy byly nejlepší (neskončí prohrou ale draw -> 0)
        newOpts = []
        for i in range(len(vals2)):
            if(vals2[i] == 0):
                newOpts.append(opts2[i])

        #nové tahy ohodnotit starým minmax alg.
        #(počet výher/remíz/proher z aktuální pozice až do konce)
        #To určí nejvýhodnější tahy proti ideal. i neideal. hráči
        newVals = [bc.minMax(x,0) for x in newOpts]

        #Přepsat output
        outPutFine = []
        loop = 0
        for i in range(len(vals2)):
            if(vals2[i] == 0):
                outPutFine.append(newVals[loop])
                loop+=1
            else:
                outPutFine.append(vals2[i])

        bc.printBoard(outPutFine,board2)

        print(outPutFine)
        outVals = outPutFine
    # --- TO TEDA JE ---

    takenValue = 0
    wantedOut = [0 for i in range(9)]
    for i in range(9):
        if(board2[i] != 0.5):
            takenValue += 1
        elif(outVals[i-takenValue] == max(outVals)):
            wantedOut[i] = 1

    print(wantedOut)
