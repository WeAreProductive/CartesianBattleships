from bs_game.ConsoleColors import *
from bs_game.log import *
from bs_game.log_dump import *

cc = ConsoleColors()

def dumpPlayerMsg(_gameState, cmd, response):
	logI(f"{cc.sep}===== User message >>> ====={cc.NC}")
	clrResponse = (f"{cc.res_ok}" if not response.startswith("error") else f"{cc.res_error}") if response is not None else ""
	logI(f"Command/Response: {cc.msg_req}{cmd.raw}{cc.NC} -> {clrResponse}{response}{cc.NC}")
	
	if cmd.cmdType == 'b':
		if response is not None:
			logI(f"{cc.action}Player {cmd.playerTag} sends encrypted board.{cc.NC}")
			if _gameState.status == 1:
				logI(f"{cc.action}Game starts. Player 1 is on the move.{cc.NC}")
				dumpGamePlayers(_gameState, False)
		
	if cmd.cmdType == 'm':
		dumpGameplayMove(_gameState, -1)
		dumpGameplayBoards(_gameState, False)
		
	if cmd.cmdType == 'e':
		if _gameState.result == cmd.playerTag:
			logI(f"{cc.action}Player {cmd.playerTag} confirms end game as a {cc.p_win}winner{cc.action}.{cc.NC}")
		else:
			logI(f"{cc.action}Player {cmd.playerTag} declares {cc.p_defeat}defeat{cc.action}.{cc.NC}")
		
		
	#clrResponse = (f"{cc.Yellow}" if not response.startswith("error") else f"{cc.LightRed}") if response is not None else ""
	#logI(f">>> {cc.LightGreen}{cmd}{cc.NC} >>> {clrResponse}{response}{cc.NC}")
	#dumpGameplayMove(_gameState, -1)
	#dumpGameplayBoards(_gameState)
	##dumpGameplayMoves(_gameState)

	logI(f"{cc.sep}===== User message <<< ====={cc.NC}")
