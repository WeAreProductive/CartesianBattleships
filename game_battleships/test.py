from game_battleships.utils import *
from game_battleships.log import *

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
		body = { "metadata": { "msg_sender": plaeyerId, "epoch_index": 0, "input_index": 0 }, "payload": convertStringToHexBytes(payload.replace("#gid", str(gid) + "_0_0")) }
		response = self._gameHandler.processAdvance(self._gameManager, body)

	def run(self, testName):
		if testName is None: return

		logI(f"{cc.test}-=-=-= Start test =-=-=-{cc.NC}")
		try:
			if testName == "1":  self.runTest1(); return
			if testName == "3":  self.runTest3(); return
			if testName == "4":  self.runTest4(); return
			logErr("Test with such name does not exist!")
		except Exception as ex:
			logEX(ex)
		
	def runTest1(self):
		self.runTest4()


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
		self.send(gid2, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 1], "hit": 1 } }')

		self.send(gid1, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 0] } }')
		self.send(gid2, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 1] } }')

		self.send(gid1, 1, '{"gid":"#gid", "cmd":"e", "arg":{ "key": "reveal" } }')
		self.send(gid1, 2, '{"gid":"#gid", "cmd":"e", "arg":{ "key": "reveal2" } }')

	def runTest4(self):
		gid1 = "1"
		gid2 = "2"
		gid3 = "3"
		gid4 = "4"

		#self.send("", 1, '{"cmd":"c", "sys": { "reqId": "111", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[15, 15] } } }')
		self.send(gid1, 1, '{"cmd":"c", "sys": { "reqId": "111", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[15] } } }')
		self.send(gid2, 1, '{"cmd":"c", "sys": { "reqId": "222", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[15] } } }')
		self.send(gid3, 1, '{"cmd":"c", "sys": { "reqId": "333", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[15] } } }')
		self.send(gid4, 1, '{"cmd":"c", "sys": { "reqId": "444", "invite": ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8"] }, "arg": { "rules":{"size":[15] } } }')

		self.send(gid1, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid1, 2, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')

		self.send(gid2, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid2, 2, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')

		self.send(gid3, 1, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')
		self.send(gid3, 2, '{"gid":"#gid", "cmd":"j", "arg":{ "board":"***" } }')

		self.send(gid1, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 1] } }')
		self.send(gid1, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 2] } }')
		self.send(gid1, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [3, 3] } }')
		self.send(gid1, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [4, 4] } }')

		self.send(gid2, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [4, 2] } }')
		self.send(gid2, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [6, 3] } }')

		self.send(gid3, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [1, 1] } }')
		self.send(gid3, 2, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [2, 1] } }')
		self.send(gid3, 1, '{"gid":"#gid", "cmd":"m", "arg":{ "shot": [3, 1] } }')

		self.send(gid1, 1, '{"gid":"#gid", "cmd":"e", "arg":{ "key": "reveal" } }')
		self.send(gid1, 2, '{"gid":"#gid", "cmd":"e", "arg":{ "key": "reveal2" } }')
