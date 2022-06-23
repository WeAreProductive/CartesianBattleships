from logging import log
from game_battleships.console import *
from game_battleships.log import *

def dumpGameInfo(_gameState, spacers = True):
	if _gameState is None: return
	_gameRules = _gameState._gameRules
	if spacers: logI(f"{cc.sep}===== Game Info >>> ====={cc.NC}")
	logI(f"Game ID: {cc.id}{_gameState.gameId}{cc.NC}")
	logI(f"Board size: {_gameRules.boardSizeX}x{_gameRules.boardSizeY}{cc.NC}")
	logI(f"Ships on board:{cc.NC} {_gameRules.countShip5} 5pin (Carrier), {_gameRules.countShip4} 4pin (Cruiser), {_gameRules.countShip3} 3pin (Submarine), {_gameRules.countShip2} 2pin (Frigate)")
	logI(f"Player turn timeout:{cc.NC} {_gameRules.timeoutTurn} minutes")
	logI(f"Player 1 ID: {cc.id}{_gameState.player1.Id}{cc.NC}")
	logI(f"Player 2 ID: {cc.id}{_gameState.player2.Id}{cc.NC}")
	logI(f"Game status: {_gameState.status}")
	logI(f"Game result: {_gameState.result}")
	if spacers: logI(f"{cc.sep}===== Game Info <<< ====={cc.NC}")

def dumpArray2D(arr):
	for row in arr:
		logI(row)

def dumpGamePlayers(_gameState, spacers = True):
	if _gameState is None: return
	if spacers: logI(f"{cc.sep}===== Game Players >>> ====={cc.NC}")
	logI(f"Player 1 ID: {cc.id}{_gameState.player1.Id}{cc.NC}")
	logI(f"Player 1 boardCrypt: {cc.data}{_gameState.player1.boardCrypt}{cc.NC}")
	logI(f"Player 1 keyCrypt: {cc.secret}{_gameState.player1.keyCrypt}{cc.NC}")
	logI(f"Player 2 ID: {cc.LightPurple}{_gameState.player2.Id}{cc.NC}")
	logI(f"Player 2 boardCrypt: {cc.data}{_gameState.player2.boardCrypt}{cc.NC}")
	logI(f"Player 2 keyCrypt: {cc.secret}{_gameState.player2.keyCrypt}{cc.NC}")
	if spacers: logI(f"{cc.sep}===== Game Players <<< ====={cc.NC}")

def dumpGameplayBoards(_gameState, spacers = True):
	if _gameState is None or _gameState.player1 is None or _gameState.player2 is None: return
	_gameRules = _gameState._gameRules
	
	def applyLastMove(playerTag, idy, line):
		last_move = _gameState.getLastMove()
		#return line
		if last_move is None or last_move.player == playerTag or last_move.my != idy or _gameState.status >= 3:
			return line		
		res = [ 0 for ix in range(len(line)) ]
		for idx in range(len(res)):
			res[idx] = 3 if idx == last_move.mx else line[idx]
		return res

	def formatLine(line):
		return str(line)\
			.replace(',', '').replace("0", "C0").replace("1", "C1").replace("2", "C2").replace("3", "C3")\
			.replace("C0", f"{cc.water}~{cc.NC}")\
			.replace("C1", f"{cc.miss}M{cc.NC}")\
			.replace("C2", f"{cc.hit}X{cc.NC}")\
			.replace("C3", f"{cc.shoot}*{cc.NC}")
	
	if spacers: logI(f"{cc.sep}===== Gameplay Boards >>> ====={cc.NC}")
	
	logI("Players 1 and 2 boards:")
	for idy in range(_gameRules.boardSizeY):
		rp1 = formatLine(applyLastMove(1, idy, _gameState.player1.board[idy]))
		rp2 = formatLine(applyLastMove(2, idy, _gameState.player2.board[idy]))
		logI(f"{rp1}    {rp2}")
	
	#logI("Player 1 board:")
	#dumpArray2D(_gameState.player1.board)
	#logI("Player 2 board:")
	#dumpArray2D(_gameState.player2.board)
	if spacers: logI(f"{cc.sep}===== Gameplay Boards <<< ====={cc.NC}")	

def dumpGameplayMove(_gameState, idx):
	if _gameState is None: return
	idx = (len(_gameState.moveHistory) - 1) if idx == -1 else idx
	if idx < 0: return
	val = _gameState.moveHistory[idx]
	action = f"was {cc.hit}HIT{cc.NC}    " if val.wasHit else f"was {cc.miss}missed{cc.NC} "
	if idx ==0: action = "starts game"
	logI(f"{cc.Brown}Turn {idx+1}:{cc.NC} Player {val.player} {action} and shoots at X={val.mx} Y={val.my}")

def dumpGameplayMoves(_gameState, spacers = True):
	if _gameState is None: return
	if spacers: logI(f"{cc.sep}===== Gameplay Moves >>> ====={cc.NC}")
	for idx, val in enumerate(_gameState.moveHistory):
		dumpGameplayMove(_gameState, idx)
		#wasHit = f"{cc.hit}HIT   {cc.NC}" if val.wasHit else f"{cc.miss}missed{cc.NC}"
		#logI(f"{idx}. player{val.player} was {wasHit} and shoots at X={val.mx} Y={val.my}")
	if _gameState.status == 3:
		logI(f"{cc.Brown}Turn {idx+2}:{cc.NC} Player {_gameState.getOpponentTag(_gameState.result)} was {cc.hit}HIT{cc.NC} and {cc.hit}defeated{cc.NC}.")
	if spacers: logI(f"{cc.sep}===== Gameplay Moves <<< ====={cc.NC}")

def dumpGameVerification(_gameState, spacers = True):
	if _gameState is None: return
	if spacers: logI(f"{cc.sep_verify}===== Gameplay Verification >>> ====={cc.NC}")
	
	msg_ok = f"{cc.NC}[{cc.verify_ok}OK{cc.NC}]"
	logI(f"{cc.verify_msg}Decrypting Player 1 board - {msg_ok}")
	logI(f"{cc.verify_msg}Decrypting Player 2 board - {msg_ok}")
	logI(f"{cc.verify_msg}Checking Player 1 fleet positioning - {msg_ok}")
	logI(f"{cc.verify_msg}Checking Player 2 fleet positioning - {msg_ok}")
	logI(f"{cc.verify_msg}Players moves:{cc.NC}")
	dumpGameplayMoves(_gameState, False)
	logI(f"{cc.verify_msg}Verifying players moves - {msg_ok}")
	logI(f"{cc.verify_msg}Replaying game against players positionings - {msg_ok}")
	logI(f"{cc.verify_msg}Verifying claimed game results - {msg_ok}")
	logI(f"Game was {cc.verify_ok}FAIR{cc.NC}")
	logI(f"The winner is {cc.p_win}Player {_gameState.result}{cc.NC}")

	if spacers: logI(f"{cc.sep_verify}===== Gameplay Verification <<< ====={cc.NC}")

def dumpAll(_gameState):
	dumpGameInfo(_gameState)
	dumpGamePlayers(_gameState)
	dumpGameplayBoards(_gameState)
	dumpGameplayMoves(_gameState)
