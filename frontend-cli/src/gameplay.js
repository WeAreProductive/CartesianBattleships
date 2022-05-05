import KeyPress from "keypress";
import CliRender from "./cli-render.js";
import { BSGameRules, BSGameState } from "./gamedata.js";

export default function GamePlay() {

	var gameRules = new BSGameRules();
	var gameState = new BSGameState(gameRules, "G1");
	var cliRender = new CliRender(gameState);

	var shoot = () => {

	}

	this.start = () => {

		//board1[2][1] = 1;
		//board1[3][2] = 2;
		// board1[4][2] = 4;
		// board1[4][3] = 4;
		// board1[4][4] = 4;
		// board1[5][4] = 4;

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
