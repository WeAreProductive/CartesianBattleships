from game_battleships.protocol_response import ProtocolResponse
from game_battleships.utils import *
#from game_battleships.log_dump import *
import json

class ProtocolInspect:
	lastRequest = ""

	def __init__(self, _gameManager):
		self._gameManager = _gameManager

	def processInspect(self, data):
		response = ""
		self.lastRequest = data
		if isinstance(data, str):
			parts = data.split("/")
			if len(parts) == 3 and parts[0] == "game":
				response = self.processInspect_game(parts[1], parts[2])
		return response

	def processInspect_game(self, opType, gameId):
		response = ""
		gameState = self._gameManager.getGame(gameId)

		if gameState is not None:
			
			pr = ProtocolResponse()
			list = []
   
			add_init = False
			add_moves = False

			if opType == "all":
				add_init = True
				add_moves = True

			if opType == "init":
				add_init = True
	
			if opType == "moves":
				add_moves = True

			if opType == "last":
				if len(gameState.moveHistory) > 0:
					list.append(json.loads(pr.getResponse_m(gameState, gameState.moveHistory[-1])))
			
			if add_init:
				list.append(json.loads(pr.getResponse_c(gameState, 0))) # TODO: add timeout
				list.append(json.loads(pr.getResponse_j(gameState, 1)))
				list.append(json.loads(pr.getResponse_j(gameState, 2)))

			if add_moves:
				for m in gameState.moveHistory:
					list.append(json.loads(pr.getResponse_m(gameState, m)))

			response = json.dumps(list)
		else:
			response = self.getResponse_error("no-such-game")

		return response

	def getResponse_error(self, msg):
		data = {}
		data["req"] = self.lastRequest
		data["error"] = msg
		return json.dumps(data)