import json
from game_battleships.protocol_response import ProtocolResponse
from game_battleships.utils import *
from game_battleships.log_dump import *

def append(list, item):
	if item is not None:
		list.append(json.loads(item))
 
class ProtocolInspect:

	def __init__(self, _gameManager):
		self._gameManager = _gameManager
		self.__lastRequest = ""

	def processInspect(self, data):
		response = ""
		self.__lastRequest = data
		if isinstance(data, str):
			parts = data.split("/")
			if len(parts) == 3 and parts[0] == "game":
				response = self.processInspect_game(parts[1], parts[2])
			if parts[0] == "dump":
				response = self.processInspect_dump(parts)
		return response

	def processInspect_game(self, opType, gameId):
		response = ""
		gameState = self._gameManager.getGame(gameId)

		if gameState is not None:
			
			pr = ProtocolResponse()
			list = []

			add_init = False
			add_moves = False
			add_end = False

			if opType == "all":
				add_init = True
				add_moves = True
				add_end = True

			if opType == "init":
				add_init = True
	
			if opType == "moves":
				add_moves = True

			if opType == "last":
				if gameState.result == 0:
					indexTurn = len(gameState.moveHistory) - 1
					if indexTurn >= 0:
						append(list, pr.getResponse_m(gameState, gameState.moveHistory[-1], indexTurn))
				else:
					add_end = True
			
			if add_init:
				append(list, pr.getResponse_c(gameState, 0)) # TODO: add timeout
				append(list, pr.getResponse_j(gameState, 1))
				append(list, pr.getResponse_j(gameState, 2))

			if add_moves:
				indexTurn = 0
				for m in gameState.moveHistory:
					append(list, pr.getResponse_m(gameState, m, indexTurn))
					indexTurn += 1

			if add_end:
				append(list, pr.getResponse_e(gameState, 1))
				append(list, pr.getResponse_e(gameState, 2))

			response = json.dumps(list)
		else:
			response = self.getResponse_error("no-such-game")

		return response

	def processInspect_dump(self, parts):

		if parts[1] == "games-list":

			games = []
			if parts[2] == "all":
				games = self._gameManager.getGames()
			elif parts[2] == "active":
				for game in self._gameManager.getGames():
					if game.status != 3:
						games.append(game)
			elif parts[2] == "finished":
				for game in self._gameManager.getGames():
					if game.status == 3:
						games.append(game)
			else:
				gameIds = parts[2].split(",")
				for game in self._gameManager.getGames():
					if game.getGameId() in gameIds:
						games.append(game)

			isFull = len(parts) > 3 and "full" in parts[3]
			showPlayers = not isFull and (len(parts) > 3 and "players" in parts[3])
			showPlayersDetails = isFull or (len(parts) > 3 and "players-details" in parts[3])
			showBoards = isFull or (len(parts) > 3 and "boards" in parts[3])
			showMoves = isFull or (len(parts) > 3 and "moves" in parts[3])

			dumpGameList(games, showPlayers, showPlayersDetails, showBoards, showMoves)

		return self.getResponse_ok()

	def getResponse_error(self, msg):
		data = {}
		data["req"] = self.__lastRequest
		data["error"] = msg
		return json.dumps(data)

	def getResponse_ok(self):
		data = {}
		data["req"] = self.__lastRequest
		data["status"] = "ok"
		return json.dumps(data)
