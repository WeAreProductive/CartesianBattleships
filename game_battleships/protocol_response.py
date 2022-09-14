import json
from game_battleships.utils import *
from game_battleships.game_data import *

class ProtocolResponse:

	def __addPlayerTag(self, data, playerTag):
		if not playerTag is None and playerTag != 0:
			data["arg"]["p"] = playerTag

	def getResponse_c(self, gameState, timeout):
		data = {
			"gid": gameState.getGameId(),
			"cmd": "c",
			"sys": {
				"reqId": gameState.getGameTokenCreate(),
				"owner": gameState.getGameOwner(),
				"invite": gameState.getInvite(),
				"timeout": timeout
			},
			"arg": { "rules": {
				"size": [gameState._gameRules.boardSizeX, gameState._gameRules.boardSizeY],
				"ships": gameState._gameRules.ships
			}}
		}
		return json.dumps(data)

	def getResponse_j(self, gameState, playerTag):
		player = gameState.getPlayerByTag(playerTag)

		if player is None:
			return None
  
		data = {
			"gid": gameState.getGameId(),
			"cmd": "j",
			"arg": {
				"board": player.boardCrypt,
			}
		}
		self.__addPlayerTag(data, playerTag)

		return json.dumps(data)

	def getResponse_m(self,  gameState, move):
		data = {
			"gid": gameState.getGameId(),
			"cmd": "m",
			"arg": {
				"hit": move.wasHit,
				"shot": [ move.mx, move.my ]
			}
		}
		self.__addPlayerTag(data, move.player)
		
		return json.dumps(data)