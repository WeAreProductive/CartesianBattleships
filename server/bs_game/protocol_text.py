from bs_game.utils import *

class Command:
	raw = ""
	playerTag = 0
	cmdType = ""
	cmdArgs = ""

	def isSys(self):
		return self.cmdType == "d"

	def isTypeKnown(self):
		return self.cmdType == "b" or self.cmdType == "m" or self.cmdType == "e"

	def __parsePayload(self, payload):
		self.raw = payload
		self.cmdType = payload[:1]
		self.cmdArgs = payload[2:].strip()

	def __init__(self, playerTag, payload):
		self.playerTag = playerTag
		self.__parsePayload(payload)
