import random

class BoardClass:

    def fileReady(self):
        file = open("TTT_games.txt")
        ff = open("TTT_trimGames.txt")
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

        '''
        self.allInOne = []
        for i in range(len(self.lines)):
            if(i % 2 == 1):
                x = self.lines[i].split("|")
                x.pop() #pop \n
                x.pop() #pop "The solution"
                for y in x:
                    self.allInOne.append(y)

        self.playCount = len(self.allInOne)
        '''

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
            # if(loop%5000 == 0):
            #     print(loop)

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
                # print(line)
                # print(loop)
                break

        return value

    def getPlayBoard(self, idx=random.randint(0,4519)):
        if(idx >= 0 and idx < len(self.allInOne)):
            return(self.allInOne[idx])
        else:
            return("INVALID INPUT")

if __name__ == "__main__":
    bc = BoardClass()
    bc.fileReady()

    print(bc.getPlayBoard(1000))
    print(bc.conv2Board(bc.getPlayBoard(1000)))
