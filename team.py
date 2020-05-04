

class Team(object):
	"""docstring for Team"""
	def __init__(self, name, pitcher, lineup):
		self.name = name # name of team
		self.pitcher = pitcher # Player
		self.lineup = lineup # array of Player
		self.plateAppearences = 0 # used to determine nextBatter
		self.runs = 0 # runs scored
		self.wins = 0 # games won
		self.losses = 0 # games lost

	def __str__(self):
		return "{} | {} - {} - {}".format(self.name, self.wins, self.losses, self.ties)

	def nextBatter(self):
		batter = self.lineup[self.plateAppearences % len(self.lineup)]
		self.plateAppearences += 1
		return batter

	def reset(self):
		self.plateAppearences = 0 # used to determine nextBatter
		self.runs = 0 # runs scored

	def createSchedule(self, opponents):
		# create a schedule of games for a season
		return

		