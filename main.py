from simulator import *
from player import *
from team import *
from generateData import *
import json
import webbrowser
from copy import deepcopy


pitcher = generatePlayer("Mariano Rivera", 1999)
batter = generatePlayer("Barry Bonds", 2004)


home = Team("Team 1", deepcopy(pitcher), [deepcopy(batter) for i in range(9)])
away = Team("Team 2", deepcopy(pitcher), [deepcopy(batter) for i in range(9)])


# Mariano Rivera save % against Barry Bonds Lineup
saves = 0
games = 0
for i in range(1000):
	g = Game(home, away, inning=9, topOfInning=False)
	g.setScore(0, 1)
	g.simulate()
	if g.getWinningTeam() == away:
		saves += 1
	games += 1
	print(g.endedWithWalkOff)

print("Games: " + str(games))
print("Saves: " + str(saves))
print("Save %: " + str( (saves / games) * 100 ))

