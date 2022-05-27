# JSON based protocol
#
# The commands follows a common pattern that can be extended with custom arguments 
# for the different commands and also different kinds of games:
#
#		{ "gid": "<gameId>", "cmd":"<commandType>", "arg": <customArgumentsObject> }
#	where:
# 		<gameId> is the Id of the game to which this command is targeted
#		<commandType> is a user defining string designating the type of the command
#		<customArgumentsObject> is a user defined object containing the command specific data
#
# Protocol commands description:
#
# 		{ "gid": "<gameId>", "cmd":"j", "arg": { "board": "<encrypted board>" } }
#
#	Playr joins game and provides board positions in encrypted form with the <encrypted board> argument.
#	Command type "j" has aliases "join" and "joingame" that can also be used.
#
#		{ "gid": "<gameId>", "cmd":"m", "arg": { "hit": <wasHit>, "shot": [<X>, <Y>] } }
#
#	Player sends move, first with the <wasHit> argument confirm if previous shot by the opponent was
#	hit or miss (0 or 1) then the player shoots at guess location addressed by <X> and <Y> coordinates.
#	Command type "m" has alias "move" that can also be used.
#
#		{ "gid": "<gameId>", "cmd":"e", "arg": { "key": "<decryption key>" } }
#
#	The first player to send this command declares defeat (all his fleet is destroyed).
#	After that the other player should respond with the same command to declare win.
#	With the <decryption key> argument the player provides own key to decrypt his board that was initially provided.
#	Command type "e" has aliases "end" and "endgame" that can also be used.

from bs_game.utils import *
import json

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
