import statsapi, json, requests
from player import *
from team import *

def findPlayer(lookup_value, year):
	lookupInfo = statsapi.lookup_player(lookup_value, season=year)
	if lookupInfo == []:
		return None
	playerId = lookupInfo[0]['id']
	return playerId

def generatePlayer(lookup_value, year, playerId=None):
	"""
		returns a Player object based on lookup_vaue and year
		currently creates a Player object based on career stats, switch to year
	"""
	if playerId == None:
		playerId = findPlayer(lookup_value, year)

	playerData = statsapi.player_stat_data(playerId, type="yearByYear")
	# get player data
	playerName = "{} {}".format(playerData['first_name'], playerData['last_name'])
	playerPosition = playerData['position']
	outfieldPositions = ["RF", "CF", "LF"]
	if playerPosition in outfieldPositions:
		playerPosition = "OF"

	isPitcher = playerPosition == "P"
	playerStatGroup = "pitching" if isPitcher else "hitting"

	playerStats = None
	for statGroup in playerData['stats']:
		if statGroup['season'] == str(year) and statGroup['group'] == playerStatGroup:
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

	startingPitcher = False
	if playerPosition == "P":
		gamesPlayed = playerStats['gamesPlayed']
		gamesStarted = playerStats['gamesStarted']
		if gamesStarted >= gamesPlayed * .6:
			startingPitcher = True
	playerObject = Player(playerName, playerPosition, year, playerStatsSimple, startingPitcher=startingPitcher)
	return playerObject

def generateTeam(teamName, year):
	teamLookup = statsapi.lookup_team(teamName, activeStatus="B", season=year, sportIds=1)
	teamId = teamLookup[0]['id']
	team = statsapi.get("team_roster", {"teamId": teamId, "season": year})
	roster = []
	for plyr in team['roster']:
		if plyr['status']['code'] == "A":
			pObj = generatePlayer("", year, playerId=plyr['person']['id'])
			roster.append(pObj)

	return Team(teamName, roster)


