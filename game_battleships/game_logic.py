from game_battleships.log import *
from game_battleships.errors import *
from game_battleships.game_data import *
from game_battleships.game_verify import *

class BSGameLogic:
	def __init__(self, gameState):
		self._gameState = gameState

	def __startGame(self):
		if self._gameState.status == 0:
			self._gameState.status = 1 # strat with giving turn to player 1

	def __endGame(self, playerTag):
		if self._gameState.status == 1 or self._gameState.status == 2:
			self._gameState.status = 3
		if playerTag == 1 or playerTag == 2:
			self._gameState.result = playerTag

	def __isReadyToStart(self):
		return self._gameState.player1 is not None and self._gameState.player2 is not None
			#and self._gameState.player1.boardCrypt is not None and self._gameState.player2.boardCrypt is not None

	def __swithcTurn(self):
		if self._gameState.status == 1:
			self._gameState.status = 2
		elif self._gameState.status == 2:
			self._gameState.status = 1

	def __isValidMove(self, move):
		if move is None or not isinstance(move, BSGameMove): return False
		if move.wasHit != 0 and move.wasHit !=1: return False
		if move.mx < 0 or move.mx >= self._gameState._gameRules.boardSizeX: return False
		if move.my < 0 or move.my >= self._gameState._gameRules.boardSizeY: return False
		return True

	def __markLastMoveHit(self, playerTag, wasHit):
		if wasHit == 1:
			prev_move = self._gameState.getLastMove()
			player = self._gameState.getPlayerByTag(playerTag)
			if player is not None and prev_move is not None \
					and self.__isValidMove(prev_move) \
					and prev_move.player != playerTag \
					and player.board[prev_move.my][prev_move.mx] == 1:
				player.board[prev_move.my][prev_move.mx] = 2

	def __addPlayer(self, address, board):
		# game owner always joins as Player 1
		if self._gameState.isUserOwner(address):
			if self._gameState.player1 is not None:
				raise(AdvanceProcessError("game", "already-joined"))
			self._gameState.player1 = BSPlayer(self._gameState._gameRules, address, 1)
			self._gameState.player1.boardCrypt = board
			return self._gameState.player1
		# anyone of the invited players (except the owner) can join as Player 2
		if self._gameState.isUserInvited(address) and not self._gameState.isUserOwner(address):
			if self._gameState.player2 is not None:
				raise(AdvanceProcessError("game", "already-joined"))
			self._gameState.player2 = BSPlayer(self._gameState._gameRules, address, 2)
			self._gameState.player2.boardCrypt = board
			return self._gameState.player2
		# user not invited
		raise(AdvanceProcessError("game", "not-invited"))

	def processPlayerCommand(self, cmd):
		responsePayload = None
  
		if self._gameState is None:
			raise(AdvanceProcessError("sys", "no-such-game"))
		#if cmd.playerTag == 0:
		#	raise(AdvanceProcessError("sys", "no-such-player"))
		
		opponentTag = self._gameState.getOpponentTag(cmd.playerTag)
		player = self._gameState.getPlayerByTag(cmd.playerTag)
		opponent = self._gameState.getPlayerByTag(opponentTag)
		
		#if player is None or opponent is None:
		#	raise(AdvanceProcessError("game", "wrong-player"))

		# 'j' - player joins game and provides board in encrypted form
		if cmd.cmdType == 'j':
			# check if game is not started
			if self._gameState.status != 0:
				raise(AdvanceProcessError("game", "join-closed"))
			# validate board
			board = cmd.getArgs_j()["board"]
			if board is None or board.strip() == "":
				raise(AdvanceProcessError("game", "invalid-board"))
			# add player
			player = self.__addPlayer(cmd.sender, board)
			# prepare response
			cmd.syncPlayerTag(player.tag)
			responsePayload = cmd.getResponse_j()
			# check if both players are ready then give turn to player 1
			if self.__isReadyToStart():
				self.__startGame()

		# 'm' - player move
		if cmd.cmdType == 'm':
			# check if the game has started
			if  self._gameState.status == 0:
				raise(AdvanceProcessError("move", "game-pending"))
			# check if it's player's turn
			if  self._gameState.status != cmd.playerTag:
				raise(AdvanceProcessError("move", "wrong-turn"))
			# load arguments
			try:
				args = cmd.getArgs_m()
				move = BSGameMove(cmd.playerTag, args["hit"], args["x"], args["y"])
			except:
				raise(AdvanceProcessError("move", "bad-arguments"))
			# check if the move is valid
			if not self.__isValidMove(move):
				raise(AdvanceProcessError("move", "invalid"))
			# check if this move had already been played
			if opponent.board[move.my][move.mx] != 0:
				raise(AdvanceProcessError("move", "already-played"))
			# mark previous move on player's board if it was hit
			self.__markLastMoveHit(cmd.playerTag, move.wasHit)
			# add move to history
			self._gameState.moveHistory.append(move)
			# mark move on opponent's board
			opponent.board[move.my][move.mx] = 1
			# switch player turn
			self.__swithcTurn()
			# prepare response
			responsePayload = cmd.getResponse_m()

		# 'e' - end game
		if cmd.cmdType == 'e':
			# player declares defeat
			if self._gameState.status == cmd.playerTag:
				if player.keyCrypt is None:
					self.__markLastMoveHit(cmd.playerTag, 1)
					self.__endGame(opponentTag)
					# reveal player key
					player.keyCrypt = cmd.getArgs_e()["key"]
					# prepare response
					responsePayload = cmd.getResponse_e(False)
			# player confirming announced end game is a winner
			elif self._gameState.status == 3:
				if player.keyCrypt is None:
					# reveal player key
					player.keyCrypt = cmd.getArgs_e()["key"]
					# verify game play against revealed boards
					verifyError = verifyGame(self._gameState)
					# prepare response
					responsePayload = verifyError if verifyError is not None else cmd.getResponse_e(True)
			else:
				raise(AdvanceProcessError("move", "wrong-turn"))

		return responsePayload
