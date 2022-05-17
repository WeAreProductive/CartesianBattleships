export default function() { return 1; }

export function BSGameRules() {
	this.boardX = 12;
	this.boardY = 12;
}

export function BSPlayer(gameRules, id) {
	this.playerId = id;
	this.board = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0))
}

export function BSGameMove(player, wasHit, mx, my) {
	this.player = player; // player tag
	this.wasHit = wasHit; // 0 - miss, 1 - hit, -1 - unknown
	this.mx = mx;
	this.my = my;
}

export function BSGameState(gameRules, gameId) {
	this.gameRules = gameRules;
	this.gameId = gameId;
	this.player1 = new BSPlayer(this.gameRules, "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266");
	this.player2 = new BSPlayer(this.gameRules, "0x70997970C51812dc3A010C7d01b50e0d17dc79C8");
	this.moveHistory = [];
	this.status = 0;
	this.result = 0;

	var playerTagMe = 1;
	var playerTagHe = 2;

	this.getPlayerByTag = (tag) => {
		if (tag == 1) return this.player1;
		if (tag == 2) return this.player2;
	}

	this.getPlayerTagMe = () => playerTagMe;
	this.getPlayerTagHe = () => playerTagHe;
	this.getPlayerMe = () => this.getPlayerByTag(playerTagMe);
	this.getPlayerHe = () => this.getPlayerByTag(playerTagHe);
}
