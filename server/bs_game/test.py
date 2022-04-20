from bs_game.utils import *
from bs_game.log import *

class BSTest:
	def __init__(self, _gameState, _gameHandler):
		self._gameState = _gameState
		self._gameHandler = _gameHandler

	def send(self, playerTag, payload):
		logI("")
		player = self._gameState.getPlayerByTag(playerTag)
		plaeyerId = player.Id if player is not None else ""
		body = { "metadata": { "msg_sender": plaeyerId }, "payload": convertStringToAsciiByteText(payload) }
		response = self._gameHandler.processAdvance(self._gameState, body)

	def run(self):
		self.runTest1()
		
	def runTest1(self):
		self.send(1, "b: xxx123")
		self.send(1, "b: xxx123")
		self.send(2, "b: ccc123")
		self.send(2, "b: ccc123")


		#self.send(3, "p3 m: 0 1 1")
		
		#self.send(1, "p1 x: xxx")
		

		self.send(1, "m: 0 1 0")
		self.send(1, "m: 0 1 1")
		self.send(2, "m: 1 2 3")
		self.send(1, "m: 0 3 4")
		self.send(2, "m: 0 0 1")
		self.send(1, "m: 0 3 2")
		self.send(2, "m: 0 0 2")
		self.send(1, "m: 1 4 5")
		
		#dumpGameplayMoves(_gameState)
		
		#self.send(1, "e: rrr111")
		#self.send(1, "e: rrr111")

		self.send(2, "e: rrr111")
		#self.send(2, "e: rrr111")
		#dumpGamePlayers(_gameState)
		self.send(1, "e: rrr111")
		#self.send(1, "e: rrr111")
		#dumpGamePlayers(_gameState)

		#logI(f">>>>>>>>>> player turn {_gameState.status}")
		#processAdvance(2, "m: 0 4 4")
		#dumpGameplayBoards(_gameState)
