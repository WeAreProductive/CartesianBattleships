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

from game_battleships.utils import *
from game_battleships.console import *
from game_battleships.log import *
from game_battleships.game_data import *
from game_battleships.game_logic import *
from game_battleships.game_manage import *
from game_battleships.game_handler import *
from game_battleships.test import *

# Setup logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
setLogger(logger)

# Setup Rollup server
rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logI(f"HTTP rollup_server url is {rollup_server}")

printLogo()

# Init
_gameManager = BSGameManager()
_gameHandler = BSGameHandler()

# Run tests if specified
BSTest(_gameManager, _gameHandler).run(environ.get("TEST"))

# Setup handlers
def handle_advance(data):
	logI("")
	logI(f"{cc.rups_msg}Received advance request body {cc.rups_val}{data}{cc.NC}")
	try:
		status = "accept"
		target = "notice"
		responsePayload = _gameHandler.processAdvance(_gameManager, data)
	except Exception as ex:
		status = "reject"
		target = "report"
		responsePayload = formatEX(ex)
		logEX(ex)
	if responsePayload is not None:
		response = requests.post(rollup_server + "/" + target, json={"payload": convertStringToHexBytes(responsePayload)})
		logI(f"{cc.rups_msg}Received {target} status {cc.rups_val}{response.status_code}{cc.rups_msg} body {cc.rups_val}{response.content}{cc.NC}")	
	else:
		logI(f"{cc.rups_msg}Irrelevant message. Do not add notice.{cc.NC}")
	return status

def handle_inspect(data):
	payload = convertHexBytesToString(getKeySafe(data, "payload", ""))
	logI(f"{cc.rups_msg}Received inspect request data payload: {payload}{cc.NC}")
	responsePayload = _gameHandler.processInspect(_gameManager, payload)
	response = requests.post(rollup_server + "/report", json={"payload": convertStringToHexBytes(responsePayload)})
	#logI(f'payload: {convertHexBytesToString(getKeySafe(data, "payload", ))}')
	logI(f"{cc.rups_msg}Received report status {response.status_code}{cc.NC}")
	return "accept"

handlers = {
	"advance_state": handle_advance,
	"inspect_state": handle_inspect,
}

finish = {"status": "accept"}
rollup_address = None

while True:
	try:
		response = requests.post(rollup_server + "/finish", json=finish)
		if response.status_code != 202:
			rollup_request = response.json()
			logI(rollup_request)
			data = getKeySafe(rollup_request, "data")
			if data is not None:			
				metadata = getKeySafe(data, "metadata")
				#metadata = rollup_request["data"]["metadata"]
				if metadata is not None and metadata["epoch_index"] == 0 and metadata["input_index"] == 0:
					rollup_address = metadata["msg_sender"]
					logI(f"Captured rollup address: {rollup_address}")
					continue
				handler = handlers[rollup_request["request_type"]]
				finish["status"] = handler(data)
      
	except KeyboardInterrupt as ex_ki:
		logI(f"{cc.exception}Interrupted by user.{cc.NC}")
		break
	except Exception as ex:
		logEX(ex)
		logI(response)
