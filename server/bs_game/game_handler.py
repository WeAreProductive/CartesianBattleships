from bs_game.utils import *
from bs_game.log_flow import *
from bs_game.log_dump import *
from bs_game.game_logic import *
from bs_game.protocol_text import *

class BSGameHandler:

	def processAdvance(self, _gameState, body):
		try:
			payload = convertAsciiByteTextToString(body["payload"])
		except:
			payload = ""
		try:
			sender = str(body["metadata"]["msg_sender"]).lower()
		except:
			sender = ""

		responsePayload = None
		cmd = Command(_gameState.getPlayerTagById(sender), payload)
		if cmd.isSys():
			responsePayload = self.processSystemCommand(_gameState, cmd.cmdArgs)
		else:
			responsePayload = processPlayerCommand(_gameState, cmd)	
			dumpPlayerMsg(_gameState, cmd, responsePayload)		
		return responsePayload


	def processSystemCommand(_gameState, cmd):
		if (cmd == "dump-info"):
			dumpGameInfo(_gameState)
		if (cmd == "dump-players"):
			dumpGamePlayers(_gameState)
		if (cmd == "dump-boards"):
			dumpGameplayBoards(_gameState)
		if (cmd == "dump-moves"):
			dumpGameplayMoves(_gameState)
		if (cmd == "dump-all"):
			dumpAll()
		#if (cmd == "reset-game"):
		#	_gameState.reset()
			#_gameState = BSGameState(_gameState)
		#if (cmd == "quit"):
		#	logI("Shutdown!")
		#	os.system("shutdown")