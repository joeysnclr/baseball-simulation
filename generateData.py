import statsapi, json
from player import *
from team import *


def generatePlayer(lookup_value, year):
	"""
		returns a Player object based on lookup_vaue and year
		currently creates a Player object based on career stats, switch to year
	"""
	print("Generating Player from: {}, {}".format(lookup_value, year))
	lookupInfo = statsapi.lookup_player(lookup_value, season=year)
	if lookupInfo == []:
		return None
	playerId = lookupInfo[0]['id']
	playerData = statsapi.player_stat_data(playerId, type="career")
	# get player data
	playerName = "{} {}".format(playerData['first_name'], playerData['last_name'])
	playerPosition = playerData['position']

	playerStatGroup = "pitching" if playerPosition == "P" else "hitting"
	playerStats = None
	for statGroup in playerData['stats']:
		if statGroup['group'] == playerStatGroup:
			playerStats = statGroup['stats']
	plateAppearences = playerStats['battersFaced'] if playerPosition == "P" else playerStats['plateAppearances']
	playerStatsSimple = {
		"PA": plateAppearences,
		"1B": playerStats['hits'] - playerStats['doubles'] - playerStats['triples'] - playerStats['homeRuns'], # Hits - 2B - 3B - HR
		"2B": playerStats['doubles'],
		"3B": playerStats['triples'],
		"HR": playerStats['homeRuns'],
		"SO": playerStats['strikeOuts'],
		"BB": playerStats['baseOnBalls'],
		"HBP": playerStats['hitByPitch'],
		"HitOut": plateAppearences - playerStats['baseOnBalls'] - playerStats['hitByPitch'] - playerStats['hits'] - playerStats['strikeOuts']# PA - BB - HBP - Hits - SO
	}
	playerObject = Player(playerName, playerPosition, year, playerStatsSimple)
	return playerObject

def generateTeam(lookup_value, year):
	x = statsapi.lookup_team(lookup_value, activeStatus="B", season=year, sportIds=1)
	y = statsapi.get("team_roster", {"teamId": x[0]['id'], "season": year})
	print(json.dumps(y, indent=1))


# generateTeam("Giants", 2010)

