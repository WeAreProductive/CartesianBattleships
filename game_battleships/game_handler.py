from game_battleships.utils import *
from game_battleships.log_flow import *
from game_battleships.log_dump import *
from game_battleships.game_logic import *
#from game_battleships.protocol_text import *
from game_battleships.protocol_json import *

class BSGameHandler:

	def processAdvance(self, _gameManager, body):
		try:
			payload = convertAsciiByteTextToString(body["payload"])
		except:
			payload = ""
		try:
			sender = str(body["metadata"]["msg_sender"]).lower()
		except:
			sender = ""

		responsePayload = None
		try:
			cmd = Command(sender, payload)

			gameState = _gameManager.getGame(cmd.gameId)
			cmd.syncPlayerTag(gameState.getPlayerTagById(sender) if not gameState is None else 0)

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