import GameProtocol from "./game-protocol.js";
import { sendCommand, getWalletAddress } from "./connect/send";
import { Receiver } from "./connect/receive"

export default function GameManager(userWallet) {

	const protocol = new GameProtocol();

	const generateRandomHexString = () => Math.random().toString(16).replace(/[^a-f\d]+/g, '');

	this.gameCreate = (answers, onCreate, onError) => {
		let reqId = generateRandomHexString();

		let invite = answers.visibility == "2" ? (answers.address + "").split(",") : [];
		invite = invite.map(a => a.trim().toLowerCase());

		let sz = answers.rules == "std" ? 10 : Number(answers.boardsize);
		let boardSize = !isNaN(sz) ? [sz, sz] : [Number(answers.bsx), Number(answers.bsy)];
	
		// prepare and send command
		let msg = protocol.createCommand_gameCreate(reqId, invite, boardSize[0], boardSize[1]);
		sendCommand(userWallet, msg);
		

		// wait for response
		console.log("Creating game ... (please wait)");
		let rcv = new Receiver(userWallet)
			.filter((n) => n.sys != null && n.sys.reqId == reqId) 
			.onReceive((messages) => {
				rcv.stopListen();
				let gameState = protocol.parseResponse_gameCreate(messages[0], getWalletAddress(userWallet));
				console.log("Game created (Game ID: {#gid})".replace("{#gid}", gameState.gameId));
				onCreate(gameState);
			})
			.startListen();
	}

	this.gameJoin = (gameState, onJoin) => {
		// prepare and send command
		let msg = protocol.createCommand_gameJoin(gameState.gameId, "****");
		sendCommand(userWallet, msg);

		// wait for response
		let rcv = new Receiver(userWallet)
			.filter((n) => n.gid == gameState.gameId && n.cmd == "j")
			.onReceive((messages) => {
				messages.forEach(msg => {
					let join = protocol.parseResponse_gameJoin(msg, gameState);
					console.log(join);
					if (join.isGameReadyToStart) {
						rcv.stopListen();
					}
					onJoin(join.player, join.isGameReadyToStart);
				});
			})
			.startListen();

	}

}