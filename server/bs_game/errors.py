class AdvanceProcessError(Exception):
	playerTag = None
	msg = ""
	def toText(self):
		return f"error p{self.playerTag} {self.msg}"
	def __init__(self, playerTag, msg):
		self.playerTag = playerTag
		self.msg = msg
