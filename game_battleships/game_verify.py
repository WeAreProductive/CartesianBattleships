from game_battleships.utils import *

def verifyGame(_gameState):
	return None

class BSGameVerify:
	def __init__(self, gameState):
		self._gameState = gameState

	def decryptPlayerBoard(self, board_encrypted, key):
		pass

	def __parseBoard(self, board_format):
		vals = list(filter(lambda str: str!="", board_format.strip().split(" ")))
		if len(vals) % 2 != 0: return []
		board = []
		for i in range(0, len(vals), 2):
			cx = convertToInt(vals[i], -1)
			cy = convertToInt(vals[i + 1], -1)
			if cx < 0 or cy < 0: return []
			board.append((cx, cy))
		return board
 	
	def validatePlayerBoard(self, board):
		# check if coordinates are on board
		for i in range(len(board)):
			cx = board[i][0] ; cy = board[i][1]
			bx = self._gameState._gameRules.boardSizeX ; by = self._gameState._gameRules.boardSizeY
			if (cx < 0 or cx > bx or cy < 0 or cy > by) : return -1
		return 0

	def verify(self):
		pass