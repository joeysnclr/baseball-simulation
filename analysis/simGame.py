from simulator import *
from player import *
from team import *
from generateData import *
import json
import webbrowser
from copy import deepcopy
import pickle

def saveData(obj, filename):
	with open(filename, 'wb') as output:  # Overwrites any existing file.
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def loadData(filename):
	with open(filename, 'rb') as data:
		return pickle.load(data)

def userOption(options):
	valid = False
	while not valid:
		validChoices = []
		for i, o in enumerate(options):
			print("{} | {}".format(i, o))
			validChoices.append(str(i))
		choice = input("Choose >> ")
		if choice in validChoices:
			valid = True
		else:
			print("Invalid Choice")
	return options[int(choice)]

teams = loadData("season2019.pkl")
season = Season(teams)

def play():
	playing = True
	while playing:
		choices = [
			"Sim Next Game",
			"Sim Next Games",
			"League Leaders Batting",
			"League Leaders Pitching",
			"Standings",
			"Todays Games"
		]
		choice = userOption(choices)
		if choice == choices[0]:
			season.simulateNextDay()
		if choice == choices[1]:
			games = int(input("Games >> "))
			for i in range(games):
				season.simulateNextDay()
		if choice == choices[2]:
			stat = input("Enter Stat >> ")
			season.printLeagueLeaders(stat, 10)
		if choice == choices[3]:
			stat = input("Enter Stat >> ")
			season.printLeagueLeaders(stat, 10, "pitching")
		if choice == choices[4]:
			season.printStandings()
		if choice == choices[5]:
			season.printUpcomingGames()
		input()
play()