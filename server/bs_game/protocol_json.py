from bs_game.utils import *
import json

# JSON based protocol

class Command:
	raw = ""
	gameId = ""
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
			self.gameId = str(data["gid"]).lower()
			self.cmdType = str(data["cmd"]).lower()
			self.cmdArgs = data["arg"]
			# command aliases
			if self.cmdType == "create" or self.cmdType == "creategame": self.cmdType = "c"
			if self.cmdType == "join" or self.cmdType == "joingame": self.cmdType = "j"
			if self.cmdType == "end" or self.cmdType == "endgame": self.cmdType = "e"
			if self.cmdType == "move": self.cmdType = "m"
			return data
		except:
			return {}

	def __getKeySafe(self, data, key, defaultVal):
		return data[key] if not data is None and key in data else defaultVal

	def __copyRaw(self):
		return self.__parsePayload(self.raw)

	def __addPlayerTag(self, data):
		data["p"] = self.playerTag

	# command arguments

	def getArgs_j(self):
		return { "board": self.__getKeySafe(self.cmdArgs, "board", None)  }

	def getArgs_e(self):
		return { "key": self.__getKeySafe(self.cmdArgs, "key", None) }

	def getArgs_m(self):
		args = self.cmdArgs
		shot = args["shot"]
		if not isinstance(shot, list) or len(shot) == 0 or len(shot) % 2 != 0:
			raise
		hit = convertToInt(args["hit"]) if "hit" in args else 0
		return { "hit": hit, "x": shot[0], "y": shot[1] }

	# command responses

	def getResponse_error(self, msg):
		data = { "gid": self.gameId, "error": msg}
		self.__addPlayerTag(data)
		return json.dumps(data)

	def getResponse_j(self):
		data = self.__copyRaw()
		self.__addPlayerTag(data)
		return json.dumps(data)

	def getResponse_e(self, win):
		data = self.__copyRaw()
		self.__addPlayerTag(data)
		data["result"] = "win" if win else "defeat"
		return json.dumps(data)

	def getResponse_m(self):
		data = self.__copyRaw()
		self.__addPlayerTag(data)
		return json.dumps(data)
