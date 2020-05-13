from simulator import *
from player import *
from team import *
from generateData import *
import json
import webbrowser
from copy import deepcopy


hitOutcomes = {"1B": 1, "2B": 2, "3B": 3, "HR": 4,}

cardinalsData = {
	"pitcher": generatePlayer("Wacha", 2014),
	"lineup": [
		generatePlayer("Carpenter, M", 2014),
		generatePlayer("Jon Jay", 2014),
		generatePlayer("Holliday", 2014),
		generatePlayer("peralta", 2014),
		generatePlayer("adams, m", 2014),
		generatePlayer("grichuk", 2014),
		generatePlayer("wong, ko", 2014),
		generatePlayer("cruz, t", 2014),
		generatePlayer("wainwright", 2014)
	]
}
giantsData =  {
	"pitcher": generatePlayer("Affeldt", 2014),
	"lineup": [
		generatePlayer("Pablo Sandoval", 2014),
		generatePlayer("Hunter Pence", 2014),
		generatePlayer("Belt", 2014),
		generatePlayer("Ishikawa", 2014),
		generatePlayer("Crawford", 2014),
		generatePlayer("Affeldt", 2014),
		generatePlayer("Blanco, G", 2014),
		generatePlayer("Panik", 2014),
		generatePlayer("Posey", 2014)
	]
}

cardinals = Team("Cardinals", cardinalsData['pitcher'], cardinalsData['lineup'])
giants = Team("Giants", giantsData['pitcher'], giantsData['lineup'])

teams = [cardinals, giants]
for t in teams:
	print("Pitcher: {}".format(t.pitcher))
	print("Lineup:")
	for p in t.lineup:
		print(p)
	print()
	print()

n = 10000
sims = []
for i in range(n):
	x = HalfInning(giants, cardinals, canWalkOff=True, runsNeededForWalkOff=1)
	x.simulate()
	sims.append(x)

results = {
	"endedWithWalkOff": 0,
	"ishikawaAtBats": 0,
	"ishikawaHits": 0,
	"ishikawaWalkoffs": 0,
	"ishikawaWalkoffHomeRuns": 0
}
for sim in sims:
	if sim.endedWithWalkOff:
		results['endedWithWalkOff'] += 1
	for pa in sim.log:
		if pa.batter.name == "Travis Ishikawa":
			results['ishikawaAtBats'] += 1
			if pa.outcome in hitOutcomes:
				results['ishikawaHits'] += 1
			if pa.outcome == "HR":
				results['ishikawaWalkoffHomeRuns'] += 1
	if sim.log[-1].batter.name == "Travis Ishikawa":
		if sim.endedWithWalkOff:
			results['ishikawaWalkoffs'] += 1



print("Total Simulations: {}".format(n))
print("Walk Off %: {}".format(  ( results['endedWithWalkOff'] / n) * 100 ))
print("Ishikawa Walk Off %: {}".format(  ( results['ishikawaWalkoffs'] / n) * 100  ))
print("Ishikawa Avg: {}".format(round( ( results['ishikawaHits'] / results['ishikawaAtBats']) , 2)))
print("% Chance that Ishikawa hit a walk off HR: {}".format( ( results['ishikawaWalkoffHomeRuns'] / n) * 100))









		







