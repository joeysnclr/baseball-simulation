import pickle

from generateData import *
from player import *
from simulator import *
from team import *


def saveData(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def loadData(filename):
	with open(filename, 'rb') as data:
		return pickle.load(data)


x = generatePlayer("pujols", 2010)
print(x.seasonStats)
