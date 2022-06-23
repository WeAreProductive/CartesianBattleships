from game_battleships.console import *
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

def printLogo():
	logI(f"")
	logI(f"")
	logI(f"  {cc.a8}   Cartesi   {cc.NC}                         {cc.a5}.) {cc.a3}|{cc.NC}")
	logI(f"  {cc.a8} Battleships {cc.NC}                      {cc.a3}____|_|_{cc.a5}(.{cc.NC}")
	logI(f"                                     {cc.a3}_\\______|{cc.NC}")
	logI(f"                                   {cc.a3}_/________|_{cc.a4}//{cc.a3}_{cc.NC}")
	logI(f"               {cc.a3}_______            /   {cc.a6}<<<{cc.a3}         |{cc.NC}")
	logI(f"               {cc.a3}\ {cc.a5}...  {cc.a3}\\___{cc.a4}[\\\\\\]{cc.a3}__/_________{cc.a4}[///]{cc.a3}__|___{cc.a7}F{cc.NC}")
	logI(f"   {cc.a1}__{cc.a2}4{cc.a1}__        {cc.a3}\\                                     |{cc.NC}")
	logI(f"   {cc.a1}\\   /{cc.NC}         {cc.a3}\\   V            {cc.a6}<<<      <<<        {cc.a3}/{cc.NC}")
	logI(f"{cc.a0}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{cc.NC}")
	logI(f"{cc.a0}~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~{cc.NC}")
	logI(f"{cc.a0} ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ {cc.NC}")
	logI(f"")
	logI(f"")
