from bs_game.utils import *

# Plain Text based protocol

class Command:
	raw = ""
	playerTag = 0
	cmdType = ""
	cmdArgs = ""

	def __init__(self, playerTag, payload):
		self.playerTag = playerTag
		self.__parsePayload(payload)

	def isSys(self):
		return self.cmdType == "d"

	def isTypeKnown(self):
		return self.cmdType == "c" or self.cmdType == "j" or self.cmdType == "m" or self.cmdType == "e"

	def __parsePayload(self, payload):
		self.raw = payload
		self.cmdType = payload[:1]
		self.cmdArgs = payload[2:].strip()

	def getArgs_j(self):
		return { "board": self.cmdArgs }

	def getArgs_e(self):
		return { "key": self.cmdArgs }

	def getArgs_m(self):
		args = self.cmdArgs.split()
		if len(args) != 3:
			raise
		return { "hit": args[0], "x": args[1], "y": args[2] }
