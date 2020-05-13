import statsapi, json, requests
from player import *
from team import *

def player_stat_data_yearByYear(playerId):
	r = requests.get("https://statsapi.mlb.com/api/v1/people/{}?hydrate=currentTeam,team,stats(type=yearByYear(team(league)),leagueListId=mlb_hist)&site=en".format(playerId))
	return r.json()['people'][0]


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

	playerData = player_stat_data_yearByYear(playerId)
	# get player data
	playerName = playerData['fullName']
	playerPosition = playerData['primaryPosition']['abbreviation']
	outfieldPositions = ["RF", "CF", "LF"]
	if playerPosition in outfieldPositions:
		playerPosition = "OF"

	playerStats = None
	for season in playerData['stats'][0]['splits']:
		if season['season'] == str(year):
			playerStats = season['stat']
		
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

# generateTeam("Giants", 2010)

