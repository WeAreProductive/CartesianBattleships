# JSON based protocol
#
# The commands follows a common pattern that can be extended with custom arguments 
# for the different commands and also different kinds of games:
#
#		{ "gid": "<gameId>", "cmd":"<commandType>", "sys": <systemArgumentsObject>, "arg": <customArgumentsObject> }
#	where:
#		<gameId> is the Id of the game to which this command is targeted
#		<commandType> is a user defining string designating the type of the command
#		<systemArgumentsObject> is an object containing data related to system commands (might be missing)
#		<customArgumentsObject> is a user defined object containing the command specific data
#
# Protocol commands description:
#
#	- Create game
#		request:
#			{ "cmd":"c", 
#			  "sys": { "reqId":"<requestId>", "invite":["<userWalletAddress>", ...] },
#			  "arg": { "rules":{"size":[<boardSizeX>, <boardSizeX>], ships:{"5": 1, "4": 1, "3": 2, "2": "2"} } }}
#		response:
#			{ "gid": "<gameId>", "cmd":"c", 
#			  "sys": { "reqId":"<requestId>", "owner": "<creatorWalletAddress>", "invite":["<invitedUserWalletAddress>", ...], "timeout": <timeout> },
#			  "arg": { "rules":{"size":[<boardSizeX>, <boardSizeX>], ships:{"5": 1, "4": 1, "3": 2, "2": 2} } }}
#
#		User creates new game.
#		<requestId> is a user generated id used to identify the response at client side (should be unique per user)
#		The "invite" field contains a list of user (by wallet address) that are allowed to join the game, if empty then anyone can join
#		Command type "c" has aliases "create" and "creategame" that can also be used.
#		Response repeats request if valid and appends fields:
# 			"gid" - id of the newly created game
#			"sys"."owner" - wallet address of the user who created the game
#			"sys"."timeout" - game timeout
#
#	- Join game
#		request:
#			{ "gid": "<gameId>", "cmd":"j", "arg": { "board": "<encrypted board>" } }
#		response:
#			{ "gid": "<gameId>", "cmd":"j", "arg": { "board": "<encrypted board>", "p": <playerTag> } }
#
#		Player joins game and provides board positions in encrypted form with the <encrypted board> argument.
#		Command type "j" has aliases "join" and "joingame" that can also be used.
#		Response repeats request if valid and appends field "p" indicating playerTag (1 or 2).
#
#	- Move
#		request:
#			{ "gid": "<gameId>", "cmd":"m", "arg": { "hit": <wasHit>, "shot": [<X>, <Y>] } }
#		response:
#			{ "gid": "<gameId>", "cmd":"m", "arg": { "hit": <wasHit>, "shot": [<X>, <Y>], "p": <playerTag> } }
#
#		Player sends move, first with the <wasHit> argument confirm if previous shot by the opponent was
#		hit or miss (0 or 1) then the player shoots at guess location addressed by <X> and <Y> coordinates.
#		Command type "m" has alias "move" that can also be used.
#		Response repeats request if valid and appends field "p" indicating playerTag (1 or 2).
#
#	- End game
#		request:
#			{ "gid": "<gameId>", "cmd":"e", "arg": { "key": "<decryption key>" } }
#		response:
#			{ "gid": "<gameId>", "cmd":"e", "arg": { "key": "<decryption key>", "result": "win|defeat", "p": <playerTag> } }
#
#		The first player to send this command declares defeat (all his fleet is destroyed).
#		After that the other player should respond with the same command to declare win.
#		With the <decryption key> argument the player provides own key to decrypt his board that was initially provided.
#		Command type "e" has aliases "end" and "endgame" that can also be used.
#		Response repeats request if valid and appends field "p" indicating playerTag (1 or 2).

from game_battleships.utils import *
import json

class Command:
	sender = ""
	raw = ""
	gameId = ""
	playerTag = 0
	cmdType = ""
	cmdArgs = ""
	cmdSys = ""

	def __init__(self, sender, payload):
		self.sender = sender
		self.__parsePayload(payload)

	def syncPlayerTag(self, playerTag):
		self.playerTag = playerTag
	
	def getHandlerClass(self):
		if self.cmdType == "d":
			return "debug"
		if self.cmdType == "c":
			return "manager"
		if self.cmdType == "j" or self.cmdType == "m" or self.cmdType == "e":
			return "game"

	def __parsePayload(self, payload):
		self.raw = str(payload)
		try:
			data = json.loads(self.raw)
			self.gameId = str(getKeySafe(data, "gid", "")).lower()
			self.cmdType = str(getKeySafe(data, "cmd", "")).lower()
			self.cmdArgs = getKeySafe(data, "arg", {})
			self.cmdSys = getKeySafe(data, "sys", {})
			# command aliases
			if self.cmdType == "create" or self.cmdType == "creategame": self.cmdType = "c"
			if self.cmdType == "join" or self.cmdType == "joingame": self.cmdType = "j"
			if self.cmdType == "end" or self.cmdType == "endgame": self.cmdType = "e"
			if self.cmdType == "move": self.cmdType = "m"
			return data
		except:
			return {}

	def __copyRaw(self):
		return self.__parsePayload(self.raw)

	def __addPlayerTag(self, data):
		if not self.playerTag is None and self.playerTag != 0:
			data["arg"]["p"] = self.playerTag


# command arguments
 
	def getArgs_c(self):
		invite = getKeySafe(self.cmdSys, "invite", [])
		for i in range(len(invite)): invite[i] = invite[i].lower()
		return { \
			"owner": self.sender, \
			"reqId": getKeySafe(self.cmdSys, "reqId", None), \
			"invite": invite, \
			"rules": getKeySafe(self.cmdArgs, "rules", []) \
			}

	def getArgs_j(self):
		return { "board": getKeySafe(self.cmdArgs, "board", None)  }

	def getArgs_e(self):
		return { "key": getKeySafe(self.cmdArgs, "key", None) }

	def getArgs_m(self):
		args = self.cmdArgs
		shot = args["shot"]
		if not isinstance(shot, list) or len(shot) == 0 or len(shot) % 2 != 0:
			raise
		hit = convertToInt(args["hit"]) if "hit" in args else 0
		return { "hit": hit, "x": shot[0], "y": shot[1] }


# command responses

	def getResponse_error(self, msg):
		data = {}
		if not self.gameId is None: data["gid"] = self.gameId
		reqId = getKeySafe(self.cmdSys, "reqId", None)
		if not reqId is None: data["reqId"] = reqId
		data["error"] = msg
		data["arg"] = {}
		self.__addPlayerTag(data)
		return json.dumps(data)

	def getResponse_c(self, gameState, timeout):
		data = {
			"gid": gameState.getGameId(),
			"cmd": "c",
			"sys": {
				"reqId": gameState.getGameTokenCreate(),
				"owner": gameState.getGameOwner(),
				"invite": gameState.getInvite(),
				"timeout": timeout
			},
			"arg": { "rules": {
				"size": [gameState._gameRules.boardSizeX, gameState._gameRules.boardSizeY],
				"ships": gameState._gameRules.ships
			}}
		}
		return json.dumps(data)

	def getResponse_j(self):
		args = self.getArgs_j()
		data = {
			"gid": self.gameId,
			"cmd": "j",
			"arg": {
				"board": getKeySafe(args, "board", ""),
			}
		}
		self.__addPlayerTag(data)
		return json.dumps(data)

	def getResponse_e(self, win):
		args = self.getArgs_e()
		data = {
			"gid": self.gameId,
			"cmd": "e",
			"arg": {
				"key": getKeySafe(args, "key", ""),
				"result": "win" if win else "defeat"
			}
		}
		self.__addPlayerTag(data)
		return json.dumps(data)

	def getResponse_m(self):
		args = self.getArgs_m()
		data = {
			"gid": self.gameId,
			"cmd": "m",
			"arg": {
				"hit": getKeySafe(args, "hit", 0),
				"shot": [ getKeySafe(args, "x"), getKeySafe(args, "y") ]
			}
		}
		self.__addPlayerTag(data)
		return json.dumps(data)
