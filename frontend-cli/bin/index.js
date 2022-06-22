#!/usr/bin/env node

import inquirer from "inquirer";
import { defaultWallets } from "../src/connect/wallets"
import Menu from "../src/menu.js";
import GameManager from "../src/game-manage.js";
import GamePlay from "../src/game-play.js";
import { Receiver } from "../src/connect/receive"
import { BSGameRules, BSGameState, BSGameMove } from "../src/game-data.js";

const menu = new Menu();

var createGame = (userWallet) => {
	menu.showCreateGameMenu((answer_GameCreate) => {
		if (answer_GameCreate.confirm) {
			var gameMgr = new GameManager(userWallet);
			gameMgr.gameCreate(answer_GameCreate, (gameState) => {
				menu.askConfirm("Join now?", (answer_Join) => {
					if (answer_Join.confirm) {
						console.log("Waiting players to join ...");
						gameMgr.gameJoin(gameState, (player, isGameReadyToStart) => {
							if (player != null) {
								console.log("User with address {#a} joined as Player {#p}.".replace("{#p}", player.playerTag).replace("{#a}", player.playerId));
								if (isGameReadyToStart) {
									menu.askConfirm("Game is ready. Start now?", (answer_Start) => {
										if (answer_Start.confirm) {
											var gamePlay = new GamePlay(gameState, userWallet);
											gamePlay.start();		
										}
									});
								}
							}
						});
					}
				});
			});
		}
	});
}

var joinGame = (userWallet) => {
	menu.showJoinGameMenu((answers) => {
		var gameRules = new BSGameRules();
		var gameState = new BSGameState(gameRules, answers.gameId, getWalletAddress(userWallet));
		var gamePlay = new GamePlay(gameState, userWallet);
		gamePlay.start();
	});
}

var testReveive = (userWallet) => {
	let rcv = new Receiver(userWallet, (messages) => {
		if (messages.length > 0) {
			console.log(messages);
		}
	}).startListen();
}

var start = (userWallet) => {
	menu.showMainMenu(
		() => createGame(userWallet), 
		() => joinGame(userWallet),
		() => testReveive(userWallet)
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
