from bs_game.console import *
from bs_game.log import *
from bs_game.log_dump import *

def dumpPlayerMsg(_gameState, cmd, response):
	logI(f"{cc.sep}===== User message >>> ====={cc.NC}")
	clrResponse = (f"{cc.res_ok}" if not response.startswith("error") else f"{cc.res_error}") if response is not None else ""
	logI(f"(Sender/Command/Response) {cc.sender}p{cmd.playerTag}{cc.NC}: {cc.msg_req}{cmd.raw}{cc.NC} -> {clrResponse}{response}{cc.NC}")
	
	if cmd.cmdType == 'j':
		if response is not None:
			logI(f"{cc.action}Player {cmd.playerTag} joins the game and provides encrypted board.{cc.NC}")
			if _gameState.status == 1:
				logI(f"{cc.action}Game starts. Player 1 is on the move.{cc.NC}")
				dumpGamePlayers(_gameState, False)

	if cmd.cmdType == 'm':
		dumpGameplayMove(_gameState, -1)
		dumpGameplayBoards(_gameState, False)

	if cmd.cmdType == 'e':
		if _gameState.result == cmd.playerTag:
			logI(f"{cc.action}Player {cmd.playerTag} confirms end game as a {cc.p_win}winner{cc.action}.{cc.NC}")
			dumpGameInfo(_gameState, False)
			dumpGameVerification(_gameState)
		else:
			logI(f"{cc.action}Player {cmd.playerTag} declares {cc.p_defeat}defeat{cc.action}.{cc.NC}")
			dumpGameplayBoards(_gameState, False)

	logI(f"{cc.sep}===== User message <<< ====={cc.NC}")
