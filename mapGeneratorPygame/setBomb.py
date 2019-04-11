from mapGeneratorPygame.emptyMatrix import emptyMatrix
import random

mergedMatrix = emptyMatrix()
bombProp = []
obstacleProp = []

# Ścieżki dla 6 przykładowych bomb
bomb1Path = '../neuralNetwork/images/test1.png'
bomb2Path = '../neuralNetwork/images/test2.png'
bomb3Path = '../neuralNetwork/images/test3.png'
bomb4Path = '../neuralNetwork/images/test4.png'
bomb5Path = '../neuralNetwork/images/test5.png'
bomb6Path = '../neuralNetwork/images/test6.png'

# Ścieżki dla 4 przykładowych przeszkód
obstacle1Path = '../mapGeneratorPygame/obstacle/obst1.png'
obstacle2Path = '../mapGeneratorPygame/obstacle/obst2.png'
obstacle3Path = '../mapGeneratorPygame/obstacle/obst3.png'
obstacle4Path = '../mapGeneratorPygame/obstacle/obst4.png'

# Lista ścieżek do bomb
bombPathArray = ['empty', 'saper', bomb1Path, bomb2Path, bomb3Path, bomb4Path, bomb5Path, bomb6Path, obstacle1Path, obstacle2Path, obstacle3Path, obstacle4Path]

def randBombPos():
    i = 0
    while i <= 9:
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        bomb = random.randrange(2, 7)

        if(mergedMatrix[x][y] == 0):
            mergedMatrix[x][y] = bomb
            i += 1
            bombProp.append((x, y, bomb, bombPathArray[bomb], x * 64, y * 64, i))

def randObstaclePos():
    i =0
    while i <= 5:
        x = random.randrange(0, 9)
        y = random.randrange(0, 9)
        obstacle = random.randrange(8, 11)

        if(mergedMatrix[x][y] == 0):
            mergedMatrix[x][y] = obstacle
            i += 1
            obstacleProp.append((x, y, obstacle, bombPathArray[obstacle], x * 64, y * 64, i))


def printBombAndPos():
    randBombPos()
    return bombProp, mergedMatrix

