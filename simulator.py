from player import Player
from numpy.random import choice

PRINT_LOG_PLATE_APPEARENCES = True
PRINT_LOG_HALF_INNINGS = True
PRINT_LOG_GAMES = True
PRINT_LOG_SEASON = True

class PlateAppearance(object):

	def __init__(self, pitcher, batter):
		self.totalInnings = 1
		self.innings = 0
		self.pitcher = pitcher
		self.batter = batter
		self.outcome = None
		self.possibilities = []
		self.probabilities = []
		self.printLogEnabled = PRINT_LOG_PLATE_APPEARENCES

	def printLog(self, message):
		if self.printLogEnabled:
			print(message)

	""" 
	simulates the outcome of an plate appearence between a batter and a pitcher
	it takes the stats for each player and uses the average probability of a stat/outcome occuring

	returns a dictionary
	outcome: string, outcome of the plate appearence (1B, SO, HR, BB, etc...)
	possibilities: array, possible outcomes
	probabilities: array, chance of each possibility
	"""
	def simulate(self):
		for stat in self.pitcher.baseProbabilities:
			self.possibilities.append(stat)
			probability = (self.pitcher.baseProbabilities[stat] + self.batter.baseProbabilities[stat]) / 2
			self.probabilities.append(probability)
		
		# generate random outcome w/ probability
		self.outcome = choice(self.possibilities, 1, p=self.probabilities)[0]
		# update stats
		self.updateStats()
		#log
		self.printLog("{} vs {} | {}".format(self.pitcher.name, self.batter.name, self.outcome))


	def updateStats(self):
		self.pitcher.simulatedStats['PA'] += 1
		self.batter.simulatedStats['PA'] += 1
		self.pitcher.simulatedStats[self.outcome] += 1
		self.batter.simulatedStats[self.outcome] += 1

class HalfInning(object):

	def __init__(self, battingTeam, pitchingTeam, canWalkOff=False, runsNeededForWalkOff=0):
		self.battingTeam = battingTeam
		self.pitchingTeam = pitchingTeam
		self.outs = 0
		self.maxOuts = 3
		self.bases = [False, False, False]
		self.canWalkOff = canWalkOff # is true if bottom of last inning
		self.runsNeededForWalkOff = runsNeededForWalkOff
		self.endedWithWalkOff = False

		# logging
		self.runs = 0
		self.hits = 0
		self.walks = 0
		self.log = []
		self.printLogEnabled = PRINT_LOG_HALF_INNINGS

	def printLog(self, message):
		if self.printLogEnabled:
			print(message)

	def hit(self, basesToMove):
		# go through bases from front to back
		i = len(self.bases) - 1

		# move all of the runners runners
		while (i >= 0):
			if self.bases[i]: # if base is active
				# set base to inactive
				self.bases[i] = False
				if i + basesToMove >= 3:
					# runner scores, add to runs
					self.runs += 1
				else:
					# runner moves # of bases
					self.bases[i + basesToMove] = True
			i += -1
		# move the batter
		if basesToMove != 4: # if not a home run but batter on base
			self.bases[basesToMove - 1] = True 
		else: # if home run don't put batter on base and add a run
			self.runs += 1
		# update # of hits
		self.hits += 1

	def walk(self):

		# move runner if base is active and base before it is active
		i = len(self.bases) - 1
		while (i >= 0):
			if i == 0: # if base is first base
				if self.bases[i]: # if runner on first set second to active
					self.bases[i] = False
					self.bases[i + 1] = True

			elif self.bases[i] and self.bases[i-1]: # if base and base before it are active
				self.bases[i] = False # set base to inactive
				newBase = i + 1
				if newBase >= 3: # runner scores, add to runs
					self.runs += 1
				else:
					self.bases[newBase] = True # advance one base
			i += -1
		self.bases[0] = True # send batter to first
		# update # of walks
		self.walks += 1

	def out(self):

		self.outs += 1

	def simulate(self):
		hitOutcomes = {"1B": 1, "2B": 2, "3B": 3, "HR": 4,}
		walkOutcomes = ["BB","HBP"]
		outOutcomes = ["SO", "HitOut"]
		while self.outs < self.maxOuts:
			pitcher = self.pitchingTeam.pitcher
			batter = self.battingTeam.nextBatter()
			pa = PlateAppearance(pitcher, batter)
			pa.simulate()
			paOutcome = pa.outcome
			if paOutcome in hitOutcomes:
				# move all runners a # of bases, move batter to base
				basesToMove = hitOutcomes[paOutcome]
				self.hit(basesToMove)
			if paOutcome in walkOutcomes:
				# move batter to first, move runners if needed
				self.walk()
			if paOutcome in outOutcomes:
				# += 1 to outs
				self.out()

			
			# log plate appearence
			self.log.append(pa)
			# if walkoff is enabled and runs scored >= runsNeededForWalkOff, end inning
			if self.canWalkOff and self.runs >= self.runsNeededForWalkOff:
				self.endedWithWalkOff = True
				break

		self.printLog("Runs: {} | Hits: {} | Walks: {}".format(self.runs, self.hits, self.walks))

class Game(object):
	"""docstring for Game"""
	def __init__(self, homeTeam, awayTeam, inning=1, topOfInning=True):
		self.homeTeam = homeTeam
		self.awayTeam = awayTeam
		self.inning = inning
		self.maxInnings = 9
		self.topOfInning = topOfInning
		self.endedWithWalkOff = False
		self.gameOver = False
		self.log = [] # list of half innings
		self.printLogEnabled = PRINT_LOG_GAMES


	def __str__(self):
		if self.gameOver:
			string = "{} ({} - {}) vs {} ({} - {}) Final Score: {}".format(
				self.homeTeam.name,
				self.homeTeam.wins,
				self.homeTeam.losses,
				self.awayTeam.name,
				self.awayTeam.wins,
				self.awayTeam.losses,
				self.getScoreString())
		else:
			string = "{} ({} - {}) vs {} ({} - {})".format(
				self.homeTeam.name,
				self.homeTeam.wins,
				self.homeTeam.losses,
				self.awayTeam.name,
				self.awayTeam.wins,
				self.awayTeam.losses)
		return string

	def printLog(self, message):
		if self.printLogEnabled:
			print(message)

	def getWinningTeam(self):
		if self.homeTeam.runs > self.awayTeam.runs:
			return self.homeTeam
		if self.homeTeam.runs < self.awayTeam.runs:
			return self.awayTeam
		return None

	def getLosingTeam(self):
		if self.homeTeam.runs < self.awayTeam.runs:
			return self.homeTeam
		if self.homeTeam.runs > self.awayTeam.runs:
			return self.awayTeam
		return None

	def isTied(self):

		return self.homeTeam.runs == self.awayTeam.runs

	def getScore(self):
		return {
			"home": self.homeTeam.runs,
			"away": self.awayTeam.runs
		}

	def setScore(self, homeTeamRuns, awayTeamRuns):
		self.homeTeam.runs = homeTeamRuns
		self.awayTeam.runs = awayTeamRuns

	def getScoreString(self):

		return "{} - {}".format(self.getScore()['home'], self.getScore()['away'])

	def getInningHalfString(self):
		if self.topOfInning:
			return "Top"
		return "Bottom"

	def getGameStateString(self):
		return "{} | {} of Inning: {}".format(self.getScoreString(), self.getInningHalfString(), self.inning)

	def isBottomOfLastInning(self):
		return self.inning == self.maxInnings and not self.topOfInning

	def dontPlayBottomOfLast(self):
		return self.inning == self.maxInnings and self.getWinningTeam() == self.homeTeam and self.topOfInning

	def simulate(self):
		# reset teams plate appearences, runs, creates lineup
		self.homeTeam.newGame()
		self.awayTeam.newGame()
		while not self.gameOver:
			# simulate bottom/top of inning, add runs for batting team

			if self.topOfInning: # is top of inning
				battingTeam = self.awayTeam
				pitchingTeam = self.homeTeam
			else: # is bottom of inning
				battingTeam = self.homeTeam
				pitchingTeam = self.awayTeam
			# enables walk off if bottom of last inning
			canWalkOff = False
			walkOffRunsNeeded = 0
			if self.isBottomOfLastInning():
				canWalkOff = True
				walkOffRunsNeeded = self.awayTeam.runs - self.homeTeam.runs + 1
			# simulates inning
			halfInning = HalfInning(battingTeam, pitchingTeam, canWalkOff, walkOffRunsNeeded)
			halfInning.simulate()
			battingTeam.runs += halfInning.runs
			
			# log half inning
			self.log.append(halfInning)



			if halfInning.endedWithWalkOff: # set game to ended with walk off if inning ended in walk off
				self.endedWithWalkOff = True

			# if bottom of last inning and game is tied, add one more inning
			if self.isBottomOfLastInning() and self.isTied(): # inning + 1 because we already added 1 to the inning once it was simulated
				self.maxInnings += 1

			# game is over if top of the last inning and home team is winning
			if self.dontPlayBottomOfLast():
				self.gameOver = True

			# game is over if bottom of last inning and game is not tied
			if self.isBottomOfLastInning() and not self.isTied():
				self.gameOver = True
			else:
				# prepare next half inning
				if self.topOfInning:
					self.topOfInning = False
				else:
					self.inning += 1
					self.topOfInning = True


		self.printLog(self.getGameStateString())
		self.gameOver = True
		self.getWinningTeam().wins += 1
		self.getLosingTeam().losses += 1

class Season(object):
	"""docstring for Season"""
	def __init__(self, teams):
		self.teams = teams # list of Teams
		self.gameDays = 162
		self.daysPlayed = 0
		self.gamesInSeries = 3
		self.series = round(self.gameDays / self.gamesInSeries)
		self.gameDays = self.series * self.gamesInSeries
		self.seriesPlayed = 0
		self.schedule = self.createSchedule()
		self.printLogEnabled = PRINT_LOG_SEASON

	def printLog(self, message):
		if self.printLogEnabled:
			print(message)

	def createSchedule(self):
		# https://en.wikipedia.org/wiki/Round-robin_tournament

		teamPool = self.teams[:-1] # all teams except last
		standStill = self.teams[-1] # last team
		schedule = []

		for i in range(self.series):
			matches = [
				[teamPool[0], standStill] # first and last
			]
			unmatchedTeams = teamPool[1:]
			matchesLeft = int(len(unmatchedTeams) / 2)
			for j in range(matchesLeft):
				team1 = unmatchedTeams[j]
				team2 = unmatchedTeams[len(unmatchedTeams) - 1 - j]
				matches.append([team1, team2])

			# if i % 2 == 1: flip home and away
			if i % 2 == 0:
				for m in matches:
					m.reverse()

			# turns matches into n (self.gamesInSeries) Game objects and
			for i in range(self.gamesInSeries):
				day = []
				for m in matches:
					g = Game(m[0], m[1])
					day.append(g)
				schedule.append(day)


			teamPool.insert(0,teamPool.pop()) # move teams right by one
		return schedule

	def printSchedule(self):
		for i, day in enumerate(self.schedule):
			print("Day {}".format(i+1))
			for game in day:
				print(game)
			print("")

	def printUpcomingGames(self):
		day = self.schedule[self.daysPlayed]
		print("Day {}".format(self.daysPlayed + 1))
		for game in day:
			print(game)

	def printStandings(self):
		teamsSorted = sorted(self.teams, key=lambda x: x.wins, reverse=True)
		for t in teamsSorted:
			print(t)

	def printLeagueLeaders(self, stat, n, group="batting"):
		leaguePlayers = []
		for t in self.teams:
			for p in t.roster:
				if group == "batting":
					if p.position != "P":
						leaguePlayers.append(p)
				else: #group == "pitching"
					if p.position == "P":
						leaguePlayers.append(p)
		reverse = True if group == "batting" else False

		leaguePlayers.sort(key=lambda x: x.simulatedStats[stat], reverse=reverse)
		for i, p in enumerate(leaguePlayers[:n]):
			print("{} | {} | {}".format(i, p.simulatedStats[stat], p))

	def simulateNextDay(self):
		if self.daysPlayed < self.gameDays:
			day = self.schedule[self.daysPlayed]
			self.printLog("Day {}".format(self.daysPlayed + 1))
			for game in day:
				game.simulate()
				self.printLog(game)
			self.daysPlayed += 1

	def simulateRestOfSeason(self):
		while self.daysPlayed < self.gameDays:
			self.simulateNextDay()


		















		



