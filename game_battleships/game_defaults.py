from os import environ
from game_battleships.utils import *

# Values -1 (or negative) means the option is inactive and no check will be performed based on it (i.e. unlimited)

class GameDefaults:

	def __init__(self):
		self.serverId = environ.get("SERVER_ID")
		if self.serverId is None: self.serverId = ""
		self.limitGamesAll = convertToInt(environ.get("LIMIT_GAMES_ALL"), -1)
		self.limitGamesOwner = convertToInt(environ.get("LIMIT_GAMES_OWNER"), -1)
		self.timeoutGame = convertToInt(environ.get("TIMEOUT_GAME"), -1)