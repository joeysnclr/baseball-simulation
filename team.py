import random

class Team(object):
	"""docstring for Team"""
	def __init__(self, name, roster):
		self.name = name # name of team
		self.roster = roster
		self.pitcher = None # Player, current player
		self.lineup = [] # array of Player
		self.plateAppearences = 0 # used to determine nextBatter
		self.runs = 0 # runs scored
		self.wins = 0 # games won
		self.losses = 0 # games lost

	def __str__(self):
		return "{} | {} - {}".format(self.name, self.wins, self.losses)

	def nextBatter(self):
		batter = self.lineup[self.plateAppearences % len(self.lineup)]
		self.plateAppearences += 1
		return batter

	def newGame(self):
		self.plateAppearences = 0 # used to determine nextBatter
		self.runs = 0 # runs scored
		self.pitcher = self.getRandomStartingPitcher() #starting pitcher
		self.lineup = self.createLineup() # create lineup order

	def createSchedule(self, opponents):
		# create a schedule of games for a season
		return

	def getRandomStartingPitcher(self):
		starters = [p for p in self.roster if p.startingPitcher]
		return random.choice(starters)

	def printRoster(self):
		self.roster.sort(key=lambda x: x.position, reverse=True)
		for p in self.roster:
			print(p)

	def createLineup(self):
		positionsNeeded = ["C", "1B", "2B", "3B", "SS", "OF", "OF", "OF"]
		batters = [p for p in self.roster if p.position != "P" and p.seasonStats['PA'] >= 100]
		batters.sort(key=lambda x: x.advancedSeasonStats['obp'], reverse=True)
		lineupPool = [] # batters in lineup, not in order
		# add best player from each position to lineupPool
		for pos in positionsNeeded:
			posPlayers = [p for p in batters if p.position == pos]
			# adds best player in that position to lineup
			if posPlayers != []:
				lineupPool.append(posPlayers[0]) # adds to line up pool
				batters.remove(posPlayers[0]) # removes from batters not in lineup
		
		for b in lineupPool:
			positionsNeeded.remove(b.position) # removes position fom being needed

		# if team had no players from that position choose random backup
		for pos in positionsNeeded:
			randomBackup = random.choice(batters)
			randomBackup.position = pos
			lineupPool.append(randomBackup) # adds to line up pool
			batters.remove(randomBackup) # removes from batters not in lineup
			positionsNeeded.remove(pos) # removes position fom being needed

		# add best batter that didn't make lineupPool, this is DH
		lineupPool.append(batters[0])
		batters.remove(batters[0])


		slotOrderAndStat = [
			(3, "ops"),
			(4, "ops"),
			(1, "obp"),
			(8, "obp"),
			(6, "ops"),
			(5, "ops"),
			(2, "obp"),
			(7, "obp"),
			(9, "obp"),
		] # the order the slots will be willed and based off which stat
		lineupOrder = []
		for slot in slotOrderAndStat:
			slotNum = slot[0]
			slotStat = slot[1]
			lineupPool.sort(key=lambda x: x.advancedSeasonStats[slotStat], reverse=True)
			player = lineupPool[0]
			lineupOrder.append(player)
			lineupPool.remove(player)
		return lineupOrder






		