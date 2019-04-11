from PIL import Image
import numpy as np
import functools
from collections import Counter

def createExamples(path, exampleFile):
    numberArrayExamples = open(exampleFile, 'a')
    numbersWeHave = range(0, 6)
    versionWeHave = range(1, 9)
    for eachNum in numbersWeHave:
        for eachVer in versionWeHave:
            imgFilePath = path + str(eachNum) + '.' + str(eachVer) + '.png'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei);
            eiar1 = str(eiar.tolist())
            lineToWrite = str(eachNum) + '::' + eiar1 + '\n'
            numberArrayExamples.write(lineToWrite)
    numberArrayExamples.close()


def threshold(imageArray):
    balanceAr = []
    newAr = imageArray
    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum = functools.reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3])
            balanceAr.append(avgNum)
    balance = functools.reduce(lambda x, y: x + y, balanceAr) / len(balanceAr)
    for eachRow in newAr:
        for eachPix in eachRow:
            if functools.reduce(lambda x, y: x + y, eachPix[:3]) / len(eachPix[:3]) > balance:
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
                eachPix[3] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
                eachPix[3] = 255
    return newAr


def whatBombIsThis(filePath, examplePath):
    matchedAr = []
    loadExamps = open(examplePath, 'r').read()
    loadExamps = loadExamps.split('\n')
    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()
    inQuestion = str(iarl)
    for eachExample in loadExamps:
        if len(eachExample) > 3:
            splitEx = eachExample.split('::')
            currentNum = splitEx[0]
            currentAr = splitEx[1]
            eachPixEx = currentAr.split('],')
            eachPixInQ = inQuestion.split('],')
            x = 0
            while x < len(eachPixEx):
                if eachPixEx[x] == eachPixInQ[x]:
                    matchedAr.append(int(currentNum))
                x += 1
    x = Counter(matchedAr).most_common(1)
    if x[0][0] == 0:
        return 'zegarowa'
    elif x[0][0] == 1:
        return 'dynamit'
    elif x[0][0] == 2:
        return 'cieplna'
    elif x[0][0] == 3:
        return 'biologiczna'
    elif x[0][0] == 4:
        return 'przeciwpiechotna'
    elif x[0][0] == 5:
        return 'przeciwpancerna'

