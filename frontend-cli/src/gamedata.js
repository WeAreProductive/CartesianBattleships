export default function() { return 1; }

export function BSGameRules() {
	this.boardX = 20;
	this.boardY = 20;
}

export function BSPlayer(gameRules, id) {
	//console.log(gameRules);
	this.playerId = id;
	this.board = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0))
}

export function BSGameMove(player, wasHit, mx, my) {
	this.player = player;
	this.wasHit = wasHit;
	this.mx = mx;
	this.my = my;
}

export function BSGameState(gameRules, gameId) {
	this.gameRules = gameRules;
	console.log(gameRules);
	this.gameId = gameId;
	this.player1 = new BSPlayer(this.gameRules);
	this.player2 = new BSPlayer(this.gameRules);
	this.moveHistory = [];
	this.status = 0;
	this.result = 0;

	var playerTagMe = 1;
	var playerTagHe = 2;

	this.getPlayerByTag = (tag) => {
		if (tag == 1) return this.player1;
		if (tag == 2) return this.player2;
	}

	this.getPlayerMe = () => this.getPlayerByTag(playerTagMe);
	this.getPlayerHe = () => this.getPlayerByTag(playerTagHe);
}
