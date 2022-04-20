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

from os import environ
import logging
import requests
from flask import Flask, request

from bs_game.utils import *
from bs_game.console import *
from bs_game.log import *
from bs_game.game_data import *
from bs_game.game_logic import *
from bs_game.game_manage import *
from bs_game.game_handler import *
from bs_game.test import *

# Setup Flask app
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
setLogger(app.logger)
# Setup Dispatcher
dispatcher_url = environ["HTTP_DISPATCHER_URL"]
logI(f"HTTP dispatcher url is {dispatcher_url}")

# Init game
_gameState = BSGameState(BSGameRules(), str(environ.get("PCBS_GAME_ID")))
_gameHandler = BSGameHandler()
# Join players
_gameState.addPlayer("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
_gameState.addPlayer("0x70997970C51812dc3A010C7d01b50e0d17dc79C8")

dumpGameInfo(_gameState)

# Run tests
if environ.get("TEST") == "1":
	BSTest(_gameState, _gameHandler).run()

# Setup route for handling input
@app.route("/advance", methods=["POST"])
def advance():
    # Get message body
	logI("")
	body = request.get_json()
	logI(f"{cc.rups_msg}Received advance request body {cc.rups_val}{body}{cc.NC}")
	# Process notice
	try:
		responsePayload = _gameHandler.processAdvance(_gameState, body)
	except Exception as ex:
		logEX(ex)
		responsePayload = ""
	if responsePayload is not None:
		response = requests.post(dispatcher_url + "/notice", json={"payload": convertStringToAsciiByteText(responsePayload)})
		logI(f"{cc.rups_msg}Added notice: status {cc.rups_val}{response.status_code}{cc.rups_msg} body {cc.rups_val}{response.content}{cc.NC}")	
	else:
		logI(f"{cc.rups_msg}Irrelevant message. Do not add notice.{cc.NC}")
	# Finalize
	response = requests.post(dispatcher_url + "/finish", json={"status": "accept"})
	logI(f"{cc.rups_msg}Received finish: status {cc.rups_val}{response.status_code}{cc.NC}")
	return "", 202

# Setup route for handling inspection
@app.route("/inspect/<payload>", methods=["GET"])
def inspect(payload):
	logI(f"{cc.rups_msg}Received inspect request: payload {payload}{cc.NC}")
	return {"reports": [{"payload": payload}]}, 200
