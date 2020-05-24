from generateData import *
from player import *
from simulator import *
from team import *


# USAGE

# create 2 teams and save
team1 = generateTeam("Dodgers", 2018)
team2 = generateTeam("Red Sox", 2018)

# create a game
worldSeries = Game(team1, team2)
# simulate the game
worldSeries.simulate()
# view the results
print(worldSeries)
