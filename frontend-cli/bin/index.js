#!/usr/bin/env node

import inquirer from "inquirer";
import { defaultWallets } from "../src/connect/wallets"
import Menu from "../src/menu.js";
import GameManager from "../src/game-manage.js";
import GamePlay from "../src/game-play.js";

const menu = new Menu();

var createGame = (userWallet) => {
	menu.showCreateGameMenu((answers) => {
		var gameMgr = new GameManager(userWallet);
		gameMgr.gameCreate(answers);
		joinGame(userWallet);
	});
}

var joinGame = (userWallet) => {
	menu.showJoinGameMenu((answers) => {
		var gamePlay = new GamePlay(answers.gameId, userWallet);
		gamePlay.start();
	});
}

var start = (userWallet) => {
	menu.showMainMenu(
		() => createGame(userWallet), 
		() => joinGame(userWallet)
	);
}

var startAsPlayer = () => {
	var getArgPlayer = () => process.argv.length > 2 ? process.argv[2] : null;
	var getUserWallet = (user) => defaultWallets.find((n) => n.name === user);
	
	var userWallet = getUserWallet(getArgPlayer());
	if (userWallet != null) {
		start(userWallet);
	} else {
		inquirer
		.prompt([ { 
			type: 'list', name: 'player', message: 'Select player', 
			choices: [ { name: 'Player 1', value: 'player1'}, { name: 'Player 2', value: 'player2'}] 
		}])
		.then((answers) => {
			userWallet = getUserWallet(answers.player);
			start(userWallet);
		});
	}
}

startAsPlayer();
