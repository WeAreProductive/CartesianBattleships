class AdvanceProcessError(Exception):

	def toText(self):
		return f"{self.cat}:{self.msg}"

	def __init__(self, cat, msg):
		self.cat = cat # default ""
		self.msg = msg # default ""
