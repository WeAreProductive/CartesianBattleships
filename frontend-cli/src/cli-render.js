import Jetty from "jetty";
import CliColors from "./cli-colors.js";

const cc = new CliColors();
const cg = cc.colorsGame;
const ci = cc.colorInfoPanel;

export default function CliRender(gameState) {
	// game data
	var gameRules = gameState.gameRules;
	var boardHe = gameState.getPlayerHe().board;
	var boardMe = gameState.getPlayerMe().board;
	
	var jetty = new Jetty(process.stdout);

	// current position of player cursor
	var aim = [0, 0];
	// origins - base [y, x, size_y, size_x] coordinates from where to start drawing objects
	var origin_header = [2, 2, 5, 67];
	var origin_history = [2, 70, 15, 23];
	var origin_b1 = [8, 2];
	var origin_b2 = [8, 14 + gameRules.boardX * 2];
	var origin_reset = [15, 0];

	// ensure origin is valid
	var ensureOrigin = (origin) => origin != null ? origin : [0, 0]; 

	// move the console blinking caret to non obstructive position
	var resetCaret = () => jetty.moveTo([origin_reset[0] + gameRules.boardY, origin_reset[1]]).text("" + cg.NC);

	// clear the game screen
	this.clear = () => jetty.clear();

	// draw single line of the game board
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

	// draw all lines of the game board
	var drawBoard = (board, origin) => {
		origin = ensureOrigin(origin);
		for (var iy = 0; iy < gameRules.boardY; iy ++) {
			drawBoardLine(iy, board, origin);
		}
	}

	// format columns and rows labels - A,B,C,... / 1,2,3,...
	var formatCol = (n) => String.fromCharCode(65 + n);
	var formatRow = (n, leading) => (n < 9 && leading ? " " : "") + (n + 1);

	// draw the game board with all its elements (column and row labels, title, etc.)
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

	// draw player's aiming cursor
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

	var drawBox = (origin, style) => {
		var chars = [];
		switch (style) {
			case "single":
				chars = [' ', '─', '│', '┌', '┐', '└', '┘'];
				break;
			case "double":
				chars = [' ', '═', '║', '╔', '╗', '╚', '╝'];
				break;
			case "single-double":
				chars = [' ', '─', '║', '╓', '╖', '╙', '╜'];
				break;
			case "double-single":
				chars = [' ', '═', '│', '╒', '╕', '╘', '╛'];
				break;
			case "dash":
				chars = [' ', '┄', '┆', '┌', '┐', '└', '┘'];
				break;
			default: // std
				chars = [' ', '-', '|', '+', '+', '+', '+'];
		}
		var line1 = chars[1].repeat(origin[3] - 2);
		var line2 = chars[0].repeat(origin[3] - 2);
		var lt = chars[3] + line1 + chars[4];
		var lm = chars[2] + line2 + chars[2];
		var lb = chars[5] + line1 + chars[6];
		jetty.moveTo([origin[0], origin[1]]).text(lt);
		for (var i = 1; i < origin[2] - 1; i++)
			jetty.moveTo([origin[0] + i, origin[1]]).text(lm);
		jetty.moveTo([origin[0] + origin[2] - 1, origin[1]]).text(lb);
	}

	var drawPanelGameInfo = (origin) => {
		var playerTag = (tag) =>{
			var lbl = (tag == gameState.getPlayerTagMe()) ? ci.tag_me + "me" : ""/*ci.tag_he + "opponent"*/;
			return (tag == gameState.getPlayerTagMe()) ? ci.lbl +" (" + lbl + ci.lbl +")" : "";
		}

		drawBox(origin, "double");
		
		var lblGameId = ci.lbl + " Game ID: " + ci.game + gameState.gameId + ci.NC;
		var lblPlayer1 = ci.lbl + "Player 1: " + ci.player + gameState.player1.playerId + playerTag(1) + ci.NC;
		var lblPlayer2 = ci.lbl + "Player 2: " + ci.player + gameState.player2.playerId + playerTag(2) + ci.NC;
		jetty.moveTo([origin[0] + 1, origin[1] + 2]).text(lblGameId);
		jetty.moveTo([origin[0] + 2, origin[1] + 2]).text(lblPlayer1);
		jetty.moveTo([origin[0] + 3, origin[1] + 2]).text(lblPlayer2);
	}

	var getHistoryPaneSize = () => origin_header[2] + 4 + gameState.gameRules.boardY;
	var getHistoryPageSize = () => Math.min(gameState.moveHistory.length, getHistoryPaneSize()-2);

	var drawGameHistory = (origin) => {
		origin[2] = getHistoryPaneSize();
		var sizeH = getHistoryPageSize();
		var moves = gameState.moveHistory.slice(-sizeH);
		var offset = Math.max(gameState.moveHistory.length - sizeH, 0);
		//var size = Math.min(moves.length, sizeH);
		for (var i = 0; i < moves.length; i++) {
			var m = moves[i];
			var index = (offset + i + 1) + "";
			index = " ".repeat(Math.max(3 - index.length, 0)) + ci.ilbl + index + ". ";
			var clrP = m.player == gameState.getPlayerTagMe() ? ci.tag_me : ci.tag_he;
			var player = clrP + "P" + m.player + ": ";
			var coord = ci.m_coord + formatCol(m.mx) + formatRow(m.my, 0);
			var shoot = m.wasHit ? ci.m_hit + " HIT" : ci.m_miss + " miss";
			var lbl = index + player + coord + shoot + ci.NC;
			jetty.moveTo([origin[0] + 1 + i, origin[1] + 2]).text(ci.NC + " ".repeat(origin[2] - 1));
			jetty.moveTo([origin[0] + 1 + i, origin[1] + 2]).text(lbl);
		}
	}

	var drawPanelGameHistory = (origin) => {
		origin[2] = getHistoryPaneSize();
		drawBox(origin, "single");
		drawGameHistory(origin);
	}

	// draw entire game screen
	this.drawScreen = () => {
		jetty.clear();
		drawPanelGameInfo(origin_header);
		drawPanelGameHistory(origin_history);
		drawBoardAll(boardHe, cg.title_p2 + "Opponent's board", origin_b1);
		drawBoardAll(boardMe, cg.title_p1 + "My board", origin_b2);
		drawCursor(aim, boardHe, origin_b1);
		resetCaret();
	}

	// move player's aiming cursor by given x/y offset
	this.moveCursor = (dx, dy) => {
		// redraw old line to clear cursor
		drawBoardLine(aim[0], boardHe, origin_b1);
		// change cursor position
		aim[1] += (aim[1] + dx >= 0 && aim[1] + dx < gameRules.boardX) ? dx : 0;
		aim[0] += (aim[0] + dy >= 0 && aim[0] + dy < gameRules.boardY) ? dy : 0;
		// redraw new line
		drawBoardLine(aim[0], boardHe, origin_b1);
		drawCursor(aim, boardHe, origin_b1);
		resetCaret();
	}

}
