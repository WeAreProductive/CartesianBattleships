from bs_game.log_dump import *

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
