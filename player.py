class Player(object):
	"""docstring for Player"""
	def __init__(self, name, position, year, seasonStats, startingPitcher=False):
		self.name = name
		self.year = year
		self.position = position
		self.startingPitcher = startingPitcher
		self.seasonStats = seasonStats
		self.advancedSeasonStats = self.calcAdvancedStats(seasonStats)
		self.simulatedStats = self.initializeStats()
		self.baseProbabilities = self.getBaseProbabilities()
		self.rating = self.getInitialRating() # player rating out of 100

	def __str__(self):
		return "{} | {}".format(self.name, self.position)

	"""
	returns a dictionary of
	stat: chance
	where stat = SO, 1B, BB, HR, etc...
	and chance is the % chance of that stat being the outcome
	"""
	def getBaseProbabilities(self):
		response = {}
		for stat in self.seasonStats:
			if stat == "PA":
				continue
			chance = self.seasonStats[stat] / self.seasonStats["PA"]
			response[stat] = chance
		return response

	def initializeStats(self):
		response = {}
		for stat in self.seasonStats:
			response[stat] = 0
		return response

	def getInitialRating(self):
		rating = 100
		return rating

	def calcAdvancedStats(self, statDict):
		s = statDict
		obp = (s['1B'] + s['2B'] + s['3B'] + s['HR'] + s['BB'] + s['HBP']) / s['PA'] # (hits + bb + hbp) / pa
		slg = ( s['1B'] + (2 * s['2B']) + (3 * s['3B']) + (4 * s['HR']) ) / (s['PA'] - s['BB'] - s['HBP'])  # (1B) +( 2 x 2B) + ( 3 x 3B) + ( 4 x HR) / AB.
		ops = obp + slg
		advancedStats = {
			"obp": round(obp, 4),
			"slg": round(slg, 4),
			"ops": round(ops, 4)
		}
		return advancedStats

