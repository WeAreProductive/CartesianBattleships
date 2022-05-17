//import { BSGameRules, BSGameState, BSGameMove } from "./game-data.js";

export default function GameProtocol() {

	this.createCommand_move = (move) => {
		return "m: " + move.wasHit + " " + move.mx + " " + move.my;
	}

	this.createCommand_gameBegin = (crypt_board) => {
		return "b: " + crypt_board;
	}

	this.createCommand_gameEnd = (key) => {
		return "e: " + key;
	}

}