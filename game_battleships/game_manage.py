from game_battleships.game_data import *
from game_battleships.game_defaults import *
from game_battleships.errors import *

class BSGameManager:

	def __init__(self):
		self.__games = []
		self.__defaults = GameDefaults()
		self.__seedGameId = 0

	def getDefaults(self):
		return self.__defaults

	def getGame(self, gameId):
		for g in self.__games:
			if g.gameId == gameId: return g

	def getGames(self):
		return self.__games

	def __generateGameId(self, messageData):
		self.__seedGameId += 1
		serverId = self.__defaults.serverId
		if serverId != "": serverId = "_" + serverId
		index = "_" + str(messageData.epoch_index) + "_" + str(messageData.input_index)
		return str(self.__seedGameId) + index + serverId

	def __validateNewGame(self, cmd, args):
		if self.__defaults.limitGamesAll >=0 and len(self.__games) >= self.__defaults.limitGamesAll:
			# error: reached the limit of maximum allowed count of games for this server
			raise(AdvanceProcessError("sys", "limit-owner-games"))
		if args["reqId"] is None or str(args["reqId"]).strip() == "":
			# error: requestId not provided or empty
			raise(AdvanceProcessError("sys", "no-requestId"))
		countGames = 0
		for g in self.__games:
			if g.getGameOwner() == cmd.getSender():
				countGames += 1
				if g.getGameTokenCreate() == args["reqId"]:
					# error: requestId duplication (a game with the same requestId is already created by this owner)
					raise(AdvanceProcessError("sys", "duplicate-requestId"))
		if self.__defaults.limitGamesOwner >=0 and countGames >= self.__defaults.limitGamesOwner:
			# error: reached the limit of maximum allowed count of games for this owner
			raise(AdvanceProcessError("sys", "limit-owner-games"))
		# TODO: validate: game rules

	def __limitBoardSize(self, sz):
		val = convertToInt(sz)
		if val < 5: return 5
		if val > 25: return 25
		return val

	def __processGameRules(self, args):
			rules = args["rules"]
			gameRules = BSGameRules()

			boardSize = getKeySafe(rules, "size")
			if isinstance(boardSize, list) and len(boardSize) >= 1:
				gameRules.boardSizeX = self.__limitBoardSize(boardSize[0])
				gameRules.boardSizeY = self.__limitBoardSize(boardSize[1 if len(boardSize) >= 2 else 0])

			boardSize = getKeySafe(rules, "size", None)

			return gameRules

	def processPlayerCommand(self, cmd):
		responsePayload = None

		# 'c' - create game
		if cmd.cmdType == 'c':
			args = cmd.getArgs_c()
			self.__validateNewGame(cmd, args)
			gameRules = self.__processGameRules(args)
			gameId = self.__generateGameId(cmd.messageData)
			gameState = BSGameState(GameDescriptor(gameId, cmd.getSender(), args["reqId"], args["invite"]), gameRules)
			self.__games.append(gameState)
			responsePayload = cmd.getResponse_c(gameState, self.__defaults.timeoutGame)

		return responsePayload