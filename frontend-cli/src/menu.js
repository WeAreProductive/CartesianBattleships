import TerminalMenu from "simple-terminal-menu";
import inquirer from "inquirer";
import CliColors from "./cli-colors.js";

export default function Menu() {

	var linesLogo = [];

	var printLogo = () => {
		const cl = new CliColors().colorsLogo;
		var addLine = (line) => {
			for (var key in cl) {
				var ph = "{cc." + key + "}";
				line = line.replaceAll(ph, cl[key]);
			}
			linesLogo.push(line);		
		}

		linesLogo = [];
		addLine("");
		addLine("");
		addLine("  {cc.a8}   Cartesi   {cc.NC}                         {cc.a5}.) {cc.a3}|{cc.NC}");
		addLine("  {cc.a8} Battleships {cc.NC}                      {cc.a3}____|_|_{cc.a5}(.{cc.NC}");
		addLine("                                     {cc.a3}_\\______|{cc.NC}");
		addLine("                                   {cc.a3}_/________|_{cc.a4}//{cc.a3}_{cc.NC}");
		addLine("               {cc.a3}_______            /   {cc.a6}<<<{cc.a3}         |{cc.NC}");
		addLine("               {cc.a3}\\ {cc.a5}...  {cc.a3}\\___{cc.a4}[\\\\\\]{cc.a3}__/_________{cc.a4}[///]{cc.a3}__|___{cc.a7}F{cc.NC}");
		addLine("   {cc.a1}__{cc.a2}4{cc.a1}__        {cc.a3}\\                                     |{cc.NC}");
		addLine("   {cc.a1}\\   /{cc.NC}         {cc.a3}\\   V            {cc.a6}<<<      <<<        {cc.a3}/{cc.NC}");
		addLine("{cc.a0}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{cc.NC}");
		addLine("{cc.a0}~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~{cc.NC}");
		addLine("{cc.a0} ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ {cc.NC}");
		addLine("");
		addLine("");
	}

	printLogo();

	this.showMainMenu = (fn_CreateGame, fn_JoinGame, fn_TestReceive) => {
		var menu = new TerminalMenu({
			width: 60,
			fg: "yellow",
			bg: "black",
			padding: { left: 4, right: 4, top: 1, bottom: 2 },
		});
		for (const line of linesLogo) {
			menu.writeLine(line);
		}
		menu.writeSeparator();
		menu.add("Create game", (label, marker) => fn_CreateGame(label, marker));
		menu.add("Join game", (label, marker) => fn_JoinGame(label, marker));
		menu.add("Test receive", (label, marker) => fn_TestReceive(label, marker));
		menu.writeSeparator();
		menu.add("Exit", menu.close);
	}

	this.showJoinGameMenu = (onJoin) => {
		inquirer
		.prompt([{
			type: 'input', name: 'gameId',
			message: 'Join to game by ID: ',
		}])
		.then(onJoin);
	}

	this.showCreateGameMenu = (onCreate) => {
		const fnValidateBoardSize = (input) => {
			let num = Number(input);
			return !isNaN(num) && num >= 5 && num <= 25;
		}
		const fnValidateShips = (input) => {
			let num = Number(input);
			return !isNaN(num) && num >= 0 && num <= 5;
		}

		inquirer
		.prompt([{ 
				type: 'list', name: 'rules', 
				message: 'Game rules', 
				choices: [
					{ value: 'std', name: 'Standard rules (10x10 board, Standard fleet)' },
					{ value: 'custom', name: 'Custom rules' } ]
			}, {
				when: (answers) => answers.rules == 'custom',
				type: 'list', name: 'boardsize',
				message: 'Board size', 
				default: 1,
				choices: [
					{ value: '8', name: '8x8' },
					{ value: '10', name: '10x10' },
					{ value: '12', name: '12x12' },
					{ value: '16', name: '16x16' },
					{ value: '20', name: '20x20' },
					{ value: 'custom', name: 'Custom size' } ]
			}, {
				when: (answers) => answers.boardsize == 'custom',
				type: 'number', name: 'bsx',
				message: 'Board columns count (5-25): ',
				default: '10',
				validate: fnValidateBoardSize
			}, {
				when: (answers) => answers.boardsize == 'custom',
				type: 'number', name: 'bsy',
				message: 'Board rows count (5-25): ',
				default: '10',
				validate: fnValidateBoardSize
			}, {
				when: (answers) => answers.rules == 'custom',
				type: 'list', name: 'ships',
				message: 'Available ships', 
				default: 0,
				choices: [
					{ value: '1', name: 'Standard fleet (1 5pin, 1 4pin, 2 3pin, 1 2pin)' },
					{ value: '2', name: 'Extended fleet (1 5pin, 2 4pin, 3 3pin, 4 2pin)' },
					{ value: '3', name: 'Compact fleet (1 4pin, 1 3pin, 2 2pin)' },
					{ value: 'custom', name: 'Custom fleet' } ]
			}, {
				when: (answers) => answers.ships == 'custom',
				type: 'number', name: 'pin5',
				message: 'Count of 5pin ships (Carriers): ',
				default: '1',
				validate: fnValidateShips
			}, {
				when: (answers) => answers.ships == 'custom',
				type: 'number', name: 'pin4',
				message: 'Count of 4pin ships (Cruisers): ',
				default: '1',
				validate: fnValidateShips
			}, {
				when: (answers) => answers.ships == 'custom',
				type: 'number', name: 'pin3',
				message: 'Count of 3pin ships (Submarines): ',
				default: '2',
				validate: fnValidateShips
			}, {
				when: (answers) => answers.ships == 'custom',
				type: 'number', name: 'pin2',
				message: 'Count of 2pin ships (Frigates): ',
				default: '1',
				validate: fnValidateShips
			}, {
				when: (answers) => answers.ships == 'custom',
				type: 'number', name: 'pin1',
				message: 'Count of 1pin ships (Boats): ',
				default: '0',
				validate: fnValidateShips
			}, {
				type: 'list', name: 'visibility',
				message: 'Opponent',
				choices: [
					{ value: '1', name: 'Anyone can join' },
					{ value: '2', name: 'Invite user by wallet address' } ]
			}, {
				when: (answers) => answers.visibility == '2',
				type: 'input', name: 'address',
				message: 'Wallet address: ',
			}, {
				type: 'confirm', name: 'confirm',
				message: 'Create game?',
			}
		])
		.then(onCreate);
	}

	this.askConfirm = (msg, onConfirm) => {
		inquirer
		.prompt([{
			type: 'confirm', name: 'confirm',
			message: msg,
		}])
		.then(onConfirm);
	}

}
