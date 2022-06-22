import { BSGameRules, BSGameState, BSGameMove } from "./game-data.js";

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

	this.parseResponse_gameCreate = (cmd, userAddress) => {
		var gameRules = new BSGameRules();
		gameRules.boardX = parseInt(cmd.arg.rules.size[0]);
		gameRules.boardY = parseInt(cmd.arg.rules.size[1]);

		var gameState = new BSGameState(gameRules, cmd.gid, userAddress);
		gameState.owner = cmd.sys.owner;
		gameState.invite = cmd.sys.invite;
	
		return gameState;
	}

	this.parseResponse_gameJoin = (cmd, gameState) => {
		// TODO: for now empty invite (meaning "anyone") will not work, player 2 must be invited with address
		let sender = ""; // TODO: playerId should be taken from sender
		let playerTag = parseInt(cmd.p);
		if (playerTag == 1) sender = gameState.owner;
		if (playerTag == 2) sender = gameState.invite.length > 0 ? gameState.invite[0] : "";
		let player = gameState.addPlayer(playerTag, sender, cmd.arg.board);
		let isGameReadyToStart = gameState.isReadyToStart();
		return { player: player, isGameReadyToStart: isGameReadyToStart };
	}

}