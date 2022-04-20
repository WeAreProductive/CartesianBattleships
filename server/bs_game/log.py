from bs_game.console import *
import traceback

#__logger = None

def setLogger(logger):
	global __logger
	__logger = logger

def logI(msg):
	global __logger
	__logger.info(msg)

def logE(ex):
	global __logger
	__logger.error(f"{cc.exception}Exception: {str(ex)}{cc.NC}")

def logEX(ex):
	global __logger
	traceback_str = ''.join(traceback.format_tb(ex.__traceback__))
	__logger.error(f"{cc.exception}Exception: {str(ex)}{cc.NC}")
	__logger.error(f"{cc.exception}Traceback: {traceback_str}{cc.NC}")
 