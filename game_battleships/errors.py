class AdvanceProcessError(Exception):
	cat = ""
	msg = ""

	def toText(self):
		return f"{self.cat}:{self.msg}"

	def __init__(self, cat, msg):
		self.cat = cat
		self.msg = msg
