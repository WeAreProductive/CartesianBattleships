from bs_game.utils import *
import json

# JSON based protocol

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
		self.raw = str(payload)
		try:
			data = json.loads(self.raw)
			self.cmdType = str(data["cmd"]).lower()
			self.cmdArgs = data["arg"]
			# command aliases
			if self.cmdType == "create" or self.cmdType == "creategame": self.cmdType = "c"
			if self.cmdType == "join" or self.cmdType == "joingame": self.cmdType = "j"
			if self.cmdType == "end" or self.cmdType == "endgame": self.cmdType = "e"
			if self.cmdType == "move": self.cmdType = "m"
		except:
			pass

	def __getKeySafe(self, data, key, defaultVal):
		return data[key] if not data is None and key in data else defaultVal

	def getArgs_j(self):
		return { "board": self.__getKeySafe(self.cmdArgs, "board", None)  }

	def getArgs_e(self):
		return { "key": self.__getKeySafe(self.cmdArgs, "key", None) }

	def getArgs_m(self):
		args = self.cmdArgs
		if not {"x", "y"} <= args.keys():
			raise
		hit = convertToInt(args["hit"]) if "hit" in args else 0
		return { "hit": hit, "x": args["x"], "y": args["y"] }
