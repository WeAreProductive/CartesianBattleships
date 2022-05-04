import Jetty from "jetty";
import KeyPress from "keypress";
import CliColors from "./cli-colors.js";

const cc = new CliColors();
const cg = cc.colorsGame;

export default function GamePlay() {

	var jetty = new Jetty(process.stdout);

	var gameRules = {
		boardX: 8,
		boardY: 8,
	};

	var aim = [0, 0];

	var origing_b1 = [2, 2];
	var origing_b2 = [2, 10 + 4 + gameRules.boardX * 2];

	var board1 = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0));
	var board2 = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0));

	var ensureOrigin = (origin) => {
		 return origin != null ? origin : [0, 0];
	}

	var drawBoardLine = (iy, board, origin) => {
		origin = ensureOrigin(origin);
		var line = "C" + board[iy].join(" C");
		line = line
			.replaceAll("C0", cg.water + "~" + cg.NC)
			.replaceAll("C1", cg.miss + "M" + cg.NC)
			.replaceAll("C2", cg.hit + "X" + cg.NC)
			.replaceAll("C3", cg.hit + "V" + cg.NC)
			.replaceAll("C4", cg.ship + "#" + cg.NC);
		line = cg.grid + " [" + line + cg.grid + "]";
		jetty.moveTo([iy + origin[0] + 1, origin[1] + 1]).text(line);
	}

	var drawBoard = (board, origin) => {
		origin = ensureOrigin(origin);
		for (var iy = 0; iy < gameRules.boardY; iy ++) {
			drawBoardLine(iy, board, origin);
		}
	}

	var drawBoardAll = (board, origin) => {
		origin = ensureOrigin(origin);
		var formatIX = (n) => {
			var i = ("" + (n + 1));
			return i[i.length - 1];
		}
		var formatIY = (n) => {
			return String.fromCharCode(65 + n);
		}
		var lblCX = Array.from({length: gameRules.boardX}, (_, i) => formatIX(i));
		var lblCY = Array.from({length: gameRules.boardY}, (_, i) => formatIY(i));
		jetty.moveTo([origin[0], origin[1] + 3]).text(cg.NC + cg.ilbl + lblCX.join(" ") + cg.NC);
		for (var iy = 0; iy < gameRules.boardY; iy ++) {
			jetty.moveTo([iy + origin[0] + 1, origin[1]]).text(cg.ilbl + lblCY[iy] + cg.NC);
		}
		drawBoard(board, origin);
	}

	var drawCursor = (pos, board, origin) => {
		var cursor = "";
		var val = board[pos[0]][pos[1]];
		if (val == 0) cursor = cg.c_water + "O";
		if (val == 1) cursor = cg.c_miss + "M";
		if (val == 2) cursor = cg.c_hit + "X";
		jetty.moveTo([pos[0] + origin[0] + 1, pos[1] * 2 + origin[1] + 3]).text(cursor);
	}

	var drawScreen = () => {

		jetty.clear();

		drawBoardAll(board1, origing_b1);
		drawBoardAll(board2, origing_b2);
		drawCursor(aim, board1, origing_b1);

		//showCursor([2, 1], board1, origing_b1);
		//showCursor([3, 2], board1, origing_b1);
		//showCursor([4, 3], board1, origing_b1);

		//console.log(board);

		// jetty.moveTo([5, 5]).text("\x1b[92m[\x1b[0m");
		// jetty.lineUp();
		// jetty.lineUp();
		// jetty.text("]");
		resetCaret();
	}

	var moveCursor = (dx, dy) => {
		drawBoardLine(aim[0], board1, origing_b1);
		aim[1] += (aim[1] + dx >= 0 && aim[1] + dx < gameRules.boardX) ? dx : 0;
		aim[0] += (aim[0] + dy >= 0 && aim[0] + dy < gameRules.boardY) ? dy : 0;
		drawBoardLine(aim[0], board1, origing_b1);
		drawCursor(aim, board1, origing_b1);
		resetCaret();
	}

	var resetCaret = () => {
		jetty.moveTo([15, 0]).text("" + cg.NC);
	}

	this.start = () => {

		board1[2][1] = 1;
		board1[3][2] = 2;
		// board1[4][2] = 4;
		// board1[4][3] = 4;
		// board1[4][4] = 4;
		// board1[5][4] = 4;

		drawScreen();
		

		var redraw = () => {
			//drawScreen();
			drawBoard(board1, origing_b1);
			drawCursor(aim, board1, origing_b1);
			resetCaret();
		}

		KeyPress(process.stdin);

		process.stdin.on('keypress', (ch, key) => {
			//console.log('got "keypress"', key);
			if (key) {
				if (key.ctrl && key.name == 'c') {
					process.stdin.pause();
				}
				if (key.name =='left') {
					moveCursor(-1, 0);
				}
				if (key.name =='right') {
					moveCursor(+1, 0);
				}
				if (key.name =='up') {
					moveCursor(0, -1);
				}
				if (key.name =='down') {
					moveCursor(0, +1);
				}
			}
		});

		process.stdin.setRawMode(true);
		process.stdin.resume();

	}

}
