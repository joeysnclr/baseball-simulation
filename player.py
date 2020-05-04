class Player(object):
	"""docstring for Player"""
	def __init__(self, name, position, year, seasonStats):
		self.name = name
		self.year = year
		self.seasonStats = seasonStats
		self.simulatedStats = self.initializeStats()
		self.baseProbabilities = self.getBaseProbabilities()

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
