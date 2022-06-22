export default function() { return 1; }

export function BSGameRules() {
	this.boardX = 12;
	this.boardY = 12;
}

export function BSPlayer(gameRules, id, playerTag, boardCrypt) {
	this.playerId = id;
	this.playerTag = playerTag;
	this.boardCrypt = boardCrypt;
	this.board = new Array(gameRules.boardY).fill(0).map(() => new Array(gameRules.boardX).fill(0));

	this.isValid = () => this.playerId != null && ("" + this.playerId).trim() != "";
}

export function BSGameMove(player, wasHit, mx, my) {
	this.player = player; // player tag
	this.wasHit = wasHit; // 0 - miss, 1 - hit, -1 - unknown
	this.mx = mx;
	this.my = my;
}

export function BSGameState(gameRules, gameId, userAddress) {
	this.gameRules = gameRules;
	this.gameId = gameId;
	this.owner = "";
	this.invite = [];
	this.player1 = null; //new BSPlayer(this.gameRules, ""); // 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
	this.player2 = null; //new BSPlayer(this.gameRules, ""); // 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
	this.moveHistory = [];
	this.status = 0;
	this.result = 0;

	var playerTagMe = 1;
	var playerTagHe = 2;

	this.getPlayerByTag = (playerTag) => {
		if (playerTag == 1) return this.player1;
		if (playerTag == 2) return this.player2;
	}

	this.getPlayerTag = () => {
		if (this.isPlayerValid(1) && userAddress.toLowerCase() == this.player1.playerId.toLowerCase()) return 1;
		if (this.isPlayerValid(2) && userAddress.toLowerCase() == this.player2.playerId.toLowerCase()) return 2;
	}

	this.getPlayerTagMe = () => playerTagMe;
	this.getPlayerTagHe = () => playerTagHe;
	this.getPlayerMe = () => this.getPlayerByTag(playerTagMe);
	this.getPlayerHe = () => this.getPlayerByTag(playerTagHe);

	this.isPlayerValid = (playerTag) => {
		if (playerTag == 1 && this.player1 != null && this.player1.isValid()) return true;
		if (playerTag == 2 && this.player2 != null && this.player2.isValid()) return true;
		return false;
	}

	this.isReadyToStart = () => this.isPlayerValid(1) && this.isPlayerValid(2);

	this.addPlayer = (playerTag, address, boardCrypt) => {
		if (playerTag == 1 && this.player1 == null) {
			this.player1 = new BSPlayer(this.gameRules, address, playerTag, boardCrypt);
			return this.player1;
		}
		if (playerTag == 2 && this.player2 == null) {
			this.player2 = new BSPlayer(this.gameRules, address, playerTag, boardCrypt);
			return this.player2;
		}
	}

}
