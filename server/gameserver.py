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
from bs_game.game_handler import *
from bs_game.errors import *
from bs_game.test import *

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

dispatcher_url = environ["HTTP_DISPATCHER_URL"]
app.logger.info(f"HTTP dispatcher url is {dispatcher_url}")

setLogger(app.logger)
cc = ConsoleColors()

_gameRules = BSGameRules()
_gameState = BSGameState(_gameRules, str(environ.get("PCBS_GAME_ID")))
_gameHandler = BSGameHandler()
#_gameState.addPlayer(environ.get("CBS_USER_ID_1"))
#_gameState.addPlayer(environ.get("CBS_USER_ID_2"))
#_gameState.addPlayer("111")
#_gameState.addPlayer("222")
_gameState.addPlayer("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
_gameState.addPlayer("0x70997970C51812dc3A010C7d01b50e0d17dc79C8")



dumpGameInfo(_gameState)

#BSTest(_gameState, _gameHandler).run()



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
	
	responsePayload = _gameHandler.processAdvance(_gameState, body)
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

