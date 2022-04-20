from bs_game.console import *

cc = ConsoleColors()

#__logger = None

def setLogger(logger):
	global __logger
	__logger = logger

def logI(msg):
	global __logger
	__logger.info(msg)

def logE(msg):
	global __logger
	__logger.error(f"{cc.exception}Exception: {str(msg)}{cc.NC}")
