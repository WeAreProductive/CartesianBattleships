# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
from os import environ
import logging
import requests
from flask import Flask, request

from bs_game.utils import *
from bs_game.ConsoleColors import *
from bs_game.log import *
from bs_game.log_dump import *
from bs_game.log_flow import *
from bs_game.game_data import *
from bs_game.game_logic import *
from bs_game.game_manage import *
from bs_game.errors import *
from bs_game.protocol_text import *

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

dispatcher_url = environ["HTTP_DISPATCHER_URL"]
app.logger.info(f"HTTP dispatcher url is {dispatcher_url}")

setLogger(app.logger)
cc = ConsoleColors()

_gameRules = BSGameRules()
_gameState = BSGameState(_gameRules, str(environ.get("PCBS_GAME_ID")))


def processAdvance(payload):
	responsePayload = None
	cmd = Command(payload)
	if cmd.isSys():
		responsePayload = processSystemCommand(_gameState, cmd)
	else:
		responsePayload = processPlayerCommand(_gameState, cmd)	
		dumpPlayerMsg(_gameState, cmd, responsePayload)		
	return responsePayload


dumpGameInfo(_gameState)
	

def test1():
	def send(cmd):
		logI("")
		response = processAdvance(cmd)
		#dumpPlayerMsg(_gameState, cmd, response)
		
		#clrResponse = (f"{cc.Yellow}" if not response.startswith("error") else f"{cc.LightRed}") if response is not None else ""
		#logI(f">>> {cc.LightGreen}{cmd}{cc.NC} >>> {clrResponse}{response}{cc.NC}")
		#dumpGameplayMove(_gameState, -1)
		#dumpGameplayBoards(_gameState)
		##dumpGameplayMoves(_gameState)

		
	send("p1 b: xxx123")
	send("p1 b: xxx123")
	send("p2 b: ccc123")
	send("p2 b: ccc123")


	#send("p3 m: 0 1 1")
	
	#send("p1 x: xxx")
	
	send("p1 m: 0 1 1")
	send("p1 m: 0 1 0")
	send("p2 m: 1 2 2")
	send("p1 m: 0 3 3")
	send("p2 m: 0 0 0")
	send("p1 m: 1 4 4")
	
	#dumpGameplayMoves(_gameState)
	
	#send("p1 e: rrr111")
	#send("p1 e: rrr111")

	send("p2 e: rrr111")
	#send("p2 e: rrr111")
	#dumpGamePlayers(_gameState)
	send("p1 e: rrr111")
	#send("p1 e: rrr111")
	#dumpGamePlayers(_gameState)

	#logI(f">>>>>>>>>> player turn {_gameState.status}")
	#processAdvance("p2 m: 0 4 4")
	#dumpGameplayBoards(_gameState)
	


test1()
#dumpGameplayBoards(_gameState)


@app.route("/advance", methods=["POST"])
def advance():
	body = request.get_json()
	logI(f"Received advance request body {body}")

	#logI("Game ID: " + str(cs_game_id))
	#logI(f"Game ID: {_gameState.gameId}")
	

	logI(body["payload"])
	#logI(str(body["payload"]))
	#logI(str(body["payload"]).replace("0x", ""))
	#logI(bytearray.fromhex(str(body["payload"]).replace("0x", "")).decode())
	payload = convertAsciiByteTextToString(body["payload"])
	try:
		sender = str(body["metadata"]["msg_sender"])
	except:
		sender = "error"
	logI(payload)
	logI(f"Sender: {sender}")
	
	responsePayload = processAdvance(payload)
	if responsePayload is not None:
		logI("Adding notice")
		response = requests.post(dispatcher_url + "/notice", json={"payload": convertStringToAsciiByteText(responsePayload)})
		logI(f"Received notice status {response.status_code} body {response.content}")	
	else:
		logI("Irrelevant message. Do not add notice.")
	

	#if (payload.startswith("m:")):
	#	if _gameState.status != 1:
	#		_gameState.status = 1
	#	else:
	#		_gameState.status = 2
	#	
	#	logI("status: " + str(_gameState.status))
	#		
	#	logI("Adding notice")
	#	response = requests.post(dispatcher_url + "/notice", json={"payload": body["payload"]})
	#	logI(f"Received notice status {response.status_code} body {response.content}")
	#else:
	#	logI("Invalid message! Do not add notice!")


	logI("Finishing")
	response = requests.post(dispatcher_url + "/finish", json={"status": "accept"})
	logI(f"Received finish status {response.status_code}")
	return "", 202


@app.route("/inspect/<payload>", methods=["GET"])
def inspect(payload):
	logI(f"Received inspect request payload {payload}")
	return {"reports": [{"payload": payload}]}, 200

