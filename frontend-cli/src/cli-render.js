import Jetty from "jetty";
import CliColors from "./cli-colors.js";

const cc = new CliColors();
const cg = cc.colorsGame;

export default function CliRender(gameRules, board1, board2) {
	var jetty = new Jetty(process.stdout);

	var aim = [0, 0];

	var origing_b1 = [2, 2];
	var origing_b2 = [2, 10 + 4 + gameRules.boardX * 2];

	// ensure origin is valid
	var ensureOrigin = (origin) => origin != null ? origin : [0, 0]; 

	var resetCaret = () => {
		jetty.moveTo([gameRules.boardY + 7, 0]).text("" + cg.NC);
	}

	this.clear = () => jetty.clear();

	var drawBoardLine = (iy, board, origin) => {
		origin = ensureOrigin(origin);
		// single numbers might cause replace conflicts, so add "C" prefix to prevent it
		var line = "C" + board[iy].join(" C");
		line = line
			.replaceAll("C0", cg.water + "~" + cg.NC)	// water
			.replaceAll("C1", cg.miss + "M" + cg.NC)	// hit missed
			.replaceAll("C2", cg.hit + "X" + cg.NC)		// hit on target
			.replaceAll("C3", cg.hit + "V" + cg.NC)		//
			.replaceAll("C4", cg.ship + "#" + cg.NC);	// player ship
		line = cg.grid + "[" + line + cg.grid + "]";
		jetty.moveTo([iy + origin[0] + 2, origin[1] + 3]).text(line);
	}

	var drawBoard = (board, origin) => {
		origin = ensureOrigin(origin);
		for (var iy = 0; iy < gameRules.boardY; iy ++) {
			drawBoardLine(iy, board, origin);
		}
	}

	// format columns and rows labels - A,B,C,... / 1,2,3,...
	var formatCol = (n) => String.fromCharCode(65 + n);
	var formatRow = (n, leading) => (n < 9 && leading ? " " : "") + (n + 1);

	var drawBoardAll = (board, title, origin) => {
		origin = ensureOrigin(origin);
		// draw columns and rows labels
		var lblCX = Array.from({length: gameRules.boardX}, (_, i) => formatCol(i));
		var lblCY = Array.from({length: gameRules.boardY}, (_, i) => formatRow(i, 1));
		jetty.moveTo([origin[0] + 1, origin[1] + 4]).text(cg.NC + cg.ilbl + lblCX.join(" ") + cg.NC);
		for (var iy = 0; iy < gameRules.boardY; iy ++) {
			jetty.moveTo([iy + origin[0] + 2, origin[1]]).text(cg.ilbl + lblCY[iy] + cg.NC);
		}
		// draw board title
		jetty.moveTo([origin[0], origin[1] + 3]).text(title + cg.NC);
		//draw board
		drawBoard(board, origin);
	}

	var drawCursor = (pos, board, origin) => {
		origin = ensureOrigin(origin);
		// draw cursor
		var cursor = "";
		var val = board[pos[0]][pos[1]];
		if (val == 0) cursor = cg.c_water + "O";
		if (val == 1) cursor = cg.c_miss + "M";
		if (val == 2) cursor = cg.c_hit + "X";
		jetty.moveTo([pos[0] + origin[0] + 2, pos[1] * 2 + origin[1] + 4]).text(cursor + cg.NC);
		// draw coordinates
		var coords = cg.coords + formatCol(pos[1]) + formatRow(pos[0], 0) + cg.NC + "    ";
		jetty.moveTo([origin[0] + gameRules.boardY + 2, origin[1] + 4]).text(coords);
	}

	this.drawScreen = () => {
		jetty.clear();
		drawBoardAll(board1, cg.title_p2 + "Opponent's board", origing_b1);
		drawBoardAll(board2, cg.title_p1 + "My board", origing_b2);
		drawCursor(aim, board1, origing_b1);
		resetCaret();
	}

	this.moveCursor = (dx, dy) => {
		// redraw old line to clear cursor
		drawBoardLine(aim[0], board1, origing_b1);
		// change cursor position
		aim[1] += (aim[1] + dx >= 0 && aim[1] + dx < gameRules.boardX) ? dx : 0;
		aim[0] += (aim[0] + dy >= 0 && aim[0] + dy < gameRules.boardY) ? dy : 0;
		// redraw new line
		drawBoardLine(aim[0], board1, origing_b1);
		drawCursor(aim, board1, origing_b1);
		resetCaret();
	}

}
