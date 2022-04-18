from bs_game.utils import *

class Command:
	raw = ""
	playerTag = 0
	cmdType = ""
	cmdArgs = ""
	sys = None
	def isSys(self):
		return self.sys is not None
	def isTypeKnown(self):
		return self.cmdType == "b" or self.cmdType == "m" or self.cmdType == "e"
	def __parsePayload(self, payload):
		self.raw = payload
		if payload.startswith('p'):
			self.playerTag = convertToInt(payload[1:2])
			cmd = payload[3:]
			self.cmdType = cmd[:1]
			self.cmdArgs = cmd[2:].strip()
			self.sys = None
		else:
			sys = payload			
	def __init__(self, payload):
		self.__parsePayload(payload)
