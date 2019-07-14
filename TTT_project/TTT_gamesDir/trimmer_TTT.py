#!/usr/bin/env python3
from tqdm import tqdm

fW = open("TTT_trimGames.txt", 'a')
fSpec = open("TTT_trimGames.txt", 'r')
fR = open("TTT_games.txt", "r")

allLines = fR.readlines()
fR.close()

qwertz = fSpec.readlines()
games = []

for line in qwertz:
    x = list(line)
    x.pop()
    s = "".join(x)
    games.append(s)

startPos = 0

if(len(games) != 0):
    lastPos = games[len(games)-1]

    startPos = 0
    for line in range(len(allLines)):
        if(lastPos in allLines[line]):
            startPos = line
            break

    print("startPos {}".format(startPos))

print("Prep Done")

gameCount = len(games)
for i in tqdm(range(startPos, len(allLines))):
    if(i % 10000 == 0):
        tqdm.write("{}/{}".format(i,len(allLines)))

    if(i%2==1):
        xxx = allLines[i].split('|')
        xxx.pop()
        xxx.pop()
        for game in xxx:
            free = True
            for item in range(gameCount):
                if(games[item] == game):
                    free = False
                    break

            if(free):
                gameCount += 1
                games.append(game)
                fW.write("{}\n".format(game))
