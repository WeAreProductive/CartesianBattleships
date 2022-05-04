import KeyPress from "keypress";
import CliRender from "./cli-render.js";

export default function GamePlay() {

	var gameRules = {
		boardX: 8,
		boardY: 8,
	};

	var board1 = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0));
	var board2 = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0));

	var cliRender = new CliRender(gameRules, board1, board2);

	this.start = () => {

		board1[2][1] = 1;
		board1[3][2] = 2;
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
			}
		});
		process.stdin.setRawMode(true);
		process.stdin.resume();

	}

}
