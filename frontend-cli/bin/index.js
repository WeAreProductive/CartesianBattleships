#!/usr/bin/env node

import inquirer from "inquirer";
import { defaultWallets } from "../src/connect/wallets"
import Menu from "../src/menu.js";
import GamePlay from "../src/game-play.js";

var createGame = (userWallet) => {
	joinGame(userWallet);
}

var joinGame = (userWallet) => {
	var gamePlay = new GamePlay(userWallet);
	gamePlay.start();
}

var start = (userWallet) => {
	var menu = new Menu();
	menu.showMainMenu(
		() => createGame(userWallet), 
		() => joinGame(userWallet)
	);
}

var startAsPlayer = () => {
	var getArgPlayer = () => process.argv.length > 2 ? process.argv[2] : null;
	var getPlayer = (player) => defaultWallets.find((n) => n.name === player);
	var getPlayerVal = (label) => label.replace(" ", "").toLowerCase();
	
	var userWallet = getPlayer(getArgPlayer());
	if (userWallet != null) {
		start(userWallet);
	} else {
		inquirer
		.prompt([ { type: 'list', name: 'player', message: 'Select player', choices: ['Player 1', 'Player 2'] } ])
		.then((answers) => {
			userWallet = getPlayer(getPlayerVal(answers.player));
			start(userWallet);
		});
	}
}

startAsPlayer();
