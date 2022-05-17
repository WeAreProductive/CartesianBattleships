import KeyPress from "keypress";
import CliRender from "./cli-render.js";
import { BSGameRules, BSGameState, BSGameMove } from "./game-data.js";
import { sendCommand } from "./connect/send";

export default function GamePlay() {

	var gameRules = new BSGameRules();
	var gameState = new BSGameState(gameRules, "G1");
	var cliRender = new CliRender(gameState);

	var shoot = () => {
		sendCommand({ network: "localhost", message: "shoot 2"});
	}

	var test = () => {
		var bH = gameState.getPlayerHe().board;
		bH[2][1] = 1;
		bH[3][2] = 2;
		// bH[4][2] = 4;
		// bH[4][3] = 4;
		// bH[4][4] = 4;
		// bH[5][4] = 4;

		// for (var i = 0; i < 30; i++) {
		// 	gameState.moveHistory.push(new BSGameMove(1, 0, 2, i));
		// 	gameState.moveHistory.push(new BSGameMove(2, 0, 3, i));
		// }

		gameState.moveHistory.push(new BSGameMove(1, 0, 2, 3));
		gameState.moveHistory.push(new BSGameMove(2, 0, 3, 4));
		gameState.moveHistory.push(new BSGameMove(1, 0, 3, 2));
		gameState.moveHistory.push(new BSGameMove(2, 1, 4, 5));
		gameState.moveHistory.push(new BSGameMove(1, 1, 1, 4));
		gameState.moveHistory.push(new BSGameMove(2, -1, 4, 2));
	}

	this.start = () => {
		test();

		cliRender.drawScreen();

		KeyPress(process.stdin);
		process.stdin.on('keypress', (ch, key) => {
			//console.log('got "keypress"', key);
			if (key) {
				if (key.ctrl && key.name == 'c') {
					process.stdin.pause();
				}
				if (key.name =='left') {
					cliRender.moveCursor(-1, 0);
				}
				if (key.name =='right') {
					cliRender.moveCursor(+1, 0);
				}
				if (key.name =='up') {
					cliRender.moveCursor(0, -1);
				}
				if (key.name =='down') {
					cliRender.moveCursor(0, +1);
				}
				if (key.name =='return') {
					shoot();
				}
			}
		});
		process.stdin.setRawMode(true);
		process.stdin.resume();

	}

}
