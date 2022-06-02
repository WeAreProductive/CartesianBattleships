//import { BSGameRules, BSGameState, BSGameMove } from "./game-data.js";

export default function GameProtocol() {

	this.createCommand_gameCreate = (reqId, invite, rule_sizeX, rule_sizeY) => {
		var cmd = {
			cmd: "c",
			sys: {
				reqId: reqId,
				invite: invite
			},
			arg: { rules: { size: [rule_sizeX, rule_sizeY] } }
		};
		return JSON.stringify(cmd);
		//return "b: " + crypt_board;
	}

	this.createCommand_gameJoin = (gameId, crypt_board) => {
		var cmd = {
			gid: gameId, cmd: "j",
			arg: { board: crypt_board }
		};
		return JSON.stringify(cmd);
		//return "b: " + crypt_board;
	}

	this.createCommand_move = (gameId, move) => {
		var cmd = {
			gid: gameId, cmd: "m",
			arg: {
				hit: move.wasHit,
				shot: [move.mx, move.my]
			}
		};
		return JSON.stringify(cmd);
		//return "m: " + move.wasHit + " " + move.mx + " " + move.my;
	}

	this.createCommand_gameEnd = (gameId, key) => {
		var cmd = {
			gid: gameId, cmd: "e",
			arg: { key: key }
		};
		return JSON.stringify(cmd);		
		//return "e: " + key;
	}

}