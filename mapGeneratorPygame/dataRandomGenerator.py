import random
import sys


def getTime(bombType):
    if bombType == 'zegarowa':
        return random.randrange(5, 80)
    elif bombType == 'dynamit':
        return random.randrange(3, 20)
    elif bombType == 'cieplna' or bombType == 'biologiczna' or bombType == 'przeciwpiechotna' or bombType == 'przeciwpancerna':
        return sys.maxsize
    else:
        return -1


def getCost(bombType):
    if bombType == 'biologiczna' or bombType == 'przeciwpancerna':
        return random.randrange(10000, 100000000)
    elif bombType == 'zegarowa' or bombType == 'dynamit' or bombType == 'cieplna' or bombType == 'przeciwpiechotna':
        return random.randrange(100, 1000000)
    else:
        return -1
