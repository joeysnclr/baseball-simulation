from player import Player
from numpy.random import choice

PRINT_LOG_PLATE_APPEARENCES = False
PRINT_LOG_HALF_INNINGS = False
PRINT_LOG_GAMES = False

class PlateAppearance(object):

	def __init__(self, pitcher, batter):
		self.totalInnings = 1
		self.innings = 0
		self.pitcher = pitcher
		self.batter = batter
		self.outcome = None

	""" 
	simulates the outcome of an plate appearence between a batter and a pitcher
	it takes the stats for each player and uses the average probability of a stat/outcome occuring

	returns a dictionary
	outcome: string, outcome of the plate appearence (1B, SO, HR, BB, etc...)
	possibilities: array, possible outcomes
	probabilities: array, chance of each possibility
	"""
	def simulate(self):
		possibilities = []
		probabilities = []
		for stat in self.pitcher.baseProbabilities:
			possibilities.append(stat)
			probability = (self.pitcher.baseProbabilities[stat] + self.batter.baseProbabilities[stat]) / 2
			probabilities.append(probability)
		
		self.outcome = choice(possibilities, 1, p=probabilities)[0]
		# update stats
		self.updateStats()
		response = {
			"outcome": self.outcome,
			"possibilities": possibilities,
			"probabilities": probabilities,
			"pitcher": self.pitcher.name,
			"batter": self.batter.name
		}
		return response

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
		self.canWalkOff = canWalkOff
		self.runsNeededForWalkOff = runsNeededForWalkOff
		self.endedWithWalkOff = False

		# logging
		self.runs = 0
		self.hits = 0
		self.walks = 0
		self.log = []
		self.printLogEnabled = PRINT_LOG_PLATE_APPEARENCES

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
			pa = PlateAppearance(pitcher, batter).simulate()
			paOutcome = pa['outcome']
			if paOutcome in hitOutcomes:
				# move all runners a # of bases
				basesToMove = hitOutcomes[paOutcome]
				self.hit(basesToMove)
			if paOutcome in walkOutcomes:
				# move a runner to first, move runners if needed
				self.walk()
			if paOutcome in outOutcomes:
				# += 1 to outs
				self.out()

			# if walkoff is enabled and runs scored >= runsNeededForWalkOff, inning will be ended after logging
			if self.canWalkOff and self.runs >= self.runsNeededForWalkOff:
				self.endedWithWalkOff = True
			# log plate appearence
			self.printLog("{} vs {} | {} | Bases: {} | Outs: {}".format(pitcher.name, batter.name, paOutcome, self.bases, self.outs))
			paDict = {
				"paInfo": pa,
				"bases": [b for b in self.bases],
				"outs": self.outs,
			}
			self.log.append(paDict)

			if self.endedWithWalkOff:
				break



		response = {
			"battingTeam": self.battingTeam.name,
			"pitchingTeam": self.pitchingTeam.name,
			"runs": self.runs,
			"hits": self.hits,
			"walks": self.walks,
			"plateAppearences": len(self.log),
			"endedWithWalkOff": self.endedWithWalkOff,
			"log": self.log
			
		}
		return response

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
		self.homeTeam.reset()
		self.awayTeam.reset()
		self.log = [] # list of half innings
		self.printLogEnabled = PRINT_LOG_HALF_INNINGS

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

	def simulate(self):
		self.printLog("{} of Inning {} | {}".format(self.getInningHalfString(), self.inning, self.getScoreString()))
		while self.inning <= self.maxInnings:
			if self.inning == self.maxInnings and self.getWinningTeam() == self.homeTeam and not self.topOfInning:
				# game is over if bottom of the last inning and home team is winning
				break

			# simulate bottom/top of inning, add runs for batting team
			if self.topOfInning: # is top of inning
				halfInning = HalfInning(self.awayTeam, self.homeTeam).simulate()
				self.awayTeam.runs += halfInning['runs']
			else: # is bottom of inning
				# enables walk off if bottom of last inning
				canWalkOff = False
				walkOffRunsNeeded = 0
				if self.inning == self.maxInnings:
					canWalkOff = True
					walkOffRunsNeeded = self.awayTeam.runs - self.homeTeam.runs + 1
				halfInning = HalfInning(self.homeTeam, self.awayTeam, canWalkOff, walkOffRunsNeeded).simulate()
				self.homeTeam.runs += halfInning['runs']
			

			if halfInning['endedWithWalkOff']: # set game to ended with walk off if inning ended in walk off
				self.endedWithWalkOff = True

			# log half inning
			self.printLog("{} of Inning {} | {}".format(self.getInningHalfString(), self.inning, self.getScoreString()))
			haDict = {
				"haInfo": halfInning,
				"inning": self.inning,
				"top": self.topOfInning,
				"score": {
					"home": self.homeTeam.runs,
					"away": self.awayTeam.runs
				},
				"log": halfInning['log']
			}
			self.log.append(haDict)

			# if bottom of last inning and game is tied, add one more inning
			if self.inning == self.maxInnings and self.isTied() and not self.topOfInning: # inning + 1 because we already added 1 to the inning once it was simulated
				self.maxInnings += 1

			# prepare next half inning
			if self.topOfInning:
				self.topOfInning = False
			else:
				self.inning += 1
				self.topOfInning = True
		self.gameOver = True
		response = {
			"log": self.log,
			"winningTeam": self.getWinningTeam(),
			"losingTeam": self.getLosingTeam(),
			"score": self.getScore(),
			"walkOff": self.endedWithWalkOff
		}
		return response

class Season(object):
	"""docstring for Season"""
	def __init__(self, teams):
		self.teams = teams # list of Teams
		self.games = 162
		self.gamesPlayed = 0

	def simulate(self):
		while self.gamesPlayed <= self.games:
			game = Game(self.teams[0], self.teams[1])
			gameInfo = game.simulate()
			if game.getWinningTeam() != None:
				game.getWinningTeam().wins += 1
				game.getLosingTeam().losses += 1
			else:
				game.awayTeam.ties += 1
				game.homeTeam.ties += 1
			print(game.getScoreString())
			self.gamesPlayed += 1
		















		



