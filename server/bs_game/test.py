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
		logI(f"{cc.test}-=-=-= Start test =-=-=-{cc.NC}")
		try:
			self.runTest2()
		except Exception as ex:
			logEX(ex)
		
	def runTest1(self):
		self.send(1, "j: xxx123")
		self.send(1, "j: xxx123")
		self.send(2, "j: ccc123")
		self.send(2, "j: ccc123")


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


	def runTest2(self):
		self.send(1, '{"gid":"###", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(2, '{"gid":"###", "cmd":"join", "arg":{ "board":"***" } }')

		self.send(1, '{"gid":"###", "cmd":"m", "arg":{ "x":1, "y": 0 } }')
		self.send(1, '{"gid":"###", "cmd":"m", "arg":{ "x":1, "y": 1 } }')
		self.send(2, '{"gid":"###", "cmd":"m", "arg":{ "x":2, "y": 3, "hit": 1} }')
		self.send(1, '{"gid":"###", "cmd":"m", "arg":{ "x":3, "y": 4 } }')
		self.send(2, '{"gid":"###", "cmd":"m", "arg":{ "x":0, "y": 1, "hit": 0} }')
		self.send(1, '{"gid":"###", "cmd":"m", "arg":{ "x":3, "y": 2, "hit": 0} }')
		self.send(2, '{"gid":"###", "cmd":"m", "arg":{ "x":0, "y": 2, "hit": 0} }')
		self.send(1, '{"gid":"###", "cmd":"m", "arg":{ "x":4, "y": 5, "hit": 1} }')

		self.send(2, '{"gid":"###", "cmd":"e", "arg":{ "key":"***" } }')
		self.send(1, '{"gid":"###", "cmd":"e", "arg":{ "key":"***" } }')
