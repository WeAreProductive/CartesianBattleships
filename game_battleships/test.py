from bs_game.utils import *
from bs_game.log import *

class BSTest:
	def __init__(self, _gameManager, _gameHandler):
		self._gameManager = _gameManager
		self._gameHandler = _gameHandler

	def getPlayerAddressByTag(self, tag):
		if tag == 1: return "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
		if tag == 2: return "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
		if tag == 3: return "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
		return ""

	def send(self, gid, playerTag, payload):
		logI("")
		plaeyerId = self.getPlayerAddressByTag(playerTag)
		body = { "metadata": { "msg_sender": plaeyerId }, "payload": convertStringToAsciiByteText(payload.replace("#gid", gid)) }
		response = self._gameHandler.processAdvance(self._gameManager, body)

	def run(self):
		logI(f"{cc.test}-=-=-= Start test =-=-=-{cc.NC}")
		try:
			#self.runTest1()
			self.runTest3()
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
		
		gid = "1"

		self.send("", 1, '{"cmd":"c", "sys": { "reqId": "111", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[8, 8] } } }')

		self.send(gid, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 3], "hit": 1} }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 0] } }')
		self.send(gid, 3, '{"gid":"#gid", "cmd":"join", "arg":{ "board":"***" } }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid, 2, '{"gid":"#gid", "cmd":"join", "arg":{ "board":"***" } }')
		self.send(gid, 2, '{"gid":"#gid", "cmd":"join", "arg":{ "board":"***" } }')


		self.send(gid, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 0] } }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 1] } }')
		self.send(gid, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 3], "hit": 1} }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [3, 4] } }')
		self.send(gid, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [0, 1], "hit": 0} }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [3, 2], "hit": 0} }')
		self.send(gid, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [0, 2], "hit": 0} }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [4, 5], "hit": 1} }')

		self.send(gid, 2, '{"gid":"#gid", "cmd":"e", "arg":{ "key":"***" } }')
		self.send(gid, 1, '{"gid":"#gid", "cmd":"e", "arg":{ "key":"***" } }')


	def runTest3(self):
		
		gid1 = "1"
		gid2 = "2"
		gid3 = "3"

		self.send("", 1, '{"cmd":"c", "sys": { "reqId": "111", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[8, 8] } } }')
		self.send(gid1, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')

		self.send("", 1, '{"cmd":"c", "sys": { "reqId": "222", "invite": ["0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"] }, "arg": { "rules":{"size":[8, 8] } } }')
		self.send(gid2, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
  
		self.send("", 2, '{"cmd":"c", "sys": { "reqId": "222", "invite": ["0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"] }, "arg": { "rules":{"size":[8, 8] } } }')
  
		self.send(gid1, 2, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid2, 3, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
  
		self.send(gid3, 3, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid3, 2, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
  
  
		self.send(gid1, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 0] } }')
		self.send(gid2, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 1] } }')

		self.send(gid1, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 0] } }')
		self.send(gid2, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 1] } }')
