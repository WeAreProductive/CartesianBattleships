from game_battleships.game_data import *
from game_battleships.game_defaults import *
from game_battleships.errors import *
# from bs_game.log_dump import *

# def processSystemCommand(_gameState, cmd):
# 	if (cmd == "dump-info"):
# 		dumpGameInfo(_gameState)
# 	if (cmd == "dump-players"):
# 		dumpGamePlayers(_gameState)
# 	if (cmd == "dump-boards"):
# 		dumpGameplayBoards(_gameState)
# 	if (cmd == "dump-moves"):
# 		dumpGameplayMoves(_gameState)
# 	if (cmd == "dump-all"):
# 		dumpAll()
# 	#if (cmd == "reset-game"):
# 	#	_gameState.reset()
# 		#_gameState = BSGameState(_gameState)
# 	#if (cmd == "quit"):
# 	#	logI("Shutdown!")
# 	#	os.system("shutdown")

class BSGameManager:
	__games = []
	__defaults = GameDefaults()
	__seedGameId = 0

	def __init__(self):
		pass

	def getGame(self, gameId):
		for g in self.__games:
			if g.gameId == gameId: return g
	
	def __generateGameId(self):
		self.__seedGameId += 1
		prefix = self.__defaults.prefixGameId
		if prefix != "": prefix += ":"
		return prefix + str(self.__seedGameId)

	def __validateNewGame(self, cmd, args):
		if self.__defaults.limitGamesAll >=0 and len(self.__games) >= self.__defaults.limitGamesAll:
			# error: reached the limit of maximum allowed count of games for this server
			raise(AdvanceProcessError("sys", "limit-owner-games"))
		if args["reqId"] is None or str(args["reqId"]).strip() == "":
			# error: requestId not provided or empty
			raise(AdvanceProcessError("sys", "no-requestId"))
		countGames = 0
		for g in self.__games:
			if g.getGameOwner() == cmd.sender:
				countGames += 1
				if g.getGameTokenCreate() == args["reqId"]:
					# error: requestId suplication (a game with the same requestId is already created by this owner)
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
			gameId = self.__generateGameId()
			gameState = BSGameState(GameDescriptor(gameId, cmd.sender, args["reqId"], args["invite"]), gameRules)
			self.__games.append(gameState)
			responsePayload = cmd.getResponse_c(gameState, self.__defaults.timeoutGame)

		return responsePayload