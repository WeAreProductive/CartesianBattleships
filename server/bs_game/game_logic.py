from bs_game.log import *
from bs_game.errors import *
from bs_game.game_data import *
from bs_game.game_verify import *

class BSGameLogic:
	def __init__(self, gameState):
		self._gameState = gameState

	def startGame(self):
		if self._gameState.status == 0:
			self._gameState.status = 1 # strat with giving turn to player 1

	def endGame(self, playerTag):
		if self._gameState.status == 1 or self._gameState.status == 2:
			self._gameState.status = 3
		if playerTag == 1 or playerTag == 2:
			self._gameState.result = playerTag

	def swithcTurn(self):
		if self._gameState.status == 1:
			self._gameState.status = 2
		elif self._gameState.status == 2:
			self._gameState.status = 1

	def isValidMove(self, move):
		if move is None or not isinstance(move, BSGameMove): return False
		if move.wasHit != 0 and move.wasHit !=1: return False
		if move.mx < 0 or move.mx >= self._gameState._gameRules.boardSizeX: return False
		if move.my < 0 or move.my >= self._gameState._gameRules.boardSizeY: return False
		return True

	def markLastMoveHit(self, playerTag, wasHit):
		if wasHit == 1:
			prev_move = self._gameState.getLastMove()
			player = self._gameState.getPlayerByTag(playerTag)
			if player is not None and prev_move is not None \
					and self.isValidMove(prev_move) \
					and prev_move.player != playerTag \
					and player.board[prev_move.my][prev_move.mx] == 1:
				player.board[prev_move.my][prev_move.mx] = 2

	def processPlayerCommand(self, cmd):
		responsePayload = None
		
		try:
			if not cmd.isTypeKnown():
				raise(AdvanceProcessError(cmd.playerTag, "sys:unknown-command"))
			
			opponentTag = self._gameState.getOpponentTag(cmd.playerTag)
			player = self._gameState.getPlayerByTag(cmd.playerTag)
			opponent = self._gameState.getPlayerByTag(opponentTag)
			
			if player is None or opponent is None:
				raise(AdvanceProcessError(cmd.playerTag, "sys:wrong-player"))

			# 'j' - player joins game and provides board in encrypted form
			if cmd.cmdType == 'j' and self._gameState.status == 0:
				if player.boardCrypt is None:
					player.boardCrypt = cmd.getArgs_j()["board"]
					responsePayload = f"board p{cmd.playerTag} {player.boardCrypt}"
				# check if both players are ready then give turn to player 1
				if self._gameState.player1.boardCrypt is not None and self._gameState.player2.boardCrypt is not None:
					self.startGame()
				
			# 'm' - player move
			if cmd.cmdType == 'm':
				if  self._gameState.status != cmd.playerTag:
					raise(AdvanceProcessError(cmd.playerTag, "move:wrong-turn"))
				try:
					args = cmd.getArgs_m()
					move = BSGameMove(cmd.playerTag, args["hit"], args["x"], args["y"])
				except:
					raise(AdvanceProcessError(cmd.playerTag, "move:bad-arguments"))
				if not self.isValidMove(move):
					raise(AdvanceProcessError(cmd.playerTag, "move:invalid"))
				if opponent.board[move.my][move.mx] != 0:
					raise(AdvanceProcessError(cmd.playerTag, "move:already-played"))
				if self.isValidMove(move) and opponent.board[move.my][move.mx] == 0: # check if move is valid and also not repeating already played move
					self.markLastMoveHit(cmd.playerTag, move.wasHit) # mark previous move on player's board if it was hit
					self._gameState.moveHistory.append(move)		# add move to history
					opponent.board[move.my][move.mx] = 1	# mark move on opponent's board
					self.swithcTurn() # switch player turn
					# prepare response
					responsePayload = f"move p{cmd.playerTag} {move.wasHit} {move.mx} {move.my}"

			# 'e' - end game
			if cmd.cmdType == 'e':
				# player declares defeat
				if self._gameState.status == cmd.playerTag:
					if player.keyCrypt is None:
						self.markLastMoveHit(cmd.playerTag, 1)
						self.endGame(opponentTag)
						# reveal player key
						player.keyCrypt = cmd.getArgs_e()["key"]
						# prepare response
						responsePayload = f"end p{cmd.playerTag} defeat {player.keyCrypt}"
				# player confirming announced end game is a winner
				elif self._gameState.status == 3:
					if player.keyCrypt is None:
						# reveal player key
						player.keyCrypt = cmd.getArgs_e()["key"]
						# verify game play against revealed boards
						verifyError = verifyGame(self._gameState)
						# prepare response
						responsePayload = verifyError if verifyError is not None else f"end p{cmd.playerTag} win {player.keyCrypt}"
				else:
					raise(AdvanceProcessError(cmd.playerTag, "end:wrong-turn"))

		except AdvanceProcessError as err:
			responsePayload = err.toText()
		except Exception as ex:
			responsePayload = "error internal"
			logE(ex)

		return responsePayload
