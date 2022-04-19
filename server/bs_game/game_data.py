from os import environ
from bs_game.utils import *

class BSGameRules:
	boardSizeX = convertToInt(environ.get("CBS_RULE_BOARD_SX"), 8)
	boardSizeY = convertToInt(environ.get("CBS_RULE_BOARD_SY"), 8)
	countShip5 = convertToInt(environ.get("CBS_RULE_SHIP_COUNT_5"), 1) # count of 5pin ships (Carrier)
	countShip4 = convertToInt(environ.get("CBS_RULE_SHIP_COUNT_4"), 1) # count of 4pin ships (Cruiser)
	countShip3 = convertToInt(environ.get("CBS_RULE_SHIP_COUNT_3"), 2) # count of 3pin ships (Submarine)
	countShip2 = convertToInt(environ.get("CBS_RULE_SHIP_COUNT_2"), 2) # count of 2pin ships (Frigate)
	timeoutTurn = convertToInt(environ.get("CBS_TIMEOUT_TURN"), 180) # player turn timeout [minutes]
#_gameRules = BSGameRules()


class BSPlayer:
	Id = ""
	keyCrypt = None
	boardCrypt = None
	board = None
	def __init__(self, _gameRules, Id):
		self.Id = Id
		self.board = [ [ 0 for ix in range(_gameRules.boardSizeX) ] for iy in range(_gameRules.boardSizeY) ]

class BSGameMove:
	player = 0
	wasHit = 0
	mx = -1
	my = -1
	def __init__(self, player, wasHit, mx, my):
		self.player = convertToInt(player) ; self.wasHit = convertToInt(wasHit) ; self.mx = convertToInt(mx) ; self.my = convertToInt(my)

class BSGameState:
	_gameRules = None
	gameId = ""
	player1 = None
	player2 = None
	moveHistory = []
	status = 0 # 0 - waiting for players to be ready, 1 - waiting move from player 1, 2 - waiting move from player 2, 3 - game ending
	result = 0 # 0 - to be decided, 1 - player 1 is winner, 2 - player 2 is winner
	# TODO: status for cheating
	
	def __init__(self, _gameRules, gameId):
		self._gameRules = _gameRules
		self.gameId = str(gameId)

	def addPlayer(self, id):
		if self.player1 is None:
			self.player1 = BSPlayer(self._gameRules, id)
			return
		if self.player2 is None:
			self.player2 = BSPlayer(self._gameRules, id)
			return
	
	def startGame(self):
		if self.status == 0:
			self.status = 1 # strat with giving turn to player 1
			
	def endGame(self, playerTag):
		if self.status == 1 or self.status == 2:
			self.status = 3
		if playerTag == 1 or playerTag == 2:
			self.result = playerTag
	
	def swithcTurn(self):
		if self.status == 1:
			self.status = 2
		elif self.status == 2:
			self.status = 1
	
	def getPlayerByTag(self, playerTag):
		if playerTag == 1:
			return self.player1
		if playerTag == 2:
			return self.player2
	
	def getPlayerTagById(self, id):
		if self.player1.Id == id: return 1
		if self.player2.Id == id: return 2
		return 0
	
	def getOpponentTag(self, player):
		return 2 if (player == 1) else 1
	
	def isValidMove(self, move):
		if move is not None and isinstance(move, BSGameMove) is BSGameMove: return False
		if move.wasHit != 0 and move.wasHit !=1: return False
		if move.mx < 0 or move.mx >= self._gameRules.boardSizeX: return False
		if move.my < 0 or move.my >= self._gameRules.boardSizeY: return False
		return True

	def markLastMoveHit(self, playerTag, wasHit):
		if wasHit == 1:
			prev_move = self.moveHistory[-1] if len(self.moveHistory) > 0 else None
			player = self.getPlayerByTag(playerTag)
			if player is not None and prev_move is not None:
				if self.isValidMove(prev_move) and prev_move.player != playerTag and player.board[prev_move.mx][prev_move.my] == 1:
					player.board[prev_move.mx][prev_move.my] = 2	
