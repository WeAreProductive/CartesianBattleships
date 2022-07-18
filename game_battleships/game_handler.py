from game_battleships.utils import *
from game_battleships.log_flow import *
from game_battleships.log_dump import *
from game_battleships.game_logic import *
#from game_battleships.protocol_text import *
from game_battleships.protocol_json import *

class BSMessageData:
	def __init__(self, data):
		self.payload = convertHexBytesToString(getKeySafe(data, "payload", ""))
		self.sender = str(getKeySafe(data, ["metadata", "msg_sender"], "")).lower()
		self.epoch_index = convertToInt(getKeySafe(data, ["metadata", "epoch_index"]))
		self.input_index = convertToInt(getKeySafe(data, ["metadata", "input_index"]))

class BSGameHandler:

	def processAdvance(self, _gameManager, data):
		md = BSMessageData(data)
	
		responsePayload = None
		try:
			cmd = Command(md)

			gameState = _gameManager.getGame(cmd.gameId)
			cmd.syncPlayerTag(gameState.getPlayerTagById(md.sender) if not gameState is None else 0)

			handlerClass = cmd.getHandlerClass()
			if handlerClass == "debug":
				pass
				# responsePayload = self.processSystemCommand(gameState, cmd.cmdArgs)
			elif handlerClass == "manager":
				responsePayload = _gameManager.processPlayerCommand(cmd)
			elif handlerClass == "game":
				responsePayload = BSGameLogic(gameState).processPlayerCommand(cmd)	
			else:
				raise(AdvanceProcessError("sys", "unknown-command"))

		except AdvanceProcessError as err:
			responsePayload = cmd.getResponse_error(err.toText())
		except Exception as ex:
			responsePayload = cmd.getResponse_error("internal")
			logEX(ex)

		dumpPlayerMsg(gameState, cmd, responsePayload)
		return responsePayload


	def processSystemCommand(self, _gameState, cmd):
		if (cmd == "dump-info"):
			dumpGameInfo(_gameState)
		if (cmd == "dump-players"):
			dumpGamePlayers(_gameState)
		if (cmd == "dump-boards"):
			dumpGameplayBoards(_gameState)
		if (cmd == "dump-moves"):
			dumpGameplayMoves(_gameState)
		if (cmd == "dump-all"):
			dumpAll(_gameState)
		#if (cmd == "reset-game"):
		#	_gameState.reset()
			#_gameState = BSGameState(_gameState)
		#if (cmd == "quit"):
		#	logI("Shutdown!")
		#	os.system("shutdown")