import pygame
import sys
from ucs.allPriorityData import returnPriorityData
import time

returnPriorityData = returnPriorityData()

bombType = returnPriorityData[8]
graphNodes = returnPriorityData[1]
posList = returnPriorityData[2]
priority = returnPriorityData[3]
bombProp = returnPriorityData[4]
mapMatrix = returnPriorityData[5]
counter = returnPriorityData[6]
counterText = returnPriorityData[7]
allBombs = []

right = True
up = True
finish = False

moveX = 0
moveY = 0

def nextNode():
    print('rozbrajam')
    global moveX
    global moveY
    moveX = 0
    moveY = 0
    time.sleep(5)
    posList.pop(0)

def dist():
    global moveX, moveY, right, up, stop

    if posList[1][0] > posList[0][0]:
        moveX = posList[1][0] - posList[0][0]
        right = True
    elif posList[1][0] < posList[0][0]:
        moveX = posList[0][0] - posList[1][0]
        right = False
    elif moveX == 0 and posList[1][1] > posList[0][1]:
        moveY = posList[1][1] - posList[0][1]
        up = False
    elif moveX == 0 and posList[1][1] < posList[0][1]:
        moveY = posList[0][1] - posList[1][1]
        up = True

    if moveX + moveY > 0 and posList.__len__() > 1:
        if moveX > 0 and moveY >= 0 and right == True:
            moveX -= 1
            mapMatrix[posList[0][0]][posList[0][1]] = 0
            mapMatrix[posList[0][0] + 1][posList[0][1]] = 1
            posList[0][0] = posList[0][0] + 1
        elif moveX > 0 and moveY >= 0 and right == False:
            moveX -= 1
            mapMatrix[posList[0][0]][posList[0][1]] = 0
            mapMatrix[posList[0][0] - 1][posList[0][1]] = 1
            posList[0][0] -= 1
        elif moveX == 0 and moveY > 0:
            if up == True:
                moveY -= 1
                mapMatrix[posList[0][0]][posList[0][1]] = 0
                mapMatrix[posList[0][0]][posList[0][1] - 1] = 1
                posList[0][1] -= 1
            if up == False:
                moveY -= 1
                mapMatrix[posList[0][0]][posList[0][1]] = 0
                mapMatrix[posList[0][0]][posList[0][1] + 1] = 1
                posList[0][1] += 1
    elif posList[0][0] == 9 and posList[0][1] == 9:
        stop = True
        print('Wszystko rozbrojone!')
    # następny node
    else:
        if posList.__len__() > 1:
            nextNode()

bomb1Path = '../neuralNetwork/images/test1.png'
bomb2Path = '../neuralNetwork/images/test2.png'
bomb3Path = '../neuralNetwork/images/test3.png'
bomb4Path = '../neuralNetwork/images/test4.png'
bomb5Path = '../neuralNetwork/images/test5.png'
bomb6Path = '../neuralNetwork/images/test6.png'

bombsShowArr = [bomb1Path, bomb2Path, bomb3Path, bomb4Path, bomb5Path, bomb6Path]

bomb1 = pygame.image.load(bomb1Path)
bomb2 = pygame.image.load(bomb2Path)
bomb3 = pygame.image.load(bomb3Path)
bomb4 = pygame.image.load(bomb4Path)
bomb5 = pygame.image.load(bomb5Path)
bomb6 = pygame.image.load(bomb6Path)

stop = False

def app():
    # Kolory
    WHITE = (255, 255, 255)

    # Saper
    saper = pygame.image.load('saper/saper.png')
    escape = pygame.image.load('saper/escape.png')

    # Szerokość i wysokość okna aplikacji
    WINDOW_SIZE = [640, 640]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Automatyczny Saper - Mapa")
    pygame.init()
    pygame.font.init()
    done = False
    explode = False
    clock = pygame.time.Clock()
    FPS = 1
    myFont = pygame.font.SysFont('Comic Sans MS', 30)
    winFont = pygame.font.SysFont('Comic Sans MS', 64)
    counterFont = pygame.font.SysFont('Consolas', 30)
    textSurface = []
    pygame.time.set_timer(pygame.USEREVENT, 7000)
    global stop

    # Główna pętla
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.USEREVENT and stop == False:
                for i in range(10):
                    if counter[i] != sys.maxsize:
                        counter[i] -= 1
                        counterText[i] = str(counter[i]).rjust(2) if counter[i] > 0 else 'X'

        for i in counterText:
            if i == 'X':
                explode = True

        screen.fill(WHITE)

        for i in posList:
            if i[3] == 2:
                screen.blit(bomb1, (i[0] * 64, i[1] * 64))
            if i[3] == 3:
                screen.blit(bomb2, (i[0] * 64, i[1] * 64))
            if i[3] == 4:
                screen.blit(bomb3, (i[0] * 64, i[1] * 64))
            if i[3] == 5:
                screen.blit(bomb4, (i[0] * 64, i[1] * 64))
            if i[3] == 6:
                screen.blit(bomb5, (i[0] * 64, i[1] * 64))
            if i[3] == 7:
                screen.blit(bomb6, (i[0] * 64, i[1] * 64))
            if i != 0 and i != 9:
                screen.blit(myFont.render('x', False, (255, 10, 17)), (i[0] * 64 + 25, i[1] * 64 + 10))

        for i in range(10):
            for j in range(10):
                if mapMatrix[i][j] == 1:
                    screen.blit(saper, (i * 64, j * 64))
                if mapMatrix[i][j] == 15:
                    screen.blit(escape, (i * 64, j * 64))

        for i in range(10):
            textSurface.append(myFont.render(str(priority[i]), False, (0, 255, 17)))

        for i in range(10):
            screen.blit(textSurface[i], ((bombProp[i][4]) + 16, (bombProp[i][5]) + 16))

        for i in range(10):
            screen.blit(counterFont.render(counterText[i], True, (0, 229, 255)), ((bombProp[i][4]), (bombProp[i][5])))

        if stop == False:
            dist()
        else:
            screen.blit(winFont.render('Wszystko rozbrojone!', False, (255, 10, 17)), (150, 240))

        if explode == True:
            screen.fill(WHITE)
            screen.blit(winFont.render('Bomba wybuchła!', False, (255, 10, 17)), (150, 240))

        pygame.display.flip()
        clock.tick(FPS)
