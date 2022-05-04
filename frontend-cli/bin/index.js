#!/usr/bin/env node

//import white from "chalk";
//import boxen from "boxen";

// import Jetty from "jetty";
// import inquirer from "inquirer";
// import TerminalMenu from "simple-terminal-menu";

import Menu from "../src/menu.js";
import GamePlay from "../src/gameplay.js";

var createGame = () => {
	const gamePlay = new GamePlay();
	gamePlay.start();
}

var joinGame = () => {

}

const menu = new Menu();
menu.showMainMenu(createGame, joinGame);


// const greeting = white.bgGreen.bold("Hola mundo!");

// const boxenOptions = {
// 	padding: 1,
// 	margin: 1,
// 	borderStyle: "round",
// 	borderColor: "green",
// 	backgroundColor: "#555555"
//    };
// const msgBox = boxen(greeting, boxenOptions);

// console.log(msgBox);

//const c = white;
//const r1 = "  " + c.bgYellowBright.black("   Cartesi   ") + "                         \x1b[0;37m.) \x1b[1;30m|\x1b[0m";
//const r2 = "  " + c.bgYellowBright.black(" Battleships ") + "                      {cc.a3}____|_|_{cc.a5}(.{cc.NC}";

// var lines = [];
// var printLogo = () => {

// 	// var colorsLogo = {
// 	// 	NC: "\x1b[0m",
// 	// 	a0 : "\x1b[0;34m",
// 	// 	a1 : "\x1b[1;37m",
// 	// 	a2 : "\x1b[1;31m",
// 	// 	a3 : "\x1b[1;30m",
// 	// 	a4 : "\x1b[0;36m",
// 	// 	a5 : "\x1b[0;37m",
// 	// 	a6 : "\x1b[0;30m",
// 	// 	a7 : "\x1b[1;32m",
// 	// 	a8 : "\x1b[1;30;103m"
// 	// };

// 	var colorsLogo = {
// 		NC: "\x1b[40m",
// 		a0 : "\x1b[0;34;40m",
// 		a1 : "\x1b[1;37;40m",
// 		a2 : "\x1b[1;31;40m",
// 		a3 : "\x1b[1;30;40m",
// 		a4 : "\x1b[0;36;40m",
// 		a5 : "\x1b[0;37;40m",
// 		a6 : "\x1b[0;35;40m",
// 		a7 : "\x1b[1;32;40m",
// 		a8 : "\x1b[1;30;103m"
// 	};

// 	lines = [];

// 	var addLine = (line) => {
// 		for (var key in colorsLogo) {
// 			var ph = "{cc." + key + "}"
// 			line = line.replaceAll(ph, colorsLogo[key]);
// 		}
// 		lines.push(line);		
// 		console.log(line);
// 	}

// 	console.clear();

// 	addLine("");
// 	addLine("");
// 	addLine("  {cc.a8}   Cartesi   {cc.NC}                         {cc.a5}.) {cc.a3}|{cc.NC}");
// 	addLine("  {cc.a8} Battleships {cc.NC}                      {cc.a3}____|_|_{cc.a5}(.{cc.NC}");
// 	addLine("                                     {cc.a3}_\\______|{cc.NC}");
// 	addLine("                                   {cc.a3}_/________|_{cc.a4}//{cc.a3}_{cc.NC}");
// 	addLine("               {cc.a3}_______            /   {cc.a6}<<<{cc.a3}         |{cc.NC}");
// 	addLine("               {cc.a3}\\ {cc.a5}...  {cc.a3}\\___{cc.a4}[\\\\\\]{cc.a3}__/_________{cc.a4}[///]{cc.a3}__|___{cc.a7}F{cc.NC}");
// 	addLine("   {cc.a1}__{cc.a2}4{cc.a1}__        {cc.a3}\\                                     |{cc.NC}");
// 	addLine("   {cc.a1}\\   /{cc.NC}         {cc.a3}\\   V            {cc.a6}<<<      <<<        {cc.a3}/{cc.NC}");
// 	addLine("{cc.a0}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{cc.NC}");
// 	addLine("{cc.a0}~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~{cc.NC}");
// 	addLine("{cc.a0} ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ {cc.NC}");
// 	addLine("");
// 	addLine("");
// }

// printLogo();

// var stdin = process.openStdin();

// stdin.resume();
// stdin.on('data', (keydata) => {
// 	process.stdout.write('output: ' + keydata); 
// });




// var jetty = new Jetty(process.stdout);

// // Draw a circle with fly colours
// var i = 0;
// setInterval(function() {
//   i += 0.025;

//   var x = Math.round(Math.cos(i) * 25 + 50),
//       y = Math.round(Math.sin(i) * 13 + 20);

//   jetty.rgb(
//     Math.round(Math.random() * 215),
//     Math.random() > 0.5
//   ).moveTo([y,x]).text(".");
// }, 5);
// //*/

// inquirer
//   .prompt([
//     {
// 		type: 'list',
// 		name: 'main',
// 		message: 'Main menu',
// 		choices: [
// 			'Create game',
// 			'Join game',
// 			new inquirer.Separator(),
// 			'Exit'
// 		  ],
// 	}
//   ])
//   .then((answers) => {
//     console.log(JSON.stringify(answers, null, '  '));
//   })
//   .catch((error) => {
//     if (error.isTtyError) {
//       // Prompt couldn't be rendered in the current environment
//     } else {
//       // Something else went wrong
//     }
//   });
  

// const menu = new TerminalMenu({
// 	width: 60,
// 	fg: "yellow",
// 	bg: "black",
// 	padding: { left: 4, right: 4, top: 1, bottom: 2 },
// });
// for (const line of lines) {
// 	menu.writeLine(line);
// }
// menu.writeSeparator();
// menu.add("Create game", (label, marker) => { });
// menu.add("Join game", (label, marker) => { });
// menu.writeSeparator();
// menu.add("Exit", menu.close);
