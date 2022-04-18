from bs_game.log import *
from bs_game.errors import *
from bs_game.game_data import *
from bs_game.game_verify import *

def processPlayerCommand(_gameState, cmd):
	responsePayload = None
	
	try:
		if not cmd.isTypeKnown():
			raise(AdvanceProcessError(cmd.playerTag, "sys:unknown-command"))
		
		opponentTag = _gameState.getOpponentTag(cmd.playerTag)
		player = _gameState.getPlayerByTag(cmd.playerTag)
		opponent = _gameState.getPlayerByTag(opponentTag)
		
		if player is None or opponent is None:
			raise(AdvanceProcessError(cmd.playerTag, "sys:wrong-player"))

		# 'b' - player game board in crypted form
		if cmd.cmdType == 'b' and _gameState.status == 0:
			if player.boardCrypt is None:
				player.boardCrypt = cmd.cmdArgs
				responsePayload = f"board p{cmd.playerTag} {player.boardCrypt}"
			# check if both players are ready then give turn to player 1
			if _gameState.player1.boardCrypt is not None and _gameState.player2.boardCrypt is not None:
				_gameState.startGame()
			
		# 'm' - player move
		if cmd.cmdType == 'm':
			if  _gameState.status != cmd.playerTag:
				raise(AdvanceProcessError(cmd.playerTag, "move:wrong-turn"))
			args = cmd.cmdArgs.split()
			if len(args) != 3:
				raise(AdvanceProcessError(cmd.playerTag, "move:bad-arguments"))
			move = BSGameMove(cmd.playerTag, args[0], args[1], args[2])
			if not _gameState.isValidMove(move):
				raise(AdvanceProcessError(cmd.playerTag, "move:invalid"))
			if opponent.board[move.mx][move.my] != 0:
				raise(AdvanceProcessError(cmd.playerTag, "move:already-played"))
			if _gameState.isValidMove(move) and opponent.board[move.mx][move.my] == 0: # check if move is valid and also not repeating already played move
				_gameState.markLastMoveHit(cmd.playerTag, move.wasHit) # mark previous move on player's board if it was hit
				_gameState.moveHistory.append(move)		# add move to history
				opponent.board[move.mx][move.my] = 1	# mark move on opponent's board
				_gameState.swithcTurn() # switch player turn
				# prepare response
				responsePayload = f"move p{cmd.playerTag} {move.wasHit} {move.mx} {move.my}"

		# 'e' - end game
		if cmd.cmdType == 'e':
			# player declares defeat
			if _gameState.status == cmd.playerTag:
				if player.keyCrypt is None:
					_gameState.markLastMoveHit(cmd.playerTag, 1)
					_gameState.endGame(opponentTag)
					# reveal player key
					player.keyCrypt = cmd.cmdArgs
					# prepare response
					responsePayload = f"end p{cmd.playerTag} defeat {player.keyCrypt}"
			# player confirming announced end game is a winner
			elif _gameState.status == 3:
				if player.keyCrypt is None:
					# reveal player key
					player.keyCrypt = cmd.cmdArgs
					# verify game play against revealed boards
					verifyError = verifyGame(_gameState)
					# prepare response
					responsePayload = verifyError if verifyError is not None else f"end p{cmd.playerTag} win {player.keyCrypt}"
			else:
				raise(AdvanceProcessError(cmd.playerTag, "end:wrong-turn"))

	except AdvanceProcessError as err:
		responsePayload = err.toText()
	except Exception as ex:
		responsePayload = "error internal"
		logE(str(ex))

	return responsePayload

