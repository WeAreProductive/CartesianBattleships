import GameProtocol from "./game-protocol.js";
import { sendCommand, getWalletAddress } from "./connect/send";

export default function GameManager(userWallet) {

	var protocol = new GameProtocol();

	var generateRandomHexString = () => {
		return Math.random().toString(16).replace(/[^a-f\d]+/g, '');		
	}

	this.gameCreate = (answers) => {
		var reqId = generateRandomHexString();

		var invite = answers.visibility == "2" ? (answers.address + "").split(",") : [];
		invite = invite.map(a => a.trim().toLowerCase());

		var sz = answers.rules == "std" ? 10 : Number(answers.boardsize);
		var boardSize = !isNaN(sz) ? [sz, sz] : [Number(answers.bsx), Number(answers.bsy)];
	
		var msg = protocol.createCommand_gameCreate(reqId, invite, boardSize[0], boardSize[1]);
		sendCommand(userWallet, msg);
	}

}