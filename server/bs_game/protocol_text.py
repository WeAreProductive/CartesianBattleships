# Plain Text based protocol
#
# Protocol commands description:
#
# 		j <encrypted board>
#
#	Playr joins game and provides board positions in encrypted form with the <encrypted board> argument.
#
#		m <wasHit> <X> <Y>
#
#	Player sends move, first with the <wasHit> argument confirm if previous shot by the opponent was
#	hit or miss (0 or 1) then the player shoots at guess location addressed by <X> and <Y> coordinates.
#
#		e <decryption key>
#
#	The first player to send this command declares defeat (all his fleet is destroyed).
#	After that the other player should respond with the same command to declare win.
#	With the <decryption key> argument the player provides own key to decrypt his board that was initially provided.

from bs_game.utils import *

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

	# command arguments

	def getArgs_j(self):
		return { "board": self.cmdArgs }

	def getArgs_e(self):
		return { "key": self.cmdArgs }

	def getArgs_m(self):
		args = self.cmdArgs.split()
		if len(args) != 3:
			raise
		return { "hit": args[0], "x": args[1], "y": args[2] }

	# command responses

	def getResponse_error(self, msg):
		return f"error p{self.playerTag} {msg}"

	def getResponse_j(self):
		return f"board p{self.playerTag} {self.cmdArgs}"

	def getResponse_e(self, win):
		result = "win" if win else "defeat"
		return f"end p{self.playerTag} {result} {self.cmdArgs}"

	def getResponse_m(self):
		args = self.getArgs_m()
		return f"move p{self.playerTag} {args['hit']} {args['x']} {args['y']}"