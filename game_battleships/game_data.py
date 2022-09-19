from os import environ
from game_battleships.utils import *

class BSGameRules:

	def __init__(self):
		self.boardSizeX = 10
		self.boardSizeY = 10
		self.ships = { "5": 1, "4": 1, "3": 2, "2": 2 }
		#countShip5 = 1 # count of 5pin ships (Carrier)
		#countShip4 = 1 # count of 4pin ships (Cruiser)
		#countShip3 = 2 # count of 3pin ships (Submarine)
		#countShip2 = 2 # count of 2pin ships (Frigate)
		self.timeoutTurn = 180 # player turn timeout [minutes]
		#_gameRules = BSGameRules()

class BSPlayer:
 
	def __init__(self, _gameRules, Id, tag):
		self.Id = str(Id).lower() # default ""
		self.tag = tag # default 0
		self.keyCrypt = None # default None
		self.boardCrypt = None # default None
		self.board = [ [ 0 for ix in range(_gameRules.boardSizeX) ] for iy in range(_gameRules.boardSizeY) ] # default None

class BSGameMove:

	def __init__(self, player, wasHit, mx, my):
		self.player = convertToInt(player) # default 0
		self.wasHit = convertToInt(wasHit) # default 0
		self.mx = convertToInt(mx) # default -1
		self.my = convertToInt(my) # default -1

class GameDescriptor:

	def __init__(self, gameId, owner, tokenCreate, invite):
		self.gameId = str(gameId) # default ""
		self.owner = str(owner) # default ""
		self.tokenCreate = str(tokenCreate) # default ""
		self.invite = invite # default []

class BSGameStateBase:
	def getGameId(self): return self.descriptor.gameId
	def getGameOwner(self): return self.descriptor.owner
	def getGameTokenCreate(self): return self.descriptor.tokenCreate
	def getInvite(self): return self.descriptor.invite
 
	def isUserOwner(self, address): return self.getGameOwner() == address

	def isUserInvited(self, address):
		return len(self.descriptor.invite) == 0 or str(address).lower() in self.descriptor.invite

	def isUserAllowed(self, address):
		return self.isUserOwner(address) or self.isUserInvited(address)

	def __init__(self, descriptor):
		self.descriptor = descriptor
		self.gameId = descriptor.gameId

class BSGameState(BSGameStateBase):
	
	def __init__(self, descriptor, _gameRules):
		super().__init__(descriptor)
		self._gameRules = _gameRules
		self.player1 = None
		self.player2 = None
		self.moveHistory = []
		self.status = 0 # 0 - waiting for players to be ready, 1 - waiting move from player 1, 2 - waiting move from player 2, 3 - game ending
		self.result = 0 # 0 - to be decided, 1 - player 1 is winner, 2 - player 2 is winner
		# TODO: status for cheating
	
	def getPlayerByTag(self, playerTag):
		if playerTag == 1:
			return self.player1
		if playerTag == 2:
			return self.player2
	
	def getPlayerTagById(self, id):
		if not self.player1 is None and self.player1.Id == id: return 1
		if not self.player2 is None and self.player2.Id == id: return 2
		return 0
	
	def getOpponentTag(self, player):
		return 2 if (player == 1) else 1

	def getLastMove(self):
		return self.moveHistory[-1] if len(self.moveHistory) > 0 else None
